# Sprint 2: Review Committee Technical Summary

**Note: this document uses HTML tags to disable rendering of instructions. View the raw file for further details.**

**Suggestion: You can use tools like [marp](https://github.com/marp-team/marp-cli) to convert this to a presentation for your end-of-sprint demo.**

<!--
- This is a document where you will summarize experiments ran this sprint, their metrics, and results. Experiments are recorded in detail in experiment cards in the Markdown Template/12-experiment-cards/ folder. You should only link the relevant experiment here and report it's main results in here.
- Keep the summary to two pages at most. Link to details rather than repeating them: config/rag.yaml holds only the product configuration, each experiment card records the parameter space it tested, the tested combinations are in W&B, and decisions are in the design document.
-->

| Team | Sprint | Last updated |
|---|---|---|
| Chunky | Sprint 2 | 2026-11-14 |

## 1. Summary

<!-- In 3 to 5 sentences: what you tried this sprint, the main result compared with the baseline and the target, and what you will do next. -->

This sprint we built the RAG baseline end to end: the six legal texts are extracted from Word, split into 472 article-level chunks, embedded locally with bge-m3 (dense and sparse vectors) and stored in a numpy index; the top 8 articles go to gpt-oss-120b on Vertex AI, which answers with article citations. On the 10 in-scope trial questions, every question gets at least one supporting article in the retrieved set (Recall@8 = 1.00, target ≥ 0.80), and 20 of the 23 supporting articles are retrieved (article recall@8 = 0.92). Hybrid retrieval beat dense-only retrieval (article recall@5 0.79 vs. 0.67), and k = 8 retrieved four more supporting articles than k = 5 (E2). The misses are articles that apply only as a consequence of another rule (chain questions). Next sprint: the retrieval spike (second embedding model, reranker) on the full in-scope set, cross-reference expansion for chain questions, and the out-of-scope refusal.

Against the long-context baseline (E3: Claude Sonnet 5.5 with all six texts in context, no retrieval), the RAG pipeline answers 5 of 10 in-scope questions correctly against 8 of 10. Since retrieval finds most supporting articles, most of this gap is in generation, mainly on chain questions.

**Decisions this sprint:** [AD-03](../11-system-architecture-design-document.md#ad-03-llm-access--hosted-model-on-google-cloud-vertex-ai-through-an-openai-compatible-gateway) (hosted LLM on Google Cloud Vertex AI; baseline generator gpt-oss-120b), [AD-04](../11-system-architecture-design-document.md#ad-04-embedding-model--bge-m3-for-the-baseline-final-choice-in-the-retrieval-spike) (bge-m3, hybrid retrieval), [AD-05](../11-system-architecture-design-document.md#ad-05-reranker--none-in-the-baseline-chosen-in-the-retrieval-spike) (no reranker in the baseline), [AD-06](../11-system-architecture-design-document.md#ad-06-vector-store--numpy-index-on-disk-qdrant-blocked-on-the-host-laptop) (numpy index instead of Qdrant), [AD-08](../11-system-architecture-design-document.md#ad-08-chunking--one-chunk-per-article-retrieval-only-sub-chunks-for-over-long-articles) (472 units, no sub-chunks), [AD-07](../11-system-architecture-design-document.md#ad-07-local-runtime--withdrawn-no-local-llm) (no local runtime), [AD-10](../11-system-architecture-design-document.md#ad-10-query-guard-and-pii-masking-before-retrieval) (simplified PII masking and rule-based guard, approved by the course assistant), [AD-12](../11-system-architecture-design-document.md#ad-12-evaluation--fully-automated-scored-against-the-d2-answer-key) (DeepEval GEval, Claude Opus 5.5 judge, threshold 0.7), [AD-13](../11-system-architecture-design-document.md#ad-13-baselines--default-state-people-and-long-context-system) (long-context baseline Claude Sonnet 5.5, E3), [AD-14](../11-system-architecture-design-document.md#ad-14-chat-ui--streamlit) (Streamlit).

## 2. Metrics

<!-- Fill this in during Sprint 2. Change it later only if a metric changes, and explain why in section 1. Take each target from the charter's success criteria. -->

| Metric | Why it fits | Target |
|---|---|---|
| Recall@k (hit rate): share of questions with at least one supporting article of the answer key in the top k | The generator can only cite what retrieval returns, so this bounds the share of answers with a supported article reference | ≥ 0.80 at the k used — derived from Objective 2 (≥ 80% of answers with a supported article reference); the charter sets no separate retrieval target |
| Article recall@k: share of the supporting articles of the answer key found in the top k | Many questions rest on two to four articles (chain and parallel questions); hit rate alone hides a missing second article | none (diagnostic) |
| MRR@k: mean reciprocal rank of the first supporting article | Shows whether the right article is ranked first; the measure a reranker should improve (AD-05) | none (diagnostic) |
| Judge score: mean `eval.py` judge score (0–1) of the in-scope answers against the answer key (AD-12) | Shows how close answers are to the answer key, not only pass or fail; an answer is counted correct at ≥ 0.7 | none (diagnostic) |
| Cited-article recall: share of the answer key's supporting articles that the answer cites | The answer-side counterpart of article recall@k: shows whether retrieved articles reach the answer | none (diagnostic) |

Answer correctness, supported article references in the answers, out-of-scope refusal and response time are reported with the RAG–long-context comparison.

## 3. Results

<!--
- Include the baseline, the best experiment from earlier sprints if it is not the baseline, and every experiment run this sprint. In the Sprint column, write the sprint each experiment ran in.
- Each row shows the experiment's best combination. Link that run in W&B.
- Run every row on the same evaluation set. If the set changes, run the baseline and the earlier best again on the new set.
- Run the best combination again n times with different seeds. Report each score as the mean ± std over those repeats, and bold the best value in each column.
- Write "null" for missing or failed outputs, and explain it under the table. Do not record them as 0.
- Leave out deprecated experiments.
- In Sprint 4, add a row for the product configuration in config/rag.yaml.
-->

**Evaluation set:** `docs/eval/trial_in_scope_10.csv` (the 10 in-scope questions of the trial set; 23 supporting articles)

| Experiment | Sprint | Best run (W&B) | Recall@8 (hit rate) | Article recall@8 | MRR@8 | Repeats (n) |
|---|---|---|---|---|---|---|
| Target (charter) | — | — | ≥ 0.80 | — | — | — |
| [E1 RAG baseline](../12-experiment-cards/E1-baseline.md) (bge-m3 hybrid, k = 8, gpt-oss-120b) | 2 | null | **1.00 ± 0.00** | **0.92 ± 0.00** | **0.76 ± 0.00** | 1 |
| [E2 Retrieval mode and k](../12-experiment-cards/E2-retrieval-mode-and-k.md) — best: hybrid, k = 8 | 2 | null | **1.00 ± 0.00** | **0.92 ± 0.00** | **0.76 ± 0.00** | 1 |
| [E3 Long-context baseline](../12-experiment-cards/E3-claude-longcontext-baseline.md) (claude-sonnet-5-5, all six texts in context, no retrieval) | 2 | null | null | null | null | 1 |

W&B was not set up in Sprint 2, so the run links are null; the run files are in `docs/eval/runs/` and the E2 results in `notebooks/04_index_check.ipynb`. Retrieval is deterministic, so one repeat gives std 0. E2's best combination is the configuration used in E1; its other combinations (dense k = 5: article recall@5 0.67; hybrid k = 5: 0.79; hybrid k = 10: 0.92) are in the card.

E3 has no retriever (the whole corpus, 447k tokens, is in the model's context), so the retrieval columns are null for it.

**RAG vs long-context baseline (answer quality, same 10 questions):**

| Experiment | Correct answers (judge ≥ 0.7) | Judge score | Answers naming a supporting article | Cited-article recall | Out-of-scope declined (of 10) | Median response time (s) | Repeats (n) |
|---|---|---|---|---|---|---|---|
| E1 RAG baseline (gpt-oss-120b) | 5 / 10 | 0.61 | **10 / 10** | 0.68 | null | 26.6 | 1 |
| E3 Long-context baseline (claude-sonnet-5-5) | **8 / 10** | **0.80** | **10 / 10** | **0.92** | 0 | **17.7** | 1 |

Correctness is scored with the team's `eval.py` (judge `claude-opus-5-5`, DeepEval GEval, AD-12) against the gold answers; one run each, so no std. E1's out-of-scope questions were not run. E3 declines 0 of 10 out-of-scope questions under the team's rule (decline only, no related provisions or referral): every answer says the topic is not covered but then adds related provisions. E1's response time is the card's median; the `latency_s` values in E1's `_eval.jsonl` give a median of 18.1 s, to be reconciled. Two limits: E3's in-scope answers were judged before one rubric step was added (D32 in the Q&A Data Report), and the judge is a Claude model, as is E3's generator.

**Best configuration:** <!-- From Sprint 3 on. Link its W&B run, and say whether config/rag.yaml now uses it. -->

## 4. User story test results

<!-- From Sprint 3 on. Add one row for each user story you have built. The tests themselves are in the story requirements. -->

| Story | Result | Note |
|---|---|---|
| US-01 Ask in my own words ([CHUNKY-124](https://chunky-502.atlassian.net/browse/CHUNKY-124)) | fail (2 of 4 tests pass, 1 accepted for Sprint 2) | Tested on the pipeline from `notebooks/05_answer_check.ipynb`, because there is no web page yet. **TC-01-1 pass:** "Hız limitini aşarsam ne kadar ceza öderim?" is answered in Turkish with the penalty bands of KTK Art. 51 (8.3 s). **TC-01-2 pass:** "kırmızı ışıkta geçtim" is answered with the sanctions of KTK Art. 47 for traffic lights (7.1 s); the amounts are to be confirmed by the Domain Expert in the everyday-wording test (CHUNKY-164). **TC-01-3 accepted for Sprint 2:** a failed model call stops with a Python error instead of hanging; the Turkish error message comes with the Streamlit page in Sprint 3. **TC-01-4 fail:** an empty question is still passed to retrieval and the LLM; the model replies "Lütfen bir soru sorun", but the rule-based check that stops the message before it is sent (AD-10) is not built yet. |
| US-09 Use the assistant in a web interface ([CHUNKY-125](https://chunky-502.atlassian.net/browse/CHUNKY-125)) | not tested | Only a UI mock-up exists (`docs/images/ui-mockup-v1.png`); no page is connected to the pipeline yet, so TC-09-1 and TC-09-2 could not be run. The Streamlit page (AD-14) is built in Sprint 3. |

## Checklist before submitting

- [x] The summary is two pages or shorter.
- [ ] Every row in Results links to an experiment card. Every card from this sprint either has a row or is marked deprecated. <!-- Open: the row for E3 (long-context baseline) is added with the RAG–long-context comparison. -->
- [x] Every decision in section 1 has a record in the design document.