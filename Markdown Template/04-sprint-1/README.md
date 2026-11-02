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

## Feedback on Sprint 1 and our response

| # | Feedback | Response | Pages changed |
|---|---|---|---|
| 1 | The front page (README.md) was not filled in. | Filled in: every cell of the canvas grid now summarises its page, with a short project summary above the grid and a glossary below it. | Project Canvas README |
| 2 | Deliverable, milestone and release dates should be pushed back to account for the review period. | From Sprint 2 on, each milestone is dated at least two days after its deliverables are due: M4 13/11, M5 20/11, M7 11/12, M9 24/12. M6 and M8 already fell five days after their deliverables. M10 stays on 30/12/2026 (C-09), so D11 and D12 move forward to 27/12/2026 and D10 to 22/12/2026. The gaps between sprints are recorded as review periods. Triggers and status dates that referred to the old dates are updated. | Milestones; Assumptions & Constraints (A-03, C-09); Deliverables; Facilities & Resources (row 12); Release Plan; Risks (R-11, R-17, R-20) |
| 3 | Correction: technical risks such as R-15 are expected, since each constraint or assumption is linked to a risk. | Acknowledged; no change needed. | — |
| 4 | What is an ambiguity label? It needs an explanation in the charter. | Defined in the D2 description, with an example, and in the canvas glossary. Major Activities rows 6 and 13 and R-15 now point to that definition. D6 and D8 now report the precision and recall of the decision to ask a clarifying question, and M7 states that it is measured. | Project Canvas README; Milestones (M7); Major Activities (rows 6, 13); Deliverables (D2, D6, D8); Risks (R-15) |
| 5 | The Q&A set needs a datasheet deliverable due in Sprint 2, logging all decisions behind the dataset. | New deliverable D13, Datasheet for Q&A Generation-Dataset v1, due 16/11/2026, supporting M5. New activity row 34 and cost row 16 (6 person-hours). The statement that the team writes no datasheet is corrected. | Milestones (M5); Major Activities (rows 6, 34); Deliverables (D13); Cost & Funding (row 16, totals); Release Plan (Sprint 2) |
