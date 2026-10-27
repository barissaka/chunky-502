# Sprint 1 Welcome Page

This is the main page of Sprint 1 (14/10/2026 – 28/10/2026) of Team Chunky, the traffic rules and penalties assistant.

**Sprint goal (Jira, Sprint 1):** Prepare the data and the plan: by 28/10/2026 we have the fixed document set (D1), question set with its answer key (D2), the default-state measurement (D3), Project Charter v1 (D4), and the system architecture, so that Sprint 2 can start building and testing the baselines.

## What was done in Sprint 1

- **Project Charter.** All eleven canvas pages are written: executive summary, milestones, assumptions and constraints, major activities, deliverables, dependencies, cost and funding, project organization, facilities and resources, release plan and risks. The charter was revised after the Week 3 and Week 4 feedback: the RAG-versus-long-context choice is justified from the corpus size (255,138 tokens), the risk mitigations are written as report, log and maintain mechanisms, and the models are listed as constraints rather than resources.
- **Document set.** The six legal texts are fixed and stored in the repository as the official PDFs and as extracted plain text (`data/legal/`). A random sample of 20 articles was compared with the official source and found identical ([article check](../../docs/eval/article-check-2026-10-25.md)). The register entry of each text is in the [Third-party Dataset Register](../11-datasheets/01-third-party-dataset-register.md).
- **User stories.** Three epics and eleven user stories with their engineering tasks are in Jira; the [User Story Map](../06-user-stories/01-user-story-map.md) shows the feature–epic–story–task hierarchy. The Jira backlog is exported to [`docs/backlog/`](../../docs/backlog/).
- **System architecture.** The [System Architecture Design Document](../11-system-architecture-design-document-local.md) describes the laptop-only design (one team laptop runs the retriever, the vector store and the chat page; the query guard added after the Week 4 feedback sits between the chat page and the retriever) and records the decisions taken so far.
- **Spike notes.** Three spikes in [`docs/spikes/`](../../docs/spikes/)
- **Tooling.** The GitHub repository (course template structure), the Jira project with four sprints and story-point estimation, the Confluence space with the automatic GitHub synchronisation, and the Definition of Ready and Done for Sprints 1 to 4 are in place.
