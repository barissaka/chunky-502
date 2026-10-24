# Spike 01: RAG or a long-context model

**Project:** Traffic rules and penalties assistant · **Team:** Chunky · **Date:** 11/10/2026 · **Jira:** [TEAM: issue key] · **Prepared by:** [TEAM: name]

## Question

At the Sprint 0 pitch (07/10/2026) the Project Review Committee asked why the assistant uses retrieval-augmented generation (RAG) [1] when a long-context (LC) model could read the whole document set in one prompt. This note records what published comparisons report and what the team will measure.

## Findings

| # | Finding | Source |
|---|---|---|
| 1 | When the documents fit the context window and cost is not limited, LC answers more questions correctly than RAG on average. Over nine datasets, Gemini-1.5-Pro scored 49.70 with LC and 37.33 with RAG. On 13,628 questions from 12 datasets, LC answered 56.3% correctly and RAG 49.0%. | [2], [3] |
| 2 | RAG costs less per question. For over 60% of the queries, RAG and LC gave the same prediction. Sending a query to LC only when the model judges the retrieved passages insufficient reduced cost by 65% (Gemini-1.5-Pro) and 39% (GPT-4O) with results close to LC. | [2] |
| 3 | The questions on which RAG fails fall into four types: questions that need several reasoning steps, general questions, long and complex questions, and questions that can only be answered from the whole text. | [2] |
| 4 | The result depends on the retrieval method, the model and the task. Summarisation-based retrieval performed comparably to LC, and chunk-based retrieval lagged behind. A benchmark with 2,326 test cases and 11 models found no single best choice. In a study with Llama2-70B and a 43B in-house model, a 4K-token window with retrieval performed comparably to a 16K-token window without it, and retrieval also improved the results of the larger windows. | [3], [4], [5] |
| 5 | A long input is not used evenly. Accuracy is highest when the relevant passage is at the beginning or the end of the input and falls when it is in the middle. A 2025 technical report on 18 models (not peer-reviewed) found that performance became less reliable as the input grew. The same holds inside RAG: as more passages are retrieved, output quality first rises and then falls. | [6], [7], [8] |

## What this means for the project

1. The literature does not support the statement that RAG answers more accurately than an LC model for a document set that fits the context window. The charter does not make that statement, and it should not be made in presentations.
2. The reasons for RAG in this project are the following.
   - RAG is the basic solution set by the Project Review Committee (C-04 in [Assumptions & Constraints](../Markdown%20Template/03-project-canvas/03-assumptions-and-constraints.md)).
   - Cost and time. An LC model receives all six texts with every question; RAG sends only the retrieved articles. The budget is $100 (C-09), and Objective 1 is measured in time.
   - The generation model of the assistant runs on the team's hardware (C-05). Whether the six texts fit its context window is assumption A-01, checked by 21/10/2026.
   - Article reference. The retrieved articles are the texts shown to the user as the quoted provision (Scope Definition, feature 2).
3. The comparison is measured, not assumed. The LC baseline (D5, 11/11/2026) and the RAG baseline (D6, 18/11/2026) run on the same 40 questions and report the same five measures in [Deliverables](../Markdown%20Template/03-project-canvas/05-deliverables.md): correct answers, supporting article named, out-of-scope questions declined, cost per question and response time.
4. Hypothesis to test with D5 and D6: the LC baseline has a share of correct answers equal to or higher than the RAG baseline, and the RAG baseline has a lower cost per question and a lower median response time.
5. Finding 1 is the basis for the probability of risk R-01 (the full document set fits the model, and the long-context baseline matches the assistant) in the Risks page.
6. Question set (D2): questions whose answer needs more than one article are tagged as a separate question type, because finding 3 predicts that RAG loses most on them.
7. The number of retrieved articles (k) is a parameter to test in D6; finding 5 shows that a larger k does not always give a better answer.

## Open questions

1. How many tokens do the six texts hold, and what is the context window of each candidate model? (A-01; D1; 21/10/2026)
2. Which LC model is used for D5, and what does one question cost with the full document set in the prompt? (C-09, A-06)

## References

[1] P. Lewis *et al.*, "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *Advances in Neural Information Processing Systems 33 (NeurIPS 2020)*, 2020. https://arxiv.org/abs/2005.11401

[2] Z. Li, C. Li, M. Zhang, Q. Mei, and M. Bendersky, "Retrieval augmented generation or long-context LLMs? A comprehensive study and hybrid approach," in *Proc. 2024 Conf. Empirical Methods in Natural Language Processing: Industry Track*, Nov. 2024, pp. 881–893. doi: 10.18653/v1/2024.emnlp-industry.66

[3] X. Li, Y. Cao, Y. Ma, and A. Sun, "Long context vs. RAG for LLMs: An evaluation and revisits," arXiv:2501.01880, 2025. https://arxiv.org/abs/2501.01880

[4] P. Xu *et al.*, "Retrieval meets long context large language models," in *Proc. Int. Conf. Learning Representations (ICLR)*, 2024. https://arxiv.org/abs/2310.03025

[5] K. Li *et al.*, "LaRA: Benchmarking retrieval-augmented generation and long-context LLMs – No silver bullet for LC or RAG routing," in *Proc. 42nd Int. Conf. Machine Learning (ICML)*, PMLR 267, 2025, pp. 36846–36867. https://proceedings.mlr.press/v267/li25dv.html

[6] N. F. Liu *et al.*, "Lost in the middle: How language models use long contexts," *Trans. Assoc. Comput. Linguistics*, vol. 12, pp. 157–173, 2024. doi: 10.1162/tacl_a_00638

[7] B. Jin, J. Yoon, J. Han, and S. O. Arik, "Long-context LLMs meet RAG: Overcoming challenges for long inputs in RAG," in *Proc. Int. Conf. Learning Representations (ICLR)*, 2025. https://arxiv.org/abs/2410.05983

[8] K. Hong, A. Troynikov, and J. Huber, "Context rot: How increasing input tokens impacts LLM performance," Chroma, technical report, Jul. 2025. https://www.trychroma.com/research/context-rot
