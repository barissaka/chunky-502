# Spike 06: Framework for the chat interface

**Project:** Traffic rules and penalties assistant · **Team:** Chunky · **Date:** 31/10/2026 (observations 12–31/10/2026) · **Jira:** [CHUNKY-165](https://chunky-502.atlassian.net/browse/CHUNKY-165) (EN-15, step 1; design document decision D7) · **Prepared by:** Team Chunky

## Question

US-09 asks for a web page with a question box and an answer area, in Turkish, showing the answer with its cited articles. The design document (D7) lists Gradio and Streamlit as candidates; a plain HTML page served by FastAPI is the third option, since the retriever service (CHUNKY-162) will run on FastAPI anyway. Which one should the team build on, and why?

## Method

No new measurement was needed: both earlier prototypes (hosted models, laptop models) already shipped a working page, so the comparison is based on what the project has actually run plus a reading of the other two frameworks' documentation against the requirements of US-09, EN-15 and the risk register (report-and-maintain, CPU answer times of minutes).

Requirements used as criteria:

1. Chat layout: question box, send, streamed or whole answer, cited chunks under the answer with scores and pages.
2. All visible text in Turkish, editable by a non-developer (CHUNKY-166).
3. Sidebar controls for experiments (k, top, reranker, model, prompt) — needed for the D5/D6 measurements, hidden or reduced for the demo.
4. One code path for two back-ends: the `/ask` endpoint when it exists, the local pipeline until then.
5. Easy to implement: Python alone is enough.
6. Runs offline on the host laptop; can be shown to teammates remotely for review.
7. Testable without a browser (the answer takes 4–6 minutes on CPU; manual click-testing is expensive).

## Findings

| # | Finding | Evidence |
|---|---|---|
| 1 | **Streamlit is already proven in this project.** Both prototypes ended with a Streamlit page (`app.py`): chat history, streamed tokens, first-token time, token counter, sources expander, sidebar settings. Teammates used the hosted-model page through a Cloudflare tunnel (`localhost:8501` exposed by one command) without installing anything. | `evren-spike/app.py`, `laptop-spike/app.py`; tunnel used 12–13/10/2026 |
| 2 | **All three can build the chat layout; the difference is control over the "answer + sources" block.** Streamlit: `st.chat_message` / `st.chat_input` plus any widget (expander, columns, caption) inside the assistant bubble. Gradio: `gr.ChatInterface` gives the chat in a few lines but the sources block must be rendered as Markdown inside the message or built with `gr.Blocks` by hand — more code than Streamlit for the same result. Plain HTML + FastAPI: unlimited, but streaming, history and layout are all hand-written JavaScript. | Framework docs; both prototype apps |
| 3 | **Turkish texts in one file works the same in all three; Streamlit needs no extra wiring.** In the current `app.py` every string comes from `texts.py` (`T["key"]`), so CHUNKY-166 can be done by editing one file without touching the page code. Gradio would need the same pattern plus overriding its built-in English labels ("Submit", "Clear", "Retry"); the HTML option would need a template engine. | `texts.py` (CHUNKY-166 attachment), 31/10/2026 |
| 4 | **Two back-ends, one rendering path, is already implemented in Streamlit.** `app.py` reads `CHUNKY_API_URL` from `.env`: set → `POST /ask` per `docs/ask-endpoint-contract.md`; unset → calls `rag.py` directly and builds the same response object. Switching is one line in `.env`. Nothing in this is Streamlit-specific, so it is not an argument against the others — but it is done. | `app.py` `answer_api()` / `answer_local()`; `.env.example` |
| 5 | **Theming and hiding the toolbar are configuration, not code.** Colours, light theme and `toolbarMode = "minimal"` (hides the Deploy/menu bar for the demo) live in `.streamlit/config.toml`. Gradio: a theme object in code. HTML: CSS by hand. | `.streamlit/config.toml` |
| 6 | **Headless testing exists for Streamlit.** `streamlit.testing.v1.AppTest` runs the page without a browser and lets a script type a question and read the rendered answer; used on 31/10/2026 to verify the Turkish error message when Ollama is down. Gradio has a Python client for calling a running app; the HTML option would need Playwright. | AppTest run, 31/10/2026 |
| 7 | **Gradio's advantage is the built-in public link; Streamlit covers it with a tunnel.** `demo.launch(share=True)` gives a temporary URL with no setup; Streamlit needs `cloudflared tunnel --url http://localhost:8501` (already used with the hosted-model prototype). Both links are temporary; neither is a deployment. | Prototype notes |
| 8 | **Memory and start-up cost are negligible next to the models.** Streamlit server about 150 MB resident; page reload re-runs the script but `st.cache_resource` keeps the index, reranker and config loaded. Not measured for Gradio; expected to be similar. The models (about 6 GB resident) dominate. | Process memory on the laptop |

Comparison against the seven criteria:

| Criterion | Streamlit | Gradio | HTML + FastAPI |
|---|---|---|---|
| 1 Chat layout with sources block | built in, flexible | built in, less flexible | all by hand |
| 2 Turkish texts in one file | done (`texts.py`) | possible, plus label overrides | template engine needed |
| 3 Sidebar controls | `st.sidebar`, done | `gr.Blocks` columns | by hand |
| 4 Two back-ends, one path | done | would be redone | would be redone |
| 5 Python only | yes | yes | no (JavaScript) |
| 6 Offline + remote review | yes; tunnel proven | yes; share link built in | yes; needs hosting for review |
| 7 Headless test | `AppTest`, used | Python client | Playwright |
| Already working in the project | two prototypes | — | — |

## What this means for the project

- **Decision: Streamlit (D7 closed).** It is the only option with no new learning or rewriting cost: the page exists, runs on the laptop, and already handles both back-ends. Gradio would reach the same page with somewhat more layout code and no feature the project needs; the HTML option adds a JavaScript layer.
- **What is not decided by this spike:** whether the UI and the retriever service run as one process or two. The current split — Streamlit on 8501, FastAPI on 8000, HTTP between them — keeps the service testable without the UI and the UI testable without the service, and is the recommended default.
- **Known Streamlit cost to live with:** Streamlit re-runs the script from the top on every click; slow-to-load objects (index, reranker, config) are kept in memory with `st.cache_resource`, otherwise they would be reloaded on every question. Also, the imported `texts.py` is cached by the Python process, so text changes need a server restart (observed 31/10/2026). Both are documented in `docs/ui-notes.md`.

## Open questions

- Behaviour with two users at once: Streamlit serves both sessions, but one Ollama on one CPU roughly doubles both answer times (contract open point 3). The UI disables the send button while waiting; a queue, if needed, belongs in the service.
- Mobile layout was not evaluated; the demo is a laptop screen.
