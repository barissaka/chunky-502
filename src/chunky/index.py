"""Step 5: chunks.jsonl -> bge-m3 dense + sparse vectors -> numpy index on disk.

Run (from the repo root, with .venv active):  python -m chunky.index

The index folder (config/rag.yaml -> vector_store.dir) contains:
  dense.npy      one normalized 1024-dim dense vector per chunk (row order = chunk order)
  sparse.jsonl   one {token_id: weight} dict per chunk (bge-m3 lexical weights)
  chunks.jsonl   chunk metadata and text (payload; includes amendments, which are not embedded)
  manifest.json  model, revision, library versions, build date, duration
"""

import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import transformers
import yaml
from huggingface_hub import hf_hub_download
from transformers import AutoModel, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]


def load_config():
    return yaml.safe_load((ROOT / "config/rag.yaml").read_text(encoding="utf-8"))


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]


class Embedder:
    """Runs bge-m3 without FlagEmbedding (FlagEmbedding is blocked by Windows App Control on the dev laptop).

    dense  = output of the first (CLS) token of the last layer, normalized
    sparse = relu(sparse_linear(hidden state)) per token; if a token occurs more than once, the largest
             weight is kept; special tokens (CLS, EOS, PAD, UNK) are skipped
    """

    def __init__(self, model_name, revision, max_tokens):
        self.tok = AutoTokenizer.from_pretrained(model_name, revision=revision)
        self.model = AutoModel.from_pretrained(model_name, revision=revision).eval()
        self.sparse_linear = torch.nn.Linear(self.model.config.hidden_size, 1)
        path = hf_hub_download(model_name, "sparse_linear.pt", revision=revision)
        self.sparse_linear.load_state_dict(torch.load(path, map_location="cpu"))
        self.max_tokens = max_tokens
        self.special_ids = set(self.tok.all_special_ids)

    @torch.no_grad()
    def encode(self, text):
        x = self.tok(text, truncation=True, max_length=self.max_tokens, return_tensors="pt")
        hidden = self.model(**x).last_hidden_state[0]
        dense = torch.nn.functional.normalize(hidden[0], dim=-1).numpy()
        weights = torch.relu(self.sparse_linear(hidden)).squeeze(-1).tolist()
        sparse = {}
        for token_id, w in zip(x["input_ids"][0].tolist(), weights):
            if token_id not in self.special_ids and w > 0:
                sparse[token_id] = max(sparse.get(token_id, 0.0), w)
        return dense, sparse


def build_index():
    cfg = load_config()
    emb = cfg["embedding"]
    chunks = read_jsonl(ROOT / cfg["corpus"]["chunks"])
    embedder = Embedder(emb["model"], emb["revision"], emb["max_tokens"])

    start = time.time()
    dense, sparse = [], []
    for n, c in enumerate(chunks, 1):
        d, s = embedder.encode(c["text"])
        dense.append(d)
        sparse.append(s)
        if n % 50 == 0 or n == len(chunks):
            print(f"{n}/{len(chunks)} chunks, {time.time() - start:.0f} s")

    out = ROOT / cfg["vector_store"]["dir"]
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "dense.npy", np.stack(dense).astype(np.float32))
    with open(out / "sparse.jsonl", "w", encoding="utf-8") as f:
        for s in sparse:
            f.write(json.dumps(s) + "\n")
    with open(out / "chunks.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    manifest = {
        "model": emb["model"],
        "revision": emb["revision"],
        "chunks": len(chunks),
        "dim": len(dense[0]),
        "built": datetime.now().isoformat(timespec="seconds"),
        "seconds": round(time.time() - start),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Index written:", out)
    print(manifest)


def load_index():
    """Opens the index from disk without embedding anything (the model is not loaded)."""
    out = ROOT / load_config()["vector_store"]["dir"]
    dense = np.load(out / "dense.npy")
    sparse = [{int(k): v for k, v in s.items()} for s in read_jsonl(out / "sparse.jsonl")]
    payload = read_jsonl(out / "chunks.jsonl")
    return dense, sparse, payload


def search(query, embedder, index, k=5, doc_code=None, sparse_weight=0.3):
    """Returns the k highest-scoring chunks as (score, payload) pairs.

    score = dense similarity + sparse_weight * sparse match. sparse_weight=0 -> dense only.
    0.3 is a starting value; to be tuned in the retrieval spike.
    """
    dense, sparse, payload = index
    q_dense, q_sparse = embedder.encode(query)
    scores = dense @ q_dense
    if sparse_weight:
        lexical = np.array([sum(w * s.get(t, 0.0) for t, w in q_sparse.items()) for s in sparse])
        scores = scores + sparse_weight * lexical
    rows = [i for i in np.argsort(-scores) if doc_code is None or payload[i]["doc_code"] == doc_code][:k]
    return [(float(scores[i]), payload[i]) for i in rows]


if __name__ == "__main__":
    build_index()