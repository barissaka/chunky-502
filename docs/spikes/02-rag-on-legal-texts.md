# Spike 02: Published examples of RAG on legal texts

**Project:** Traffic rules and penalties assistant · **Team:** Chunky · **Date:** 11/10/2026 · **Jira:** [CHUNKY-119](https://chunky-502.atlassian.net/browse/CHUNKY-119) · **Prepared by:** Team Chunky

## Question

What have others built and measured for question answering over legislation, in Turkish where possible, and what does it tell the team about chunking, retrieval, evaluation, the baseline and hardware?

## Findings

Studies [1]–[6] are published papers or theses. Projects [7]–[10] are personal repositories that have not been reviewed; their numbers are the authors' own, measured on their own question sets, and were read on 11/10/2026. No study or project on Turkish traffic legislation was found in this search.

| # | Source | What it is | Result that matters for the project |
|---|---|---|---|
| 1 | Louis et al. [1] | Answers to citizens' questions on Belgian statutory law, in French: 1,868 questions, 27,942 articles, retrieve-then-read | Recall at 5 articles was 17.4 for BM25 and 48.6 for a retriever fine-tuned on the task: on average fewer than half of the relevant articles were in the top five. The generated answers contained invented facts and sources. |
| 2 | Louis and Spanakis [2] | Article retrieval for 1,100+ legal questions over 22,600+ Belgian law articles | Fine-tuned dense retrieval performed best; the best baseline reached 74.8% recall at 100 articles. |
| 3 | Magesh et al. [3] | Test of commercial legal research tools built on RAG, with over 200 queries | Each tool hallucinated on more than 17% of the queries. An answer counts as hallucinated when it is incorrect or when the cited source does not support it. |
| 4 | Köse et al. [4] | Seven stages of a RAG pipeline compared on Turkish text (Wikipedia and web text, not legal) | Accuracy 78.70% for the baseline pipeline, 85% with HyDE, 84.60% with cross-encoder reranking and context augmentation at lower cost. Stacking several generative steps lowered accuracy. |
| 5 | Erkan [5] | METU M.S. thesis: Turkish legal corpus of 23,035 court decisions and 9,277 legislative documents, with a RAG system | No embedding method performed best for every category of legal text and every task. |
| 6 | Pipitone and Houir Alami [6] | Benchmark for the retrieval step of legal RAG in English: 6,858 query-answer pairs | Scores retrieval on the exact passage, not the document, because short passages let the user check the citation. |
| 7 | TránsitoRAG [7] | Chatbot on Peru's traffic regulations in Spanish, run on one computer (qwen2.5:7b, bge-m3) | Hybrid search with rank fusion; answers cite the passage and page. On 25 questions (3 outside the documents): faithfulness 0.75, answer relevancy 0.67. The model runs on CPU and the first token is slow. |
| 8 | mevzuat-rag [8] | RAG over Turkish laws from mevzuat.gov.tr, one chunk per article | On 34 questions the correct article ranked first for 12 with hybrid search alone and for 32 after reranking, HyDE and parent-child chunks. Questions in everyday language scored lowest (MRR 0.26–0.45). |
| 9 | turkish-legal-retrieval [9] | Retrieval over 31,304 articles of 907 Turkish laws; 5,010 test pairs built from the laws' cross-references | Recall@10: BM25 0.139, BM25 with a Turkish stemmer 0.156, turkish-e5 0.154, both fused 0.183, and 0.195 when the name of the law is also prepended to each chunk. |
| 10 | Turkish-Legal-Question-Answering-RAG [10] | Course project: article-aware chunks, BM25 and dense search fused, reranker, Qwen2.5 7B | Run locally on a 12 GB GPU. Uses a public set of Turkish legal questions with gold articles (194 used). |

## What this means for the project

1. **Chunking.** One chunk per article is planned for D6. [8] chunks by article, [10] uses article-aware chunks, and [9] compares whole articles with other cuts. Prepending the name of the text to each chunk [9] and splitting long articles into parent and child chunks [8] are candidates for later experiments.
2. **Retrieval.** The four projects [7]–[10] all combine keyword search (BM25 or full-text) with dense search. A Turkish stemmer for the keyword side [9] and a reranker [4], [8] are the next candidates.
3. **Baseline from the literature.** BM25 is the retrieval baseline in [1], [2] and [9]. Proposal: D6 reports BM25 Recall@k next to the dense retriever, in addition to the long-context baseline of D5.
4. **Everyday wording is the hard case** [1], [8]. The question set (D2) draws on real user questions, which keeps this case in the test. Proposal: each question is tagged as everyday wording or legal wording so that results can be reported for both.
5. **Evaluation.** Objective 2 already separates a correct answer from a named article that supports the answer. This is the distinction made in [3] and the reason not to merge the two measures.
6. **Hardware.** [7] and [10] run a 7B model on one computer, on CPU with a slow first token or on a 12 GB GPU. This is input for C-07 and for risk R-10 (no open-weight model that runs on the team's hardware reaches the Objective 2 levels in Turkish).
7. **Risk basis.** [1] and [3] are the basis for the probability of an incorrect or unsupported answer; [7] states that its refusal of out-of-document questions is not yet enforced by a threshold, which is the situation of risk R-07.

## Open questions

1. Which embedding models are tested first? Candidates named in the sources: bge-m3 [7], [10], turkish-e5 [9]; Turkish legal embedding models were published in 2026 [11], and their licence and availability are not checked yet.
2. Can the public Turkish legal question set used in [10] supply questions for D2, or does it not cover traffic legislation?

## References

[1] A. Louis, G. van Dijck, and G. Spanakis, "Interpretable long-form legal question answering with retrieval-augmented large language models," in *Proc. AAAI Conf. Artificial Intelligence*, vol. 38, no. 20, 2024, pp. 22266–22275. doi: 10.1609/aaai.v38i20.30232

[2] A. Louis and G. Spanakis, "A statutory article retrieval dataset in French," in *Proc. 60th Annu. Meeting Assoc. Comput. Linguistics*, 2022, pp. 6789–6803. doi: 10.18653/v1/2022.acl-long.468

[3] V. Magesh, F. Surani, M. Dahl, M. Suzgun, C. D. Manning, and D. E. Ho, "Hallucination-free? Assessing the reliability of leading AI legal research tools," *J. Empirical Legal Stud.*, vol. 22, p. 216, 2025. Preprint: https://arxiv.org/abs/2405.20362

[4] S. K. Köse *et al.*, "RAGTurk: Best practices for retrieval augmented generation in Turkish," in *Proc. 2nd Workshop Natural Language Processing for Turkic Languages (SIGTURK 2026)*, 2026, pp. 179–196. doi: 10.18653/v1/2026.sigturk-1.15

[5] M. A. Erkan, "Turkish legal NLP: A comprehensive AI framework for legal document understanding, summarization, and retrieval-augmented generation," M.S. thesis, Middle East Technical University, Ankara, 2025. https://open.metu.edu.tr/handle/11511/115579

[6] N. Pipitone and G. Houir Alami, "LegalBench-RAG: A benchmark for retrieval-augmented generation in the legal domain," arXiv:2408.10343, 2024. https://arxiv.org/abs/2408.10343

[7] vorellana99, "pe-traffic-rules-rag-chatbot (TránsitoRAG)," GitHub repository. https://github.com/vorellana99/pe-traffic-rules-rag-chatbot

[8] berkaytaygurt, "mevzuat-rag," GitHub repository. https://github.com/berkaytaygurt/mevzuat-rag

[9] agirgol, "turkish-legal-retrieval," GitHub repository. https://github.com/agirgol/turkish-legal-retrieval

[10] BeratMert29, "Turkish-Legal-Question-Answering-RAG," GitHub repository. https://github.com/BeratMert29/Turkish-Legal-Question-Answering-RAG

[11] Ö. Uğur *et al.*, "Mecellem models: Turkish models trained from scratch and continually pre-trained for the legal domain," arXiv:2601.16018, 2026. https://arxiv.org/abs/2601.16018
