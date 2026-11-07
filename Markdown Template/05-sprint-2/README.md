# Sprint 2 Welcome Page

Welcome.

This is the main page of “Sprint 2” made by the Chunky team.

Sprint goal

Show a first working baseline: run the long-context model (all six texts at once) and the RAG alpha on the same 10 development questions, and give the team a frozen charter, a prioritised backlog and a design to build the beta on.

Deliverables of Sprint 2

- [X] Actions agreed on in the last sprint's retrospective have been carried out by the respective owners.
- [ ] The team has agreed on the Definition of Ready and Done checklists, and on a one-sentence sprint goal.
- [ ] Every relevant task and user story is moved to the current sprint, and each task has a story point estimate and an owner.
- [ ] **Welcome page** (`README.md` in the sprint folder): the sprint goal, what you achieved, links to the other deliverables, and the Git commit you submit.
- [ ] **Definition of Ready and Done** (`03-definition-of-ready-definition-of-done.md`).
- [ ] **Burndown chart** for the whole sprint, from Jira (`04-burndown-chart.md`).
- [ ] **Retrospective** (sprint folder): every "what went bad" row has an action and an owner.
- [ ] **Last sprint's review page**, if applicable (sprint folder): your answer to every item (accepted, accepted with rework, or rejected with a reason) and, for every accepted item, a link to its fix in the correction explanation.
- [ ] **Technical summary** (`01-review-committee-technical-summary.md` in the sprint folder), and one experiment card for each experiment run this sprint, in `Markdown Template/12-experiment-cards/`.
- [ ] **Design document** (`11-system-architecture-design-document.md`): a record for every decision taken this sprint, and the diagram and RAG parameters as the system is now.
- [ ] **Spike notes** (`docs/spikes/`), one per spike.
- [ ] **SBOM** (`10-software-bill-of-materials.md`): every model you tried, with its exact version, provider, licence, who accessed it and when, how you call it (API or local), whether you use it and why, and its experiment card. Also list tools and services that are not in `requirements.txt`.
- [ ] **Jira backlog export** (`docs/backlog/`): Markdown with the [Jira sync](../docs/JIRA_SYNC_SETUP.md), or `.xlsx` if the sync does not work.
- [ ] **Demo** in class at the end-of-sprint presentation, 10 minutes or less.

## Sprint 2 · Baseline

**Goal:** The charter and user stories are finalized. A first baseline retrieves relevant documents to the user queries and its performance has been measured. Go further if your workload allows.

### Deliverables, in addition to every sprint's

- [ ] **Final charter (v2)**, revised after the Sprint 1 feedback.
- [ ] **Final user stories:** story map v2, story requirements for every epic, and a prioritized backlog estimated with planning poker. Take the roles from the ISO/IEC 5339 stakeholder categories.
- [ ] **Test cases for your user stories:** for each story, a short test that checks its success criteria: the input or steps, and the expected result. Put them in the story requirements, next to the story.
- [ ] **Baseline:** the most basic vector database and retrieval over your documents; add a generator only if needed. Its setup should be documented in `README.md`, with pinned `requirements.txt`, parameters in `config/rag.yaml`, and prompts, if any, in `prompts/`. Also record the baseline parameters in its experiment card, because `config/rag.yaml` will change.
- [ ] **Q&A dataset v1** in `docs/eval/eval-set-v1.csv` (question, type, gold source, gold answer), with its data card in [`03-qa-data-report.md`](../Markdown%20Template/11-datasheets/03-qa-data-report.md), following Gebru et al., *Datasheets for Datasets*.
- [ ] **Corpus datasheet:** your document sources' register entry or dataset report, completed.
- [ ] **In the technical summary:** the metrics you chose (for retrieval, if applicable), why, the baseline score and the target from the charter, plus the baseline experiment card.
- [ ] **In the design document:** the RAG pipeline (each stage and its parameters) and your user interface technology (for example Gradio or Streamlit).
- [ ] **A mockup of the user interface**, as an image. It does not have to be connected to the system yet.

### Halfway check (11/11)

- [ ] The Sprint 1 feedback is addressed.
- [ ] The documents are indexed, and retrieval returns passages for a handful of test questions.
- [ ] A first draft of `eval-set-v1.csv` exists.
- [ ] The metrics and their targets are drafted.
- [ ] The user interface technology is chosen.
- [ ] The charter and story revisions are in a pull request.
