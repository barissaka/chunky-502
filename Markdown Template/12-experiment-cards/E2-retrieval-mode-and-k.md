# E2: Retrieval mode (dense vs. hybrid) and number of retrieved articles (k)

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
Does adding bge-m3's sparse (lexical) score to the dense score improve retrieval of the supporting articles, and how many articles (k) should be passed to the generator? Compared against dense-only retrieval with the same embedding model and index. The result sets the retrieval parameters of the baseline [E1](E1-baseline.md).

**Setup:**
<!--
Links only:
- The public W&B sweep or project. W&B records every combination you tested, including the fixed parameters.
- The evaluation set version.
- The prompt files. To change a prompt, add a new file to prompts/ instead of editing the old one.
-->
- W&B: not logged in Sprint 2. Results: cells 5 and 6 of [`notebooks/04_index_check.ipynb`](../../notebooks/04_index_check.ipynb).
- Evaluation set: [`docs/eval/trial_in_scope_10.csv`](../../docs/eval/trial_in_scope_10.csv) (10 in-scope questions, 23 supporting articles). These questions are the development set: retrieval parameters are tuned on them, and they are not counted in the final test score. They were selected from the 40 questions of D2 v1; the formal test runs use the other questions of D2 and 10 new questions added in their place, none of which is used for tuning.
- Prompt: none (retrieval only).

**Design:**
<!-- The parameter space you tested. Add one row for each parameter you varied. For the baseline, give the single value each main parameter had. Then give the search method (grid, random or Bayesian) and the number of runs. -->

| Parameter | Values or range tested | Best value |
|---|---|---|
| Retrieval score | dense only (`sparse_weight` = 0); hybrid (`sparse_weight` = 0.3) | hybrid |
| `top_k` | 5, 8, 10 (dense only at 5) | 8 |

Fixed: `BAAI/bge-m3` (same revision as E1), numpy index of 472 chunks, no reranker. The sparse weight 0.3 is a starting value and was not tuned.

**Search method and runs:** Grid over the combinations above, 4 runs (dense k = 5; hybrid k = 5, 8, 10). Retrieval is deterministic, so each combination was run once.

**Summary of Results:**
<!-- The main scores go in the results table of the technical summary. Put the breakdown here: scores by question type, and failures by cause. -->

| Combination | Recall@k (hit rate) | Article recall@k (mean over questions) | Articles found (total of 23) | MRR@k | Context tokens to the LLM (median / max) |
|---|---|---|---|---|---|
| Dense, k = 5 | 0.90 | 0.67 | 14 / 23 | 0.68 | — |
| Hybrid, k = 5 | 1.00 | 0.79 | 16 / 23 | 0.76 | 3,635 / 9,613 |
| **Hybrid, k = 8** | **1.00** | **0.92** | **20 / 23** | **0.76** | 4,911 / 11,633 |
| Hybrid, k = 10 | 1.00 | 0.92 | 20 / 23 | 0.76 | 5,514 / 12,902 |

Hybrid retrieval found the expected article where dense retrieval missed it in S09 (MUAYENE-m8), S13 (SKUTER-m4) and S28 (SKUTER-m5); dense retrieval found one article that hybrid ranked lower at k = 5 (KTK-m45 in S20). Breakdown by question type for the best combination: see E1.

| Failure cause (hybrid, k = 8) | Count | % of failures |
|---|---|---|
| Supporting article not named in the question; relevant only as a consequence of another rule (KTK-m36) | 2 | 67% |
| Vehicle-type speed table not retrieved (KTY-m100) | 1 | 33% |

**Discussion and Conclusion:**
<!-- What the numbers mean and what you will do next. Link the decision they led to (D?), if any. -->
Hybrid retrieval beats dense-only retrieval at k = 5 with a sparse weight of 0.3; dense-only retrieval was not run at k = 8 or 10, so part of the gain from k = 5 to k = 8 may come from the larger k alone, and the comparison does not show that hybrid is better at k = 8. The sparse score helps where the question shares exact terms with the article (inspection fee, e-scooter definitions, sidewalk riding), and costs nothing extra because bge-m3 produces both vectors in one pass. Raising k from 5 to 8 adds four supporting articles for about 1,300 more context tokens at the median; k = 10 adds none. Hybrid retrieval with k = 8 is used in the baseline (E1) and in `config/rag.yaml`. The result rests on 10 questions; the sparse weight and k are tuned again in the Sprint 3 retrieval spike, on the development set only. These are development scores, not a check of the Objective 2 target. Decision: AD-04 in the design document.