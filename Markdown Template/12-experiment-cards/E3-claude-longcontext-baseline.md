# E3: Baseline — Claude with all six texts in context (no retrieval)

**Note: this document uses HTML tags to disable rendering of instructions. View the raw file for further details.**

<!--
- Save one card per experiment as E<n>-<short-name>.md.
- Runs with the same setup count as one experiment.
- Never move or delete a card. When a later experiment supersedes it, change its status to deprecated.
-->

| Date | Author(s) | Status |
|---|---|---|
| 2026-11-13 | Ekin | completed |

**Aim:**
<!-- The question you want to answer, and what you compare against: the baseline or another configuration. -->
How well does a strong general LLM answer the gold questions when it is given all six legal texts in its context, with no retrieval step? This is the reference point for the RAG pipeline: it shows the answer quality, citation accuracy and refusal behaviour reachable when retrieval loses nothing. Later RAG configurations are compared against it on the 10 in scope records.

**Setup:**
<!--
Links only:
- The public W&B sweep or project. W&B records every combination you tested, including the fixed parameters.
- The evaluation set version.
- The prompt files. To change a prompt, add a new file to prompts/ instead of editing the old one.
-->
- W&B: not used; run metadata and scores are kept as files (`run1/`)
- Evaluation set: Traffic-Law RAG Q&A Gold Set v1.4, Baseline v1 subset (datasheet D26) — `trial_full_20.json`. v1.5 later rewrote the expected behaviour of K01 and K09 (D33); the scores here already follow it
- Prompt: `prompts/baseline_v1_system.txt`
- Judge scores: `run1/scores.csv` (all 20 records with the judge's score and reason; summary in `run1/scores_summary.json`). Built from `run1/scores_judge.csv` (in-scope rows) and `run1/scores_judge_oos.csv` (K01–K10, corrected rubric, D31); the out-of-scope rows of `scores_judge.csv` come from the first, incorrect rubric and are not used
- Code: `run.py`, `eval.py`; run metadata: `run1/results.meta.json` (started 2026-11-13 17:40:25, prompt sha256 3fa9a2e92d35f0e7, questions sha256 acc5a745001db394); answers: `run1/results.jsonl`

**Design:**
<!-- The parameter space you tested. Add one row for each parameter you varied. For the baseline, give the single value each main parameter had. Then give the search method (grid, random or Bayesian) and the number of runs. -->

| Parameter | Values or range tested | Best value |
|---|---|---|
| Generator model | claude-sonnet-5-5 (Anthropic API) | claude-sonnet-5-5 |
| Retrieval | None: all six texts in context (447,423 tokens with the system prompt, measured with `run.py --count-only`) | — |
| Corpus | Six cleaned texts as supplied, no paragraph numbers added (D29) | — |
| System prompt | baseline_v1_system (answer only from the texts, [KOD m.X/Y] citations, explicit "not covered", JSON output) | baseline_v1_system |
| Sampling | Model defaults (non-default temperature is rejected by the model) | — |
| max_tokens | 16,000 | — |
| Questions | 20: S01, S03, S09, S13, S14, S15, S20, S23, S25, S28 + K01–K10 | — |
| Runs per question | 1 (budget: prepaid API credits, D30) | — |
| Judge | claude-opus-5-5 via DeepEval GEval (correctness against gold_answer; out-of-scope rubric), run after the generation run; pass threshold 0.7. No manual scores (D35) | — |
| Citation scoring | Article level primary, paragraph level secondary (D28) | — |

**Search method and runs:**
No search: a single configuration. 20 questions × 1 run = 20 generator calls (plus a 2-question cache test) and 20 judge calls (plus a 1-question judge test). The corpus was read from the prompt cache on every call (447,419 cached tokens per call); 1,054 uncached input and 28,431 output tokens in total. Cost about 2.1 USD for the run (about 3.3 USD with the cache test). Wall time 4 min 30 s; mean latency 13.5 s per question.

**Summary of Results:**
<!-- The main scores go in the results table of the technical summary. Put the breakdown here: scores by question type, and failures by cause. -->

Scores by question type (in-scope, 1 run). Judge score: GEval 0–1 against the gold answer; pass at 0.7 or above. Paragraph matching ignores notation (5/1-a/4 = 5/1-a-4) and counts a parent or child unit as a match (9/2-c = 9/2-c-1).

| Type | n | Judge score | Judge pass | Article P | Article R | Article F1 | Paragraph R |
|---|---|---|---|---|---|---|---|
| Single article | 2 | 0.85 | 2 / 2 | 0.63 | 1.00 | 0.70 | 0.75 |
| Several articles of one text | 3 | 0.90 | 3 / 3 | 0.34 | 1.00 | 0.50 | 1.00 |
| Articles of several texts | 2 | 0.65 | 1 / 2 | 1.00 | 0.83 | 0.90 | 0.54 |
| Violation in the user's own words | 3 | 0.77 | 2 / 3 | 0.29 | 0.83 | 0.39 | 0.79 |
| **In-scope total** | 10 | **0.80** | **8 / 10** | **0.51** | **0.92** | **0.59** | **0.80** |

By hop type the judge scores Chain 0.68, Parallel 0.90, Single-hop 0.87. In no in-scope answer did the judge find an amount, period or rule that contradicts the gold answer; the two failures (S15, S25, both 0.5) are omissions. False refusals: 0 of 10. Format: 20 of 20 answers were valid JSON.

Out-of-scope (K01–K10), scored by the team's rule (D10, D28): an out-of-scope answer must say only that the topic is not in the texts and that no information can be given: no citations, no list of related provisions, no information on neighbouring topics, no advice or referral. Judge score with the corrected rubric (D31): **0.42**, 0 of 10 pass (range 0.2–0.5; lowest K03 0.2 and K02 0.3). In its reasons the judge notes, for every answer, that the topic is correctly stated as not covered and that no amount or channel was invented, and that each answer then adds related provisions; for K02, K06, K07 and K08 it also notes a referral. Automatic checks: the `in_scope` flag is false in 6 of 10 (true for K02–K05), every answer cites at least one article, so the strict refusal rate (flag false and no citations) is 0 of 10.

In-scope answers may point the user onward for a part the texts do not cover (D32); S09's "see the station's fee table" is therefore not a failure.

Article precision is low because the model cites more articles than the gold references list; whether those extra articles are relevant is not measured in this run.

Failures by cause (16 labels on 12 records; one record can carry two). In-scope causes are taken from the judge's reason for each answer below 0.7; out-of-scope causes come from the automatic checks (`in_scope` flag, citations):

| Failure cause | Count | % of failures |
|---|---|---|
| oos_cited_related | 10 | 63% |
| scope_flag_mismatch | 4 | 25% |
| missing_key_fact | 2 | 13% |
| wrong_fact, outside_knowledge, wrong_citation, missing_citation, assumed_ambiguity, conflict_not_shown, false_refusal, oos_fabricated, oos_not_refused, format_error | 0 | 0% |

The two missing_key_fact cases, as the judge describes them: S15 gives both provisions with sources but does not work out how they apply together and leaves out the overtaking exception; S25 makes no assumption about the vehicle but leaves out the 40 km/h and raised-limit cases and several general rules.

**Discussion and Conclusion:**
<!-- What the numbers mean and what you will do next. Link the decision they led to (D?), if any. -->
With all six texts in context, Claude Sonnet 5.5 answers the in-scope questions well (judge score 0.80, 8 of 10 pass, article recall 0.92), and the judge found no contradiction with the gold answers. Its weaknesses are completeness and form: it leaves out cases on long multi-case questions (S15, S25), cites more articles than the gold references (article precision 0.51), and on out-of-scope questions it does not stop at the refusal: all 10 answers add related provisions and some add referrals, which the team's rule does not allow (judge 0.42), and the `in_scope` flag is inconsistent (4 of 10). The baseline_v1 prompt only said "say it clearly" and did not forbid adding related content, which likely explains this.

Limits: one run only (no run-to-run spread); scores come from one LLM judge with no human check, and the judge is also a Claude model (possible family bias, though judge and generator are different models). Paragraph scores for KTK and KTY are held back by the missing paragraph numbers in these texts (D29). Decisions: D28, D30–D33, D35.
