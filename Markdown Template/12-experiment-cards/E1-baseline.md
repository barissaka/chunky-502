# E1: RAG baseline — bge-m3 hybrid retrieval, top 8, gpt-oss-120b

**Note: this document uses HTML tags to disable rendering of instructions. View the raw file for further details.**

<!--
- Save one card per experiment as E<n>-<short-name>.md.
- Runs with the same setup count as one experiment.
- Never move or delete a card. When a later experiment supersedes it, change its status to deprecated.
-->

| Date | Author(s) | Status |
|---|---|---|
| 2026-11-14 | Özge Çalışkan | completed |

**Aim:**
<!-- The question you want to answer, and what you compare against: the baseline or another configuration. -->
Set up the most basic working RAG pipeline over the six legal texts and measure how well its retrieval finds the supporting articles of the in-scope trial questions. This is the reference that later retrieval experiments (embedding model, reranker, cross-reference expansion) are compared against. A generator was added so that the pipeline answers end to end; its scores are reported as secondary results. The comparison with the long-context baseline (E3) is reported separately.

**Setup:**
<!--
Links only:
- The public W&B sweep or project. W&B records every combination you tested, including the fixed parameters.
- The evaluation set version.
- The prompt files. To change a prompt, add a new file to prompts/ instead of editing the old one.
-->
- W&B: not logged in Sprint 2. Run files: [`docs/eval/runs/`](../../docs/eval/runs/) (`2026-11-14_trial10_gpt-oss-120b-maas.jsonl` with its `_summary.json`, `.xlsx` and `_eval.jsonl` for `eval.py`).
- Evaluation set: [`docs/eval/trial_in_scope_10.csv`](../../docs/eval/trial_in_scope_10.csv) — the 10 in-scope questions of the trial set (23 supporting articles in total). These questions are the development set: the pipeline is tuned on them, and they are not counted in the final test score. They were selected from the 40 questions of D2 v1; the formal test runs use the other questions of D2 and 10 new questions added in their place, none of which is used for tuning.
- Prompt: [`prompts/answer_v1.txt`](../../prompts/answer_v1.txt).
- Configuration: [`config/rag.yaml`](../../config/rag.yaml) as committed with this card; code: `src/chunky/index.py`, `src/chunky/answer.py`; checks: `notebooks/04_index_check.ipynb`, `notebooks/05_answer_check.ipynb`.

**Design:**
<!-- The parameter space you tested. Add one row for each parameter you varied. For the baseline, give the single value each main parameter had. Then give the search method (grid, random or Bayesian) and the number of runs. -->

| Parameter | Values or range tested | Best value |
|---|---|---|
| Chunking | one chunk per unit (article, annex, schedule); 472 units; no sub-chunks (largest unit 6,603 tokens < 8,192) | — |
| Embedding text | chunk `text` field as it is (amendment notes already moved to metadata) | — |
| Embedding model | `BAAI/bge-m3`, revision `5617a9f61b028005a4858fdac845db406aefb181`, FP32 on CPU, max 8,192 tokens | — |
| Vector store | numpy index on disk (`dense.npy`, `sparse.jsonl`, `chunks.jsonl`, `manifest.json`), exhaustive search | — |
| Retrieval score | hybrid: dense cosine + `sparse_weight` × sparse (lexical) match | — |
| `sparse_weight` | 0.3 | — |
| `top_k` | 8 | — |
| Reranker | none | — |
| Generator | `openai/gpt-oss-120b-maas` on Vertex AI (us-central1), temperature 0 | — |
| Prompt | `answer_v1` | — |

**Search method and runs:** Single configuration, no search. Retrieval is deterministic (same index, same query → same ranking), so one run is enough for the retrieval scores (std 0). Index build: 472 chunks in 347 s on the host laptop CPU.

**Summary of Results:**
<!-- The main scores go in the results table of the technical summary. Put the breakdown here: scores by question type, and failures by cause. -->

Retrieval, 10 questions (means over questions):

| Metric | @5 | @8 |
|---|---|---|
| Recall@k (hit rate: at least one supporting article retrieved) | 1.00 | 1.00 |
| Article recall@k (share of a question's supporting articles retrieved, mean over questions) | 0.79 | 0.92 |
| Supporting articles retrieved (total over the 10 questions) | 16 of 23 | 20 of 23 |
| Precision@k | 0.32 | 0.25 |
| MRR@k | 0.76 | 0.76 |

By question type (k = 8):

| Question tag | n | Recall@8 (hit) | Article recall@8 | MRR@8 |
|---|---|---|---|---|
| Single article | 2 | 1.00 | 1.00 | 0.75 |
| Several articles of one text | 3 | 1.00 | 0.89 | 0.58 |
| Articles of several texts | 2 | 1.00 | 1.00 | 1.00 |
| Violation in the user's own words | 3 | 1.00 | 0.83 | 0.78 |

| Hop type | n | Recall@8 (hit) | Article recall@8 | MRR@8 |
|---|---|---|---|---|
| Single-hop | 3 | 1.00 | 1.00 | 0.83 |
| Parallel | 3 | 1.00 | 1.00 | 0.36 |
| Chain | 4 | 1.00 | 0.79 | 1.00 |

Generation (secondary, one run): all 10 answers cite at least one supporting article; citation recall 0.73, citation precision 0.62; 4 invented citations (cited but not retrieved) in 2 answers (S13, S25); response time median 26.6 s, mean 29.5 s, p95 62.1 s (within the proposed 30 s median budget); mean tokens 7,816 in / 920 out per question. The answers vary between runs even at temperature 0 (gpt-oss-120b reasons before answering), so the generation scores need repeats before they are compared. Answer correctness is scored with the team's `eval.py` judge and reported with the RAG–long-context comparison.

Retrieval failures (supporting articles not in the top 8):

| Failure cause | Count | % of failures |
|---|---|---|
| Supporting article not named in the question; relevant only as a consequence of another rule (KTK-m36, driving while the licence is suspended; S14, S25) | 2 | 67% |
| Vehicle-type speed table not retrieved for a speed question without vehicle type (KTY-m100; S25) | 1 | 33% |

**Discussion and Conclusion:**
<!-- What the numbers mean and what you will do next. Link the decision they led to (D?), if any. -->
These are scores on the development set, not a check of the Objective 2 target. Every question gets at least one supporting article in the top 5, and 20 of the 23 supporting articles are in the top 8, so retrieval is not the main limit for single-article questions. The misses are in chain questions: the penalty for driving while the licence is suspended (KTK-m36) is never retrieved, because the questions describe the situation (a licence already taken away) rather than the rule, and the article shares few terms with them. Precision@8 is low by design (most questions have one or two supporting articles), which is acceptable because the generator receives whole articles and the context stays small (median about 5k tokens at k = 8). The low MRR for parallel questions shows that the first supporting article is often not ranked first, which a reranker may improve. Next (Sprint 3): retrieval spike with a second embedding model and a reranker (AD-04, AD-05), and one-step cross-reference expansion for chain questions. Decisions: AD-04, AD-05, AD-06, AD-08 in the design document; the choice of hybrid retrieval and k = 8 comes from [E2](E2-retrieval-mode-and-k.md).

**Answer correctness (`eval.py` LLM judge, added 2026-11-14):**
<!-- Added after the run; the sections above are unchanged. -->

The 10 answers of this run (`2026-11-14_trial10_gpt-oss-120b-maas_eval.jsonl`) scored with the team's `eval.py`: judge `claude-opus-5-5` via DeepEval GEval against the gold answers, current correctness rubric, pass at 0.7 or above, one run. Results: [`tests/baseline/rag/scores_rag.csv`](../../tests/baseline/rag/scores_rag.csv) (score and reason per answer) and [`scores_rag_summary.json`](../../tests/baseline/rag/scores_rag_summary.json).

| Metric | Value |
|---|---|
| Judge score (mean) | 0.61 |
| Judge pass (≥ 0.7) | 5 of 10 (S01, S03, S13, S23, S28) |
| Cited-article precision (`eval.py`, mean over questions) | 0.68 |
| Cited-article recall (`eval.py`, mean over questions) | 0.68 |
| Cited-article F1 (`eval.py`, mean over questions) | 0.62 |

The cited-article figures are computed by `eval.py` (citations normalised to text and article, averaged over questions) and are not the same calculation as the citation recall and precision in the generation paragraph above.

| Question tag | n | Judge score | Judge pass |
|---|---|---|---|
| Single article | 2 | 0.75 | 2 / 2 |
| Several articles of one text | 3 | 0.53 | 1 / 3 |
| Articles of several texts | 2 | 0.55 | 0 / 2 |
| Violation in the user's own words | 3 | 0.63 | 2 / 3 |

| Hop type | n | Judge score | Judge pass |
|---|---|---|---|
| Single-hop | 3 | 0.73 | 3 / 3 |
| Parallel | 3 | 0.67 | 2 / 3 |
| Chain | 4 | 0.47 | 0 / 4 |

Answers below 0.7, as the judge describes them:

| ID | Judge score | Judge's main point |
|---|---|---|
| S14 | 0.3 | Treats driving during the suspension as a repeat alcohol offence instead of the 200,000 TL fine of KTK m.36/3, and adds a 75-penalty-point condition the texts do not support |
| S15 | 0.5 | Does not work out how the 10% tolerance and the KTK fine bands combine; leaves out the overtaking exception |
| S25 | 0.5 | Gives only the 50 km/h case and a general method, not the other speed limits or the general rules |
| S09 | 0.6 | States that any accident makes a special inspection mandatory; the rule applies only when the traffic police deem it necessary |
| S20 | 0.6 | Leaves out the three-year, six-monthly neurology condition and the referral route |

All four Chain questions fall below 0.7, in line with the retrieval misses on chain questions above (KTK-m36 not retrieved for S14 and S25). Two citations name a different article from the one whose content they support: S13 cites SKUTER-m10 for the geofencing rule (SKUTER m.16/10) and S20 cites KTK-m90 for the temporary withdrawal (KTY m.90).