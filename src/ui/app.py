"""Chunky — Trafik Mevzuatı Asistanı · Streamlit sohbet arayüzü (US-09 / CHUNKY-125, EN-15 / CHUNKY-165)

İki çalışma modu, tek ekran:
  * API modu   — .env'de CHUNKY_API_URL tanımlıysa soru  POST {CHUNKY_API_URL}/ask  ile retriever servisine gider
                 (sözleşme: docs/ask-endpoint-contract.md). Cevap tek parça gelir.
  * Yerel mod  — CHUNKY_API_URL yoksa aynı klasördeki laptop-spike pipeline'ı (rag.py + Ollama) doğrudan çağrılır;
                 cevap akışlı yazılır. Yerel mod sözleşmedeki yanıt nesnesinin aynısını üretir, arayüz tek yol kullanır.

Tüm Türkçe metinler texts.py'de (T sözlüğü). Tema .streamlit/config.toml'da.

Çalıştır:  python -m streamlit run app.py        ->  http://localhost:8501
.env:      CHUNKY_API_URL=http://localhost:8000   (isteğe bağlı)   CHUNKY_API_TIMEOUT_S=600
"""
from __future__ import annotations

import os
import time
from pathlib import Path

import requests
import streamlit as st

from texts import DOC_NAMES, T

ROOT = Path(__file__).resolve().parent
MAX_QUESTION_CHARS = 1000


# ----------------------------------------------------------------------------- .env
def _load_env() -> None:
    """python-dotenv varsa onu, yoksa basit bir okuyucu kullan; ortam değişkeni .env'i ezer."""
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
        return
    except ImportError:
        pass
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()
API_URL = os.environ.get("CHUNKY_API_URL", "").strip().rstrip("/")
API_TIMEOUT = float(os.environ.get("CHUNKY_API_TIMEOUT_S", "600"))
API_MODE = bool(API_URL)


class UIError(Exception):
    """Kullanıcıya gösterilecek, çevrilmiş hata metni."""


# ----------------------------------------------------------------------------- yerel pipeline (API yoksa)
if not API_MODE:
    import llm_api
    import rag

    @st.cache_resource(show_spinner=False)
    def _reranker(model: str, max_len: int, bs: int):
        from rerank import Reranker

        return Reranker(model, max_len, bs)

    @st.cache_resource(show_spinner=False)
    def _retriever(use_rerank: bool, prompt_file: str):
        cfg = rag.load_config()
        rr = _reranker(cfg["reranker_model"], cfg.get("rerank_max_length", 1536), cfg.get("rerank_batch_size", 4)) if use_rerank else None
        return rag.Retriever(cfg, use_rerank=use_rerank, reranker=rr, prompt_file=prompt_file)

    LOCAL_CFG = rag.load_config()
    PROMPTS = sorted(p.stem for p in (ROOT / "prompts").glob("*.md"))
    try:
        LOCAL_MODELS = [m for m in llm_api.installed_models(LOCAL_CFG["ollama_base_url"]) if "embed" not in m and "rerank" not in m]
        LOCAL_OLLAMA_OK = True
    except Exception:
        LOCAL_MODELS, LOCAL_OLLAMA_OK = [LOCAL_CFG["answer_model"]], False


def _pages(chunk: dict):
    p = chunk.get("pages")
    if isinstance(p, (list, tuple)) and p:
        return [p[0], p[-1]]
    if isinstance(p, (int, str)) and str(p).strip():
        return [str(p), str(p)]
    return None


def _source_from_chunk(chunk: dict, score: float, with_text: bool) -> dict:
    doc = chunk.get("doc_id") or chunk["id"].split("-")[0]
    return {
        "id": chunk["id"],
        "document": DOC_NAMES.get(doc, doc),
        "article": rag.article_of(chunk) if not API_MODE else None,
        "header": chunk.get("header", chunk["id"]),
        "pages": _pages(chunk),
        "score": round(float(score), 4),
        "text": (chunk["text"][:4000] if with_text else None),
    }


