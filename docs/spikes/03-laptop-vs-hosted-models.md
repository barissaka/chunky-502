# Spike 03: Models on the team laptop or on a hosted API

**Project:** Traffic rules and penalties assistant · **Team:** Chunky · **Date:** 25/10/2026 (measurements 18–24/10/2026) · **Jira:** [CHUNKY-214](https://chunky-502.atlassian.net/browse/CHUNKY-214) (design document, decision D1) · **Prepared by:** Team Chunky

## Question

The design document (D1) places all three models — embedding, reranker and answer LLM — on one team laptop, so that nothing leaves the machine and no external service is needed. The alternative is to keep the data pipeline, index and UI on the laptop but call the models on a hosted inference API (an OpenAI-compatible endpoint; which provider is a separate question). What does each option give up, measured on the same corpus and the same questions?

## Method

Two prototypes with identical data pipeline (six legal texts, `pdftotext -layout`, one chunk per article: 638 chunks, about 210 k tokens), identical retrieval logic (cosine top-20 → reranker → top-5), the same system prompt (`answer_v1`) and the same 20-question evaluation set with expected articles (easy questions; one labelling error found and corrected on the first pass). Only the place and size of the models differ:

| | Laptop | Hosted API |
|---|---|---|
| Host | i7-1355U, 32 GB RAM, no discrete GPU, Windows; Ollama for embedding and LLM, `transformers` on CPU for the reranker | Laptop runs the pipeline; models called over HTTPS on a hosted OpenAI-compatible endpoint |
| Embedding | Qwen3-Embedding 0.6B (1024-d) | Qwen3-Embedding 8B (4096-d) |
| Reranker | Qwen3-Reranker 0.6B | Qwen3-Reranker 8B |
| Answer LLM | Qwen3 4B (Q4_K_M, instruct and thinking) and Qwen3 8B | Gemma 4 31B; DeepSeek V4.1 Flash as a second candidate |
| Runs | 18–24/10/2026 | 18–19/10/2026 |

Retrieval hit@5 = the expected article is among the five chunks handed to the LLM. Answer correctness = every numeric claim checked by hand against the corpus. Timings are wall-clock on the laptop; the hosted service's generation speed varied 5–10× between runs on the same evening, so its timings are ranges.

## Findings

| # | Finding | Evidence |
|---|---|---|
| 1 | **Retrieval quality is the same once the reranker is on.** Dense search alone: 17/20 on the laptop (0.6B embedding) vs 20/20 hosted (8B). With the reranker both reach 20/20 — the 0.6B reranker recovered all three misses. | `03_eval.py --retrieval-only` with and without `--no-rerank`, both prototypes |
| 2 | **Retrieval time differs by two orders of magnitude.** Laptop: embedding the question 2.2 s, reranking 20 candidates with the 0.6B model 80–90 s on CPU (about 95 % of retrieval time); hosted: about 1 s for both. | Per-question timings in `eval_*.jsonl` |
| 3 | **Answer quality depends on model size more than on location.** Laptop Qwen3 4B instruct: 13/20 correct, 2 fabricated numbers. Laptop Qwen3 8B: 19/20, no fabrication. Hosted Gemma 4 31B: 20/20, no fabrication. Hosted DeepSeek V4.1 Flash: 16/20 produced (4 empty or truncated by the reasoning budget), 0 errors among those. | Manual grading of all answers |
| 4 | **Answer time on the laptop is minutes, hosted is seconds.** Laptop 4B instruct: about 186 s per answer (prompt 29 tok/s, generation 5.1 tok/s); 4B with thinking: about 24 min per answer, 4/5 correct on the first five questions, run stopped; 8B: 265–276 s (about 3 tok/s), thinking mode not measured (estimated 15–20 min). Hosted Gemma 4 31B: 10–20 s per full answer; first token 0.4–2.0 s with thinking off. | `04_latency.py`; Streamlit footer timings |
| 5 | **Thinking mode: off by default.** Hosted: turning thinking off cut generation time about 3× with no measured accuracy loss on this set; `reasoning_effort` and a "keep it short" instruction had no effect. Laptop: the 4B thinking variant produced 15–18 k characters of reasoning per question. | `04_latency.py`, hosted; laptop logs |
| 6 | **Prompt changes are not free.** A second prompt version (`answer_v2`: "write the first-offence amount first") removed a meaningless closing sentence (11/20 → 3/20) but made the 8B model invent an amount on q1 when the amount was not in the chunks; kept `answer_v1`. Citation style drifted to internal labels ("Parça N") in 5/20 hosted answers and 5–8/20 laptop answers; fixed in the prompt for the hosted run, still open on the laptop. | Graded runs v1 vs v2 |
| 7 | **Memory fits on a 16 GB host.** Resident at once: Qwen3 4B (about 3 GB with context) + 0.6B embedding (0.7 GB) + 0.6B reranker in bf16 (1.3 GB) + Python, index and UI (about 1 GB) ≈ 6 GB. The 8B answer model adds about 2.5 GB and halves generation speed. | Ollama and process memory on the laptop |
| 8 | **Hosted cost is small, availability is the risk.** The national platform used in the spike is free until 01/11/2026 (pricing after that not published; starting balance 1,010 credits). A commercial OpenAI-compatible provider with the same three open-weight models prices them at about $0.10 / 1M tokens (embedding 8B), $0.20 / 1M (reranker 8B) and $0.14 in / $0.40 out per 1M (Gemma 4 31B); the whole 20-question evaluation costs under $0.10, a semester of runs $10–20. Switching provider is a change of base URL, key and the rerank request format (about 15 lines). | Provider price lists, 22/10/2026; token counts from the hosted run (about 3,700 tokens per question with Gemma) |

Summary table, same 20 questions:

| Configuration | Retrieval hit@5 (dense / +rerank) | Correct answers | Fabrications | Time per answer |
|---|---|---|---|---|
| Laptop · Qwen3 4B instruct, thinking off | 17/20 / 20/20 | 13/20 | 2 | ≈ 1.5 min retrieval + 3 min answer |
| Laptop · Qwen3 4B, thinking on | same retrieval | 4/5 (stopped) | 0 | ≈ 24 min |
| Laptop · Qwen3 8B, thinking off | same retrieval | 19/20 | 0 | ≈ 1.5 min retrieval + 4–5 min answer |
| Hosted · Gemma 4 31B, thinking off | 20/20 / 20/20 | 20/20 | 0 | 10–20 s |
| Hosted · DeepSeek V4.1 Flash | 20/20 / 20/20 | 16/20 produced, 0 errors | 0 | similar; reasoning budget exhausted on 4 |

## What this means for the project

- **D1 stands, with its cost made explicit.** The laptop variant meets the "nothing leaves the machine" goal and reaches the same retrieval quality; what it gives up is speed (minutes instead of seconds) and some answer accuracy at 4B. The charter's original "answer under 2 s" target is not reachable on CPU with a reranker; the revised targets (retrieval < 2 s, first token < 3 s, full answer < 30 s) hold only for the hosted option. For the laptop variant the targets must be restated from measurements (D2, section 5 Evaluation).
- **The reranker is the lever.** It is both the reason retrieval reaches 20/20 and 95 % of laptop retrieval time. Sprint 2 experiments should try k = 10 candidates (halves rerank time, risk of missing the article not observed in 20 questions), the Arc iGPU for the reranker (D6), and running the reranker on the one laptop with an RTX 3050 — each changes the "single host" picture and must be recorded as a decision if adopted.
- **Model size on the laptop is a decision to make, not to assume.** 8B gives 19/20 at twice the answer time of 4B (13/20). The design document names 4B (D5); the evidence favours 8B if 16 GB RAM allows it alongside the other models — to be measured on the host laptop (D2), since the spike ran on a 32 GB machine.
- **A hybrid is possible but is a different variant.** Keeping index and UI local and calling only the LLM (or only the reranker) on a hosted API gives most of the speed; it ends the "no data leaves the machine" claim, since the question and the retrieved articles go out. If the team wants it, it goes into the design document as its own option in D1 with that consequence stated, not as a silent change.
- **Evaluation design is confirmed.** Retrieval metrics without a judge (hit@5, P/R@k, MRR) separated the two variants cleanly; manual grading caught fabrications that citation checks alone would miss. The citation metric should check the cited document, not only the article number (finding 6).

## Open questions

- Laptop 8B with thinking on: not measured (estimated 15–20 min per answer).
- Hosted dense-only vs reranked on harder questions: identical on these 20 easy questions; the extended question set (EN-02) is needed to see the reranker's real contribution.
- Price of the national platform after 01/11/2026; whether the $100 Google Cloud credits can host an open-weight model instead (A variant, not measured).
- Behaviour of all configurations on the out-of-scope and injection questions that the query guard (D10) will need.

## References

1. Spike 01: RAG or a long-context model — `docs/spikes/01-rag-or-long-context.md`.
2. System Architecture Design Document, decisions D1, D2, D5, D6, D8 — `Markdown Template/11-system-architecture-design-document.md`.
