"""Step 6: question -> hybrid retrieval (top_k articles) -> prompt -> open LLM on Vertex AI (MaaS) -> answer with citations.

Usage (from a notebook or script):
    cfg = load_config()
    embedder = Embedder(cfg["embedding"]["model"], cfg["embedding"]["revision"], cfg["embedding"]["max_tokens"])
    index = load_index()
    result = answer("Şehir içinde hız sınırı nedir?", embedder, index, cfg)

Authentication: Application Default Credentials (run `gcloud auth application-default login` once).
"""

import re
import time

import google.auth
import google.auth.transport.requests
import requests

from chunky.index import ROOT, search

# Chunk IDs as produced by chunk.py, e.g. KTK-m48, SAĞLIK-m4, KTY-cetvel4, KTK-m65A, KTK-islenemeyen.
# Models sometimes write the hyphen as a Unicode variant (e.g. U+2011 non-breaking hyphen), so any dash is accepted.
CHUNK_ID = re.compile(r"(KTK|KTY|KURS|SAĞLIK|MUAYENE|SKUTER)[-‐-―−]([A-Za-z0-9]+)")


def citation_label(c):
    """Human-readable citation: document title, article label, heading, version date."""
    heading = f" – {c['article_heading']}" if c["article_heading"] else ""
    return f"{c['doc_title']}, {c['article_label']}{heading} (version {c['version_date']})"


def format_context(hits):
    blocks = [f"[{c['chunk_id']}] {citation_label(c)}\n{c['text']}" for _, c in hits]
    return "\n\n---\n\n".join(blocks)


def call_llm(messages, gen):
    """Calls an open model served by Vertex AI as a managed API (OpenAI-compatible chat completions)."""
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds.refresh(google.auth.transport.requests.Request())
    url = (
        f"https://{gen['location']}-aiplatform.googleapis.com/v1/projects/{gen['project']}"
        f"/locations/{gen['location']}/endpoints/openapi/chat/completions"
    )
    body = {"model": gen["model"], "messages": messages, "temperature": gen["temperature"]}
    r = requests.post(url, headers={"Authorization": f"Bearer {creds.token}"}, json=body, timeout=180)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def answer(question, embedder, index, cfg):
    start = time.time()
    ret, gen = cfg["retrieval"], cfg["generation"]
    hits = search(question, embedder, index, k=ret["top_k"], sparse_weight=ret["sparse_weight"])
    system_prompt = (ROOT / "prompts" / f"{gen['prompt']}.txt").read_text(encoding="utf-8")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Articles:\n\n{format_context(hits)}\n\nQuestion: {question}"},
    ]
    # Normalize cited IDs to the plain-hyphen form used in chunks.jsonl.
    text = CHUNK_ID.sub(lambda m: f"{m[1]}-{m[2]}", call_llm(messages, gen))

    # Citation check: every cited ID must be one of the retrieved articles.
    retrieved = {c["chunk_id"]: c for _, c in hits}
    cited = list(dict.fromkeys(f"{doc}-{rest}" for doc, rest in CHUNK_ID.findall(text)))
    return {
        "question": question,
        "answer": text,
        "sources": [citation_label(retrieved[i]) for i in cited if i in retrieved],
        "cited": cited,
        "unknown_citations": [i for i in cited if i not in retrieved],
        "retrieved": list(retrieved),
        "model": gen["model"],
        "prompt": gen["prompt"],
        "seconds": round(time.time() - start, 1),  # end-to-end: retrieval + LLM call
    }