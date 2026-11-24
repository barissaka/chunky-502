# RAG compared with the long-context baseline: 10 in-scope questions

The comparison covers the first RAG pipeline ([E1](../Markdown%20Template/12-experiment-cards/E1-baseline.md)) and the long-context baseline ([E3](../Markdown%20Template/12-experiment-cards/E3-claude-longcontext-baseline.md)) on the same 10 in-scope questions of the trial subset, scored by the same judge. All values are taken from the two experiment cards.

## 1. Compared systems

| | Long-context baseline (E3) | First RAG pipeline |
|---|---|---|
| Generation model | claude-sonnet-5-5 | openai/gpt-oss-120b-maas |
| Retrieval | None: all six texts in the context | Retrieval over the six texts, then generation |
| Prompt | baseline_v1_system | answer_v1 |
| Questions | 10 in-scope (S01, S03, S09, S13, S14, S15, S20, S23, S25, S28) | The same 10 |
| Runs per question | 1 | 1 |
| Judge | claude-opus-5-5, pass at 0.7 | claude-opus-5-5, pass at 0.7 |
| Citation level | Article (paragraph matching also computed) | Article |

## 2. Overall result

| Metric | RAG | Baseline (E3) | Difference |
|---|---|---|---|
| Judge score (mean, 0–1) | 0.61 | 0.80 | -0.19 |
| Judge pass (≥ 0.7) | 5 / 10 | 8 / 10 | -3 questions |
| Cited-article precision | 0.68 | 0.51 | +0.17 |
| Cited-article recall | 0.68 | 0.92 | -0.24 |
| Cited-article F1 | 0.62 | 0.59 | +0.03 |
| Median response time, in-scope (s) | 26.6 | 17.7 | +8.9 (RAG about 1.5 times the baseline) |

**Observations**

1. The baseline scores higher: judge 0.80 against 0.61, and 8 of 10 answers pass against 5 of 10.
2. Four of the five RAG passes (S03, S13, S23, S28) are exactly at the threshold of 0.70.
3. RAG cites fewer extra articles (cited-article precision 0.68 against 0.51) but reaches fewer of the needed ones (cited-article recall 0.68 against 0.92). F1 is about equal (0.62 against 0.59). The cited-article figures count the articles named in the answer; they are not the retrieval recall of section 3.
4. The median response time on the in-scope questions is 26.6 s for RAG and 17.7 s for the baseline; the RAG mean is 29.5 s and its p95 is 62.1 s, so at least one RAG answer took more than 60 seconds (E1). The baseline mean over all 20 questions is 13.5 s (E3).

## 3. Retrieval recall of the RAG pipeline

Recall@k counts a question as a hit when at least one supporting article is among the k retrieved chunks (glossary of the charter); article recall@k is the share of supporting articles retrieved.

| Measure | k = 5 | k = 8 |
|---|---|---|
| Recall@k (hit rate) | 1.00 | 1.00 |
| Article recall@k, macro (mean over questions) | 0.79 | 0.92 |
| Article recall@k, micro (supporting articles retrieved) | 16 / 23 | 20 / 23 |

**Observations**

1. Every question gets at least one supporting article at k = 5. Article recall rises from 0.79 to 0.92 (macro) when k goes from 5 to 8; 4 more of the 23 supporting articles are retrieved.
2. Both figures come from the same run (E1): article recall@8 (0.92) is higher than the cited-article recall of the answers (0.68), so part of the loss happens after retrieval, in the answer. E1 also records 4 cited articles that were not retrieved (S13, S25) and 2 citations that name the wrong article (S13, S20).

## 4. By question type

| Type | n | Judge RAG | Judge baseline | Difference | Cited-article recall RAG | Cited-article recall baseline | Difference |
|---|---|---|---|---|---|---|---|
| Single article | 2 | 0.75 | 0.85 | -0.10 | 1.00 | 1.00 | 0.00 |
| Several articles of one text | 3 | 0.53 | 0.90 | -0.37 | 0.44 | 1.00 | -0.56 |
| Articles of several texts | 2 | 0.55 | 0.65 | -0.10 | 0.58 | 0.83 | -0.25 |
| Violation in the user's own words | 3 | 0.63 | 0.77 | -0.14 | 0.75 | 0.83 | -0.08 |

**Observations**

1. The baseline has the higher judge score in all four question types.
2. The judge gap is largest for several articles of one text (-0.37), where RAG cited-article recall is also lowest (0.44 against 1.00), although retrieval found 0.89 of their supporting articles at k = 8 (E1).
3. The gap is smallest for single-article and several-texts questions (-0.10 each). For single-article questions cited-article recall is equal (1.00).

## 5. By hop type

| Hop type | n | Judge RAG | Judge baseline | Difference | Cited-article recall RAG | Cited-article recall baseline | Difference |
|---|---|---|---|---|---|---|---|
| Single-hop | 3 | 0.73 | 0.87 | -0.14 | 1.00 | 1.00 | 0.00 |
| Parallel | 3 | 0.67 | 0.90 | -0.23 | 0.67 | 1.00 | -0.33 |
| Chain | 4 | 0.47 | 0.68 | -0.21 | 0.44 | 0.79 | -0.35 |

**Observations**

1. Single-hop questions have equal cited-article recall (1.00 in both systems) and the smallest judge gap (-0.14).
2. Parallel and chain questions have cited-article recall gaps of -0.33 and -0.35 and judge gaps of -0.23 and -0.21.
3. Chain is the lowest hop type in both systems on the judge score (RAG 0.47, baseline 0.68).

## 6. Per question

| ID | Judge RAG | Judge baseline | Difference | Pass RAG | Pass baseline | Cited-article recall RAG | Cited-article recall baseline |
|---|---|---|---|---|---|---|---|
| S01 | 0.80 | 0.70 | +0.10 | yes | yes | 1.00 | 1.00 |
| S03 | 0.70 | 1.00 | -0.30 | yes | yes | 1.00 | 1.00 |
| S09 | 0.60 | 0.90 | -0.30 | no | yes | 0.50 | 1.00 |
| S13 | 0.70 | 0.90 | -0.20 | yes | yes | 0.50 | 1.00 |
| S14 | 0.30 | 0.90 | -0.60 | no | yes | 0.33 | 1.00 |
| S15 | 0.50 | 0.50 | 0.00 | no | no | 0.67 | 0.67 |
| S20 | 0.60 | 0.80 | -0.20 | no | yes | 0.50 | 1.00 |
| S23 | 0.70 | 0.90 | -0.20 | yes | yes | 1.00 | 1.00 |
| S25 | 0.50 | 0.50 | 0.00 | no | no | 0.25 | 0.50 |
| S28 | 0.70 | 0.90 | -0.20 | yes | yes | 1.00 | 1.00 |

Pass is derived from the judge score (≥ 0.7) and matches the pass counts in the source (5 and 8).

**Observations**

1. RAG is higher on 1 question (S01), equal on 2 (S15, S25) and lower on 7.
2. The largest drop is S14 (-0.60), where RAG cited-article recall is also low (0.33 against 1.00): the supporting article KTK-m36 was not retrieved (E1).
3. RAG cited-article recall is lower on 5 questions (S09, S13, S14, S20, S25), equal on 5 and higher on none.
4. On S03, S23 and S28 cited-article recall is 1.00 in both systems, yet the RAG judge score is lower (-0.30, -0.20, -0.20). The judge's reasons for these answers are in `tests/baseline/rag/scores_rag.csv`; E1 summarises only the answers below 0.7.
5. S15 and S25 score 0.50 in both systems.

## 7. Out-of-scope questions

The RAG pipeline was not run on the out-of-scope questions (K01–K10) in this comparison. In the baseline (E3), 0 of 10 pass under the strict refusal rule.

## 8. Conclusion

On the 10 in-scope questions the first RAG pipeline scores below the long-context baseline (judge 0.61 against 0.80, 5 of 10 passes against 8 of 10), and its median response time is about 1.5 times higher (26.6 s against 17.7 s). RAG cites fewer extra articles but reaches fewer of the needed ones, although its retrieval finds 20 of the 23 supporting articles at k = 8. The gap is widest for questions that need several articles and smallest for single-article and single-hop questions. Four of the five RAG passes sit exactly at the threshold of 0.70.

