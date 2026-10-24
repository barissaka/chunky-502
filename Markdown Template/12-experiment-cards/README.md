# Experiment Cards

One card per experiment, saved as `E<n>-<short-name>.md`. This page is the index: it is updated after every experiment and links to the card, which records the parameter space tested and the decision. Runs are tracked in W&B; the product configuration lives in `config/rag.yaml`.

| Card | Experiment | Sprint | Metrics | Runs | Decision | Status |
|---|---|---|---|---|---|---|
| [E1](E1-baseline.md) | Baseline — dense retrieval with Qwen3-Embedding | 2 | Precision@k, Recall@k, MRR | — | — | planned |
| [E2](E2-short-name.md) | Reranker on/off | 2 | Precision@k, Recall@k, MRR | — | — | planned |