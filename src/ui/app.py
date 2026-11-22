"""Chunky web interface: Streamlit chat page for the traffic legislation assistant.

Jira: US-09 / CHUNKY-125 (question box and answer area), EN-15 / CHUNKY-165 (interface
framework and /ask connection), US-04 (new chat button).

The page has two modes and one screen:

* Local mode (default): calls the team pipeline in ``src/chunky`` directly, the same
  function as ``notebooks/05_answer_check.ipynb`` (``chunky.answer.answer``). Retrieval
  runs on this laptop with the bge-m3 index; the answer comes from the model set in
  ``config/rag.yaml`` (Google Cloud Vertex AI).
* API mode: if ``CHUNKY_API_URL`` is set in ``src/ui/.env``, each question is sent to
  ``POST {CHUNKY_API_URL}/ask`` instead (contract: ``docs/ask-endpoint-contract.md``).

Prerequisites (README, "Running the baseline"): ``pip install -e .`` in the virtual
environment, the index built with ``python -m chunky.index``, and
``gcloud auth application-default login``.

All Turkish texts shown on the page are in ``texts.py`` (dictionary ``T``); the theme is in
``.streamlit/config.toml``, which Streamlit reads only when started from this folder.

Run from ``src/ui``:  ``python -m streamlit run app.py``  ->  http://localhost:8501
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


# ----------------------------------------------------------------------------- .env settings
def _load_env() -> None:
    """Load ``src/ui/.env`` into the process environment.

    Uses python-dotenv when it is installed; otherwise reads ``KEY=VALUE`` lines with a
    small built-in parser. Variables already set in the environment are not overwritten.

    Returns:
        None. The values are written to ``os.environ``.
    """
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
    """Error whose message is a Turkish text meant to be shown to the user as is."""


# ----------------------------------------------------------------------------- local mode: the team pipeline
if not API_MODE:
    from chunky.answer import answer as chunky_answer
    from chunky.index import ROOT as REPO_ROOT
    from chunky.index import Embedder, load_config, load_index

    CFG = load_config()

    @st.cache_resource(show_spinner=False)
    def _pipeline():
        """Load the embedding model and the search index once per server process.

        Streamlit keeps the result in memory (``st.cache_resource``), so later questions
        and page reloads do not load bge-m3 again. An exception is not cached, so the page
        retries after the index has been built.

        Returns:
            tuple: ``(embedder, index, by_id)`` where ``embedder`` is the bge-m3
            ``chunky.index.Embedder``, ``index`` is the tuple returned by
            ``chunky.index.load_index()`` and ``by_id`` maps each ``chunk_id`` to its
            chunk record (title, article label, heading, version date, text).

        Raises:
            UIError: if the index folder (``index/bge-m3``) does not exist.
        """
        emb = CFG["embedding"]
        try:
            index = load_index()
        except FileNotFoundError:
            raise UIError(T["err_index_missing"])
        embedder = Embedder(emb["model"], emb["revision"], emb["max_tokens"])
        by_id = {c["chunk_id"]: c for c in index[2]}
        return embedder, index, by_id


def _local_error(e: Exception) -> str:
    """Turn an error of the local pipeline into a Turkish message that says what to do.

    The technical details are printed to the terminal; the user sees only the message.

    Args:
        e: the exception raised by ``chunky.answer.answer``.

    Returns:
        str: one of the error texts of ``texts.T``: missing Google Cloud login, no access
        to the project (HTTP 401/403/404), model unavailable (HTTP 429/5xx or a network
        error), timeout, or a generic error with the exception name.
    """
    print(f"[app] yerel pipeline hatası: {type(e).__name__}: {e}", flush=True)
    if type(e).__name__ == "DefaultCredentialsError" or "credentials" in str(e).lower():
        return T["err_auth"]
    if isinstance(e, requests.exceptions.HTTPError) and e.response is not None:
        code = e.response.status_code
        if code in (401, 403, 404):
            return T["err_permission"].format(code=code, project=CFG["generation"]["project"])
        if code in (429, 500, 502, 503):
            return T["err_model_unavailable"]
    if isinstance(e, requests.exceptions.Timeout):
        return T["err_timeout"]
    if isinstance(e, requests.exceptions.RequestException):
        return T["err_model_unavailable"]
    return T["err_generic"].format(code=type(e).__name__)


def answer_local(question: str) -> dict:
    """Answer a question with the team pipeline and shape the result for the page.

    Calls ``chunky.answer.answer`` with the settings of ``config/rag.yaml`` and converts its
    result into the same fields as the /ask contract, so that both modes are shown by the
    same code.

    Args:
        question: the user's question, already stripped and cut to
            ``MAX_QUESTION_CHARS``.

    Returns:
        dict: ``request_id``, ``question``, ``answer``, ``refused`` and ``refusal_reason``
        (an empty answer counts as refused), ``sources`` (one entry per cited article that
        was also retrieved: ``id``, ``document``, ``header``, ``version_date``, ``text``),
        ``unknown_citations`` (cited ids that were not retrieved), ``config`` (model,
        prompt, ``top_k``, sparse weight), ``timings`` (``total_s``) and ``usage``
        (prompt and completion tokens).

    Raises:
        UIError: if the pipeline fails; the message comes from ``_local_error``.
    """
    embedder, index, by_id = _pipeline()
    gen, ret = CFG["generation"], CFG["retrieval"]
    with st.spinner(T["spinner_answering"]):
        try:
            r = chunky_answer(question, embedder, index, CFG)
        except Exception as e:
            raise UIError(_local_error(e))
    text = (r["answer"] or "").strip()
    sources = []
    for cid in r["cited"]:
        c = by_id.get(cid)
        if c is None or cid not in r["retrieved"]:
            continue  # cited but not retrieved: left out of the sources and shown as a warning
        heading = f" – {c['article_heading']}" if c.get("article_heading") else ""
        sources.append({
            "id": cid,
            "document": c.get("doc_title") or DOC_NAMES.get(c.get("doc_code"), c.get("doc_code")),
            "header": f"{c.get('doc_title', cid)}, {c.get('article_label', cid)}{heading}",
            "version_date": c.get("version_date"),
            "pages": None,
            "score": None,
            "text": c["text"][:4000],
        })
    return {
        "request_id": "local-" + time.strftime("%Y%m%d-%H%M%S"),
        "question": question,
        "answer": text or T["empty_answer"],
        "refused": not text,
        "refusal_reason": None if text else "empty_or_invalid",
        "sources": sources,
        "unknown_citations": r.get("unknown_citations", []),
        "config": {"model": r["model"], "prompt": r["prompt"], "k": ret["top_k"], "sparse_weight": ret["sparse_weight"]},
        "timings": {"total_s": r["seconds"]},
        "usage": {"prompt_tokens": r.get("input_tokens"), "completion_tokens": r.get("output_tokens")},
    }


# ----------------------------------------------------------------------------- API mode
def api_health() -> dict | None:
    """Ask the /ask service whether it is running (``GET {CHUNKY_API_URL}/health``).

    Returns:
        dict | None: the service's health record (for example ``corpus_version``,
        ``embedding_model``, ``reranker_model``) if it answers with HTTP 200 within
        5 seconds; ``None`` otherwise.
    """
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def answer_api(question: str, opts: dict | None) -> dict:
    """Send a question to the /ask service and return its answer.

    Args:
        question: the user's question, already stripped and cut to
            ``MAX_QUESTION_CHARS``.
        opts: retrieval options chosen in the sidebar (``rerank``, ``k``, ``top``), or
            ``None`` to use the service defaults.

    Returns:
        dict: the service's answer with the contract fields (``answer``, ``sources``,
        ``config``, ``timings``, ``usage`` and so on); missing optional fields are filled
        with empty defaults. A refusal (HTTP 422 with code ``rejected``) is returned as an
        answer with ``refused = True`` and the matching Turkish refusal text.

    Raises:
        UIError: on a timeout, a connection error, or HTTP 400, 503, 504 or any other
        error status, with a Turkish message.
    """
    payload: dict = {"question": question, "client": {"name": "streamlit-ui", "version": "0.2"}}
    if opts:
        payload["options"] = opts
    try:
        with st.spinner(T["spinner_waiting_api"]):
            r = requests.post(f"{API_URL}/ask", json=payload, timeout=API_TIMEOUT)
    except requests.exceptions.Timeout:
        raise UIError(T["err_timeout"])
    except requests.exceptions.RequestException:
        raise UIError(T["err_connection"].format(url=API_URL))
    if r.status_code == 200:
        data = r.json()
        for key, default in (("refused", False), ("refusal_reason", None), ("sources", []),
                             ("config", {}), ("timings", {}), ("usage", {}), ("unknown_citations", [])):
            data.setdefault(key, default)
        return data
    body = {}
    try:
        body = r.json()
    except ValueError:
        pass
    err = body.get("error", {}) if isinstance(body, dict) else {}
    if r.status_code == 422 and err.get("code") == "rejected":  # contract section 3: a refusal, not an error
        reason = err.get("reason", "default")
        return {"request_id": body.get("request_id", "-"), "question": question,
                "answer": T["refusal"].get(reason, T["refusal"]["default"]), "refused": True,
                "refusal_reason": reason, "sources": [], "unknown_citations": [],
                "config": {}, "timings": {}, "usage": {}}
    if r.status_code == 400:
        raise UIError(T["err_bad_request"])
    if r.status_code == 503:
        raise UIError(T["err_model_unavailable"])
    if r.status_code == 504:
        raise UIError(T["err_timeout"])
    raise UIError(T["err_generic"].format(code=r.status_code))


# ----------------------------------------------------------------------------- page
st.set_page_config(page_title=T["page_title"], page_icon="🚦", layout="wide", initial_sidebar_state="collapsed")

# Hide the toolbar menu and the Deploy button (the sidebar toggle stays) and add the fixed
# AI notice under the chat box (mockup: docs/images/ui-mockup-v1.png).
st.markdown(
    f"""<style>
    [data-testid="stAppDeployButton"], .stAppDeployButton, [data-testid="stMainMenu"], #MainMenu {{ display: none !important; }}
    [data-testid="stBottomBlockContainer"]::after {{ content: "{T['ai_notice']}"; display: block; text-align: center;
        font-size: 0.75rem; color: #6b7280; padding: 6px 0 2px 0; }}
    [data-testid="stBottomBlockContainer"] {{ padding-bottom: 0.6rem; }}
    </style>""",
    unsafe_allow_html=True,
)

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

    st.subheader(T["settings_header"])
    opts: dict = {}
    if API_MODE:
        with st.expander(T["advanced_expander"]):
            rerank = st.toggle(T["opt_rerank"], value=True)
            k = st.slider(T["opt_k"], 5, 40, 20, step=5)
            top = st.slider(T["opt_top"], 1, 10, 5)
        if not (rerank and k == 20 and top == 5):  # send options only if changed
            opts = {"rerank": rerank, "k": k, "top": top}
    else:
        gen, ret = CFG["generation"], CFG["retrieval"]
        st.markdown(T["settings_local"].format(
            model=gen["model"], prompt=gen["prompt"], k=ret["top_k"], sw=ret["sparse_weight"]))
    show_text = st.toggle(T["opt_show_text"], value=False)

    st.divider()
    if API_MODE:
        h = st.session_state.health or {}
        if h.get("embedding_model"):
            st.markdown(T["models_line"].format(embedding=h.get("embedding_model"), reranker=h.get("reranker_model", "-")))
    else:
        try:
            n_chunks = sum(1 for _ in open(REPO_ROOT / CFG["corpus"]["chunks"], encoding="utf-8"))
            st.markdown(T["corpus_line"].format(n_chunks=n_chunks))
        except OSError:
            pass
        st.markdown(T["models_line_local"].format(embedding=CFG["embedding"]["model"]))
    st.divider()
    st.caption(T["disclaimer"])
    st.caption(T["ai_disclaimer"])


def render_sources(result: dict) -> None:
    """Show the details under an answer: warnings, sources, timing and settings.

    Args:
        result: an answer in the contract format, from ``answer_local`` or ``answer_api``.

    Returns:
        None. Writes to the page: a warning for citations outside the retrieved set; for a
        refused answer or one without sources only the request id; otherwise a collapsed
        "used chunks" section with one line per source (title, version date, pages, score
        if any, and the text when the sidebar switch is on), token counts and the settings
        of the run. Uses ``show_text`` from the sidebar.
    """
    tm, us, cf = result.get("timings", {}), result.get("usage", {}), result.get("config", {})
    if result.get("unknown_citations"):
        st.warning(T["unknown_citations"].format(ids=", ".join(result["unknown_citations"])))
    if result.get("refused") or not result.get("sources"):
        if result.get("request_id"):
            st.caption(T["request_line"].format(request_id=result["request_id"]))
        return
    label = T["sources_label"].format(total=tm.get("total_s") or 0)
    if tm.get("retrieval_s") is not None:
        label += (T["sources_label_detail"].format(retr=tm["retrieval_s"], ttft=tm["first_token_s"])
                  if tm.get("first_token_s") else T["sources_label_detail_no_ttft"].format(retr=tm["retrieval_s"]))
    with st.expander(label, expanded=False):
        for s in result["sources"]:
            header = s.get("header", s.get("id"))
            line = (T["source_line"].format(header=header, score=s["score"]) if s.get("score") is not None
                    else T["source_line_noscore"].format(header=header))
            if s.get("version_date"):
                line += T["source_version"].format(date=s["version_date"])
            if s.get("pages"):
                p = s["pages"]
                line += T["source_pages"].format(pages=f"{p[0]}–{p[1]}" if p[0] != p[1] else p[0])
            st.markdown(line)
            if show_text and s.get("text"):
                st.text(s["text"][:1500])
        if us.get("prompt_tokens") or us.get("completion_tokens"):
            st.caption(T["tokens_line"].format(prompt=us.get("prompt_tokens", "-"), completion=us.get("completion_tokens", "-")))
        if "sparse_weight" in cf:
            st.caption(T["config_line_local"].format(
                model=cf.get("model", "-"), prompt=cf.get("prompt", "-"), k=cf.get("k", "-"),
                sw=cf.get("sparse_weight", "-"), request_id=result.get("request_id", "-")))
        else:
            st.caption(T["config_line"].format(
                model=cf.get("model", "-"), prompt=cf.get("prompt", "-"), k=cf.get("k", "-"), top=cf.get("top", "-"),
                rerank=T["rerank_on"] if cf.get("rerank") else T["rerank_off"], request_id=result.get("request_id", "-")))


# In local mode bge-m3 is loaded on first open; if the index is missing, the user is told how to build it.
if not API_MODE:
    try:
        with st.spinner(T["spinner_loading"]):
            _pipeline()
    except UIError as e:
        st.error(str(e))
        st.stop()

# Heading row: the question heading on the left, "Yeni Sohbet" on the right (US-04, visible with the sidebar closed)
col_title, col_new = st.columns([6, 1], vertical_alignment="center")
with col_title:
    st.markdown(f"### {T['heading_icon']} {T['ask_heading']}")
with col_new:
    if st.button(T["new_chat"], icon=":material/add_comment:", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
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
            result = answer_api(question, opts) if API_MODE else answer_local(question)
            text = result["answer"]
            if result.get("refused") and result.get("refusal_reason") not in (None, "not_in_corpus"):
                text = T["refusal"].get(result["refusal_reason"], result["answer"])
            if result.get("question") and result["question"] != question:
                st.caption(T["interpreted_as"].format(q=result["question"]))
            box.markdown(text)
        except UIError as e:
            text = str(e)
            box.error(text)
        except Exception as e:  # unexpected error: Turkish message to the user, details to the terminal
            print(f"[app] beklenmeyen hata: {type(e).__name__}: {e}", flush=True)
            text = T["err_generic"].format(code=type(e).__name__)
            box.error(text)
        if result:
            render_sources(result)
    st.session_state.messages.append({"role": "assistant", "content": text, "result": result})
