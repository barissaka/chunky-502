# Experiment Cards

One card per experiment, saved as `E<n>-<short-name>.md`. This page is the index: it is updated after every experiment and links to the card, which records the parameter space tested and the decision. Runs are tracked in W&B; the product configuration lives in `config/rag.yaml`.

| Card | Experiment | Sprint | Metrics | Runs | Decision | Status |
|---|---|---|---|---|---|---|
| [E1](E1-baseline.md) | RAG baseline — bge-m3 hybrid retrieval, top 8, numpy index, gpt-oss-120b on Vertex AI | 2 | Recall@k (hit rate), article recall@k, Precision@k, MRR | 1 | Baseline configuration in `config/rag.yaml`; AD-04, AD-05, AD-06, AD-08 | completed |
| [E2](E2-retrieval-mode-and-k.md) | Retrieval mode (dense vs. hybrid) and k (5, 8, 10) | 2 | Recall@k (hit rate), article recall@k, MRR | 4 | Hybrid retrieval, k = 8 (AD-04) | completed |
| [E3](E3-claude-longcontext-baseline.md) | Baseline — Claude Sonnet 5.5 with all six texts in context, no retrieval (reference for the RAG pipeline) | 2 | LLM-judge score (GEval), article P/R/F1, paragraph recall, out-of-scope refusal | 1 run × 20 questions | Kept as the no-retrieval reference; scored by LLM judge only (D35) | completed |
| — | Reranker on/off | 3 | Precision@k, Recall@k, MRR | — | — | planned (retrieval spike, Sprint 3) |