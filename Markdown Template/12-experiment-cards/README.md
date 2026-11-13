# Experiment Cards

One card per experiment, saved as `E<n>-<short-name>.md`. This page is the index: it is updated after every experiment and links to the card, which records the parameter space tested and the decision. Runs are tracked in W&B; the product configuration lives in `config/rag.yaml`.

| Card | Experiment | Sprint | Metrics | Runs | Decision | Status |
|---|---|---|---|---|---|---|
| [E1](E1-baseline.md) | Baseline — dense retrieval with Qwen3-Embedding | 2 | Precision@k, Recall@k, MRR | — | — | planned |
| [E2](E2-short-name.md) | Reranker on/off | 2 | Precision@k, Recall@k, MRR | — | — | planned |
| [E3](E3-claude-longcontext-baseline.md) | Baseline — Claude Sonnet 5.5 with all six texts in context, no retrieval (reference for the RAG pipeline) | 2 | LLM-judge score (GEval), article P/R/F1, paragraph recall, out-of-scope refusal | 1 run × 20 questions | Kept as the no-retrieval reference; scored by LLM judge only (D35) | completed |