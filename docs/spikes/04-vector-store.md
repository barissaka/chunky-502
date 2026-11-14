# Spike 04: Vector store — Chroma, FAISS or Qdrant (literature review)

**Project:** Traffic rules and penalties assistant · **Team:** Chunky · **Date:** 28/10/2026 · **Time box:** 3 hours (reading only) · **Decision served:** [AD-06 Vector store](../../Markdown%20Template/11-system-architecture-design-document-local.md#ad-06-vector-store--to-be-chosen-among-chroma-faiss-and-qdrant) (needed by 11/11/2026) · **Jira:** [CHUNKY-172](https://chunky-502.atlassian.net/browse/CHUNKY-172) "Create the embeddings and build the vector index" (depends on this decision); related [CHUNKY-171](https://chunky-502.atlassian.net/browse/CHUNKY-171) · **Prepared by:** Barış Saka

## Question

AD-06 leaves the vector store open among Chroma, FAISS and Qdrant. This note is a literature review: it records what the three tools' documentation says, measured against the project's own requirements, and states the expected finding. It does not include a hands-on test; verifying the expected finding on the host laptop is outside the scope of this note.

## Terms used in this note

- **Vector store.** The component that holds the 638 article chunks together with their vectors and metadata (document name, article number, page) and returns the chunks closest to a question. The two prototypes measured in [Spike 03](03-laptop-vs-hosted-models.md) kept the vectors in a plain in-memory matrix and compared them by cosine similarity, with no store; AD-06 decides which dedicated store the assistant uses instead.
- **Dense retrieval.** Finding chunks by meaning: the question and every chunk are turned into vectors by the embedding model and compared. This is what the assistant does today. It matches "kırmızıda geçtim" to the article on traffic lights even though the words differ.
- **Keyword retrieval (BM25).** Finding chunks by the words they contain, weighted by how rare each word is in the corpus. It is strong on exact strings — article numbers, fine amounts, legal terms — that dense retrieval sometimes misses.
- **Hybrid retrieval.** Running both searches and merging the two ranked lists (usually by reciprocal rank fusion, RRF, which combines by rank position rather than by score).
- **Local mode.** Qdrant run inside the Python process, storing data in a local folder, with no server to install or run. Chroma's persistent client works the same way.

## Working assumption

The embedding, reranking and answer models run on a team laptop. This matters here because Spike 03 showed that retrieval misses come from the small embedding model that fits on a laptop (finding 7).

## Requirements the store must meet

The criteria come from the user stories and constraints, not from the tools' feature lists.

| # | Requirement | Where it comes from |
|---|---|---|
| R1 | Return, with each chunk, the document name and article number (needed for the citation) | [US-02](https://chunky-502.atlassian.net/browse/CHUNKY-129) Get a correct answer with its sources |
| R2 | Restrict a query to one document, or exclude a document | US-02 (answers that span several texts); [US-05](https://chunky-502.atlassian.net/browse/CHUNKY-138) Know what the assistant covers ("shall not use any text that is not listed") |
| R3 | Delete one document and re-index it when a consolidated text is replaced, without rebuilding the rest | US-05 ("use the new version for answers after the next deployment") |
| R4 | Persist the index on disk so the demo laptop does not re-embed at start-up | Objective 1 (response time); demo |
| R5 | Return a similarity score, used by the query guard for the out-of-scope decision | [US-06](https://chunky-502.atlassian.net/browse/CHUNKY-130) Decline when the assistant does not know; AD-10 Query guard |
| R6 | Run in-process on a Windows laptop with 16 GB RAM, installed by `pip`, no server | C-05 (team hardware); AD-02 (single host) |
| R7 | Support hybrid retrieval (dense + BM25) as an experiment | Instructor feedback, Sprint 1 progress review, 21/10/2026: tag each chunk with its source law and key terms and combine keyword search with vector search — "easier and better", and "a very good test as well". Spike 03: retrieval misses track the embedding model size, so a second, keyword-based signal is the cheapest way to cover them on a laptop |
| R8 | Store no personal data; query text and query vectors must not be persisted | [US-08](https://chunky-502.atlassian.net/browse/CHUNKY-132) Keep my personal data private; C-03 |

Search speed is not a criterion: with 638 vectors an exact (flat) search in any of the three tools, or in numpy, takes milliseconds [6].

## Findings

| # | Finding | Source |
|---|---|---|
| 1 | The three candidates are not the same kind of tool. FAISS is a library: it searches vectors and nothing else; ids, metadata, filtering and persistence are left to the caller (`IndexIDMap` for custom int64 ids, `write_index` / `read_index` for saving, `remove_ids` whose support depends on the index type). Chroma and Qdrant are databases: vectors, metadata, filters and persistence in one package. | [5], [6] |
| 2 | Chroma: metadata filters (`where`) with `$eq`, `$ne`, `$gt`, `$lt`, `$in`, `$and`, `$or`; document-text filters (`where_document`) with `$contains` and `$regex`; `delete` by ids or by a `where` filter, which removes every matching item; results can include distances. The persistent client runs in-process and uses SQLite by default. | [1], [2], [7] |
| 3 | Chroma has added sparse-vector (BM25, SPLADE) and hybrid search (RRF) through a new `Search()` API. The documentation places it under the Cloud search API; whether the open-source persistent client supports it is not stated. | [3] |
| 4 | Qdrant local mode (`QdrantClient(path=...)`) runs without a server, persists to a local directory. The client's own README describes it as "useful for development, prototyping and testing" and advises switching to server mode "when you need to scale"; the LangChain documentation describes it as suited to testing and to "storing just a small amount of vectors". Payload (metadata) filtering is a core feature. Hybrid search is built in: sparse named vectors, `Prefetch` per vector, fusion by RRF or DBSF; server-side BM25 vectors need v1.15.3 or later. The LangChain examples run sparse and hybrid retrieval against a local `path=` store. | [4], [8], [9], [10] |
| 5 | FAISS has no metadata filtering and no keyword search; hybrid retrieval would mean a second BM25 index and a hand-written fusion step. | [5], [6] |
| 6 | A comparable case: a Microsoft ADR for an offline, in-process RAG on constrained hardware compared the same three tools and chose Chroma for its small footprint and easy deployment; FAISS was rejected for in-memory-only operation (no persistence of its own) and Qdrant for the engineering cost of its server mode. Qdrant's local mode was not part of that comparison. | [7] |
| 7 | From the team's own spikes: with the laptop embedding model, dense-only retrieval placed the expected article in the top 5 for 17 of 20 questions; the reranker recovered the other 3 but costs 80–90 s per question on the CPU. With the hosted embedding model the same set scored 20/20 without the reranker. | [Spike 03](03-laptop-vs-hosted-models.md), findings 1–2 |

## What this means for the project

1. **FAISS is not selected.** It satisfies R4, R5 and R6 but not R1–R3 or R7 on its own. Everything the team would have to write around it (an id-to-metadata table, per-document delete, a separate BM25 index, a fusion step) is what a plain in-memory matrix, as in the Spike 03 prototypes, also lacks; FAISS would add fast search, which 638 vectors do not need, and leave the rest to the team. AD-06 lists it as a candidate; this note records why it is not chosen.
2. **The choice is between Chroma and Qdrant local mode.** Both are documented to meet R1–R6 and R8. They differ on R7:
   - Qdrant: hybrid retrieval is built in and shown working in local mode (finding 4).
   - Chroma: hybrid retrieval is new and its availability in the open-source client is unconfirmed (finding 3).
3. **Qdrant is the expected choice.** Finding 7 shows that on the team laptop retrieval misses occur and the reranker that recovers them is expensive; a keyword signal is the cheapest way to cover those misses, which is what the instructor suggested on 21/10/2026. Chroma's remaining advantage — a smaller dependency — carries little weight on a laptop that already runs three models through Ollama and transformers.
4. **This is an expectation from the documentation, not a measured result.** Whether hybrid retrieval actually improves retrieval on the team's 40 questions has not been tested. If it does not, R7 loses weight and Chroma becomes an equal candidate.
5. Whichever store is chosen, `config/rag.yaml` records the library version, the on-disk path and the collection name, and the AI BOM lists the library.

## Open questions

1. Does the open-source Chroma persistent client support the sparse/hybrid `Search()` API, and from which version? (Not settled by the documentation.)
2. Which BM25 tokenisation does each tool apply to Turkish, and does it matter for article text (suffixes, case)?
3. Does hybrid retrieval improve hit@5 over dense-only on the 40-question set with the laptop embedding model? (Not measured.)
## References

[1] Chroma, "Filters," Chroma Cookbook. https://cookbook.chromadb.dev/core/filters/

[2] Chroma, "Delete data," Chroma Docs. https://docs.trychroma.com/docs/collections/delete-data.md

[3] Chroma, "Sparse vector support in Chroma." https://www.trychroma.com/project/sparse-vector-search

[4] Qdrant, "Hybrid search," Qdrant Documentation. https://qdrant.tech/documentation/search-tuning/hybrid-search/

[5] Faiss, "IndexIDMap.h," Faiss C++ API reference. https://faiss.ai/cpp_api/file/IndexIDMap_8h.html

[6] "FAISS Python API tutorial: IndexFlatL2, IndexIVFFlat, add, search, and remove_ids," GoLinuxCloud. https://www.golinuxcloud.com/faiss-python-api/

[7] Microsoft, "Vector DBs comparison for offline RAG search running on in-car embedded system," Edge AI solution ADR library. https://microsoft.github.io/edge-ai/solution-adr-library/vdb-on-edge-in-car-embedded-system

[8] qdrant-client, "Client setup" (local and in-memory mode), package documentation, v1.15.0. https://tessl.io/registry/tessl/pypi-qdrant-client/1.15.0/files/docs/client-setup.md

[9] LangChain, "Qdrant vector store" (local mode, sparse and hybrid retrieval examples). https://docs.langchain.com/oss/python/integrations/vectorstores/qdrant

[10] Qdrant, "qdrant-client" README (local mode), GitHub. https://github.com/qdrant/qdrant-client