def answer_local(question: str, opts: dict, box) -> dict:
    """Sözleşmedeki 200 yanıtının aynısını üretir; cevabı `box` içine akışlı yazar."""
    r = _retriever(opts["rerank"], f"prompts/{opts['prompt']}.md")
    t0 = time.perf_counter()
    with st.spinner(T["spinner_retrieving"]):
        res = r.retrieve(question, opts["k"], opts["top"])
    ids = [cid for cid, _ in res["final"]]
    box.markdown(T["writing"])
    text, stats, t_first = "", {}, None
    t1 = time.perf_counter()
    for kind, piece in r.answer_stream(question, ids, opts["model"], False):
        if kind == "content":
            if t_first is None:
                t_first = time.perf_counter() - t0
            text += piece
            box.markdown(text + T["cursor"])
        elif kind == "done":
            stats = piece
    text = text.strip()
    refused = rag.is_refusal(text) or not text
    return {
        "request_id": "local-" + time.strftime("%Y%m%d-%H%M%S"),
        "question": question,
        "answer": text or T["empty_answer"],
        "refused": refused,
        "refusal_reason": ("not_in_corpus" if text else "empty_or_invalid") if refused else None,
        "sources": [] if refused else [_source_from_chunk(r.by_id[cid], s, True) for cid, s in res["final"]],
        "config": {
            "model": stats.get("model", opts["model"]), "prompt": r.prompt_name, "k": opts["k"], "top": opts["top"],
            "rerank": opts["rerank"], "embedding_model": r.cfg["embedding_model"], "reranker_model": r.cfg["reranker_model"],
            "corpus_version": r.index.meta.get("built_at", "?"),
        },
        "timings": {
            "retrieval_s": res["timings"]["retrieval_s"],
            "first_token_s": round(t_first, 3) if t_first else None,
            "total_s": round(time.perf_counter() - t0, 3),
        },
        "usage": {"prompt_tokens": stats.get("prompt_tokens"), "completion_tokens": stats.get("completion_tokens")},
    }


# ----------------------------------------------------------------------------- API modu
def api_health() -> dict | None:
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def answer_api(question: str, opts: dict | None) -> dict:
    payload: dict = {"question": question, "client": {"name": "streamlit-ui", "version": "0.1"}}
    if opts:
        payload["options"] = opts
    try:
        r = requests.post(f"{API_URL}/ask", json=payload, timeout=API_TIMEOUT)
    except requests.exceptions.Timeout:
        raise UIError(T["err_timeout"])
    except requests.exceptions.RequestException:
        raise UIError(T["err_connection"].format(url=API_URL))
    if r.status_code == 200:
        data = r.json()
        data.setdefault("refused", False)
        data.setdefault("refusal_reason", None)
        data.setdefault("sources", [])
        data.setdefault("config", {})
        data.setdefault("timings", {})
        data.setdefault("usage", {})
        return data
    body = {}
    try:
        body = r.json()
    except ValueError:
        pass
    err = body.get("error", {}) if isinstance(body, dict) else {}
    if r.status_code == 422 and err.get("code") == "rejected":  # sözleşme §3: ret, hata değil
        reason = err.get("reason", "default")
        return {"request_id": body.get("request_id", "-"), "question": question,
                "answer": T["refusal"].get(reason, T["refusal"]["default"]), "refused": True,
                "refusal_reason": reason, "sources": [], "config": {}, "timings": {}, "usage": {}}
    if r.status_code == 400:
        raise UIError(T["err_bad_request"])
    if r.status_code == 503:
        raise UIError(T["err_model_unavailable"])
    if r.status_code == 504:
        raise UIError(T["err_timeout"])
    raise UIError(T["err_generic"].format(code=r.status_code))


# ----------------------------------------------------------------------------- sayfa
st.set_page_config(page_title=T["page_title"], page_icon="🚦", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if API_MODE and "health" not in st.session_state:
    st.session_state.health = api_health()

with st.sidebar:
    st.title(T["sidebar_title"])
    st.caption(T["sidebar_caption"])
    if API_MODE:
        st.markdown(T["mode_api"].format(url=API_URL))
        h = st.session_state.health
        if h:
            st.success(T["health_ok"].format(corpus=h.get("corpus_version", "?")))
    else:
        st.markdown(T["mode_local"])
        if not LOCAL_OLLAMA_OK:
            st.error(T["err_model_unavailable"])

    st.subheader(T["settings_header"])
    opts: dict = {}
    if API_MODE:
        with st.expander(T["advanced_expander"]):
            rerank = st.toggle(T["opt_rerank"], value=True)
            k = st.slider(T["opt_k"], 5, 40, 20, step=5)
            top = st.slider(T["opt_top"], 1, 10, 5)
        if not (rerank and k == 20 and top == 5):  # yalnızca değiştirildiyse gönder
            opts = {"rerank": rerank, "k": k, "top": top}
    else:
        default_ix = next((i for i, m in enumerate(LOCAL_MODELS) if m.split(":latest")[0] == LOCAL_CFG["answer_model"]), 0)
        model = st.selectbox(T["opt_model"], LOCAL_MODELS, index=default_ix)
        default_prompt = Path(LOCAL_CFG["prompt_file"]).stem
        prompt = st.selectbox(T["opt_prompt"], PROMPTS, index=PROMPTS.index(default_prompt) if default_prompt in PROMPTS else 0)
        rerank = st.toggle(T["opt_rerank"], value=LOCAL_CFG.get("rerank", True))
        k = st.slider(T["opt_k"], 5, 40, LOCAL_CFG["k"], step=5)
        top = st.slider(T["opt_top"], 1, 10, LOCAL_CFG["top"])
        opts = {"model": model, "prompt": prompt, "rerank": rerank, "k": k, "top": top}
    show_text = st.toggle(T["opt_show_text"], value=False)

    st.divider()
    if API_MODE:
        h = st.session_state.health or {}
        if h.get("embedding_model"):
            st.markdown(T["models_line"].format(embedding=h.get("embedding_model"), reranker=h.get("reranker_model", "-")))
    else:
        try:
            n_chunks = sum(1 for _ in open(LOCAL_CFG["chunks_file"], encoding="utf-8"))
            st.markdown(T["corpus_line"].format(n_chunks=n_chunks))
        except OSError:
            pass
        st.markdown(T["models_line"].format(embedding=LOCAL_CFG["embedding_model"], reranker=LOCAL_CFG["reranker_model"]))
    if st.button(T["clear_chat"], use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption(T["disclaimer"])
    st.caption(T["ai_disclaimer"])


def render_sources(result: dict) -> None:
    tm, us, cf = result.get("timings", {}), result.get("usage", {}), result.get("config", {})
    if result.get("refused") or not result.get("sources"):
        if result.get("request_id"):
            st.caption(f"istek {result['request_id']}")
        return
    label = T["sources_label"].format(total=tm.get("total_s") or 0)
    if tm.get("retrieval_s") is not None:
        label += (T["sources_label_detail"].format(retr=tm["retrieval_s"], ttft=tm["first_token_s"])
                  if tm.get("first_token_s") else T["sources_label_detail_no_ttft"].format(retr=tm["retrieval_s"]))
    with st.expander(label, expanded=False):
        for s in result["sources"]:
            line = T["source_line"].format(header=s.get("header", s.get("id")), score=s.get("score") or 0)
            if s.get("pages"):
                p = s["pages"]
                line += T["source_pages"].format(pages=f"{p[0]}–{p[1]}" if p[0] != p[1] else p[0])
            st.markdown(line)
            if show_text and s.get("text"):
                st.text(s["text"][:1500])
        if us.get("prompt_tokens") or us.get("completion_tokens"):
            st.caption(T["tokens_line"].format(prompt=us.get("prompt_tokens", "-"), completion=us.get("completion_tokens", "-")))
        st.caption(T["config_line"].format(
            model=cf.get("model", "-"), prompt=cf.get("prompt", "-"), k=cf.get("k", "-"), top=cf.get("top", "-"),
            rerank=T["rerank_on"] if cf.get("rerank") else T["rerank_off"], request_id=result.get("request_id", "-")))


st.title(T["title"])
st.caption(T["subtitle"])
st.info(T["ai_disclaimer"], icon="ℹ️")

st.markdown(f"### {T['ask_heading']}")
cols = st.columns(len(T["examples"]))
clicked = None
for c, ex in zip(cols, T["examples"]):
    if c.button(ex, use_container_width=True):
        clicked = ex

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar=T["avatar_user"] if m["role"] == "user" else T["avatar_assistant"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and m.get("result"):
            render_sources(m["result"])

question = st.chat_input(T["input_placeholder"]) or clicked

if question:
    question = question.strip()
    if len(question) > MAX_QUESTION_CHARS:
        st.warning(T["input_too_long"].format(n=len(question), max=MAX_QUESTION_CHARS))
        question = question[:MAX_QUESTION_CHARS]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar=T["avatar_user"]):
        st.markdown(question)
    with st.chat_message("assistant", avatar=T["avatar_assistant"]):
        box = st.empty()
        result = None
        try:
            if API_MODE:
                with st.spinner(T["spinner_waiting_api"]):
                    result = answer_api(question, opts)
            else:
                result = answer_local(question, opts, box)
            text = result["answer"]
            if result.get("refused"):
                text = T["refusal"].get(result.get("refusal_reason") or "default", result["answer"]) if result.get("refusal_reason") != "not_in_corpus" else result["answer"]
            if result.get("question") and result["question"] != question:
                st.caption(T["interpreted_as"].format(q=result["question"]))
            box.markdown(text)
        except UIError as e:
            text = str(e)
            box.error(text)
        except Exception as e:  # yerel pipeline hataları — kullanıcıya Türkçe, ayrıntı terminale
            print(f"[app] yerel pipeline hatası: {type(e).__name__}: {e}", flush=True)
            is_conn = isinstance(e, requests.exceptions.RequestException) or "Ollama" in type(e).__name__
            text = T["err_model_unavailable"] if is_conn else T["err_generic"].format(code=type(e).__name__)
            box.error(text)
        if result:
            render_sources(result)
    st.session_state.messages.append({"role": "assistant", "content": text, "result": result})
