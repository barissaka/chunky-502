# Sprint 2 Welcome Page

Welcome.

This is the main page of “Sprint 2” made by the Chunky team.

Sprint goal

Show a first working baseline: run the long-context model (all six texts at once) and the RAG alpha on the same 10 development questions, and give the team a frozen charter, a prioritised backlog and a design to build the beta on.

Deliverables of Sprint 2

- [X] Actions agreed on in the last sprint's retrospective have been carried out by the respective owners.
- [X] The team has agreed on the Definition of Ready and Done checklists, and on a one-sentence sprint goal.
- [X] Every relevant task and user story is moved to the current sprint, and each task has a story point estimate and an owner.
- [X] **Welcome page** (`README.md` in the sprint folder): the sprint goal, what you achieved, links to the other deliverables, and the Git commit you submit.
- [X] **Definition of Ready and Done** (`03-definition-of-ready-definition-of-done.md`).
- [X] **Burndown chart** for the whole sprint, from Jira (`04-burndown-chart.md`).
- [X] **Retrospective** (sprint folder): every "what went bad" row has an action and an owner.
- [X] **Last sprint's review page**, if applicable (sprint folder): your answer to every item (accepted, accepted with rework, or rejected with a reason) and, for every accepted item, a link to its fix in the correction explanation.
- [X] **Technical summary** (`01-review-committee-technical-summary.md` in the sprint folder), and one experiment card for each experiment run this sprint, in `Markdown Template/12-experiment-cards/`.
- [X] **Design document** (`11-system-architecture-design-document.md`): a record for every decision taken this sprint, and the diagram and RAG parameters as the system is now.
- [X] **Spike notes** (`docs/spikes/`), one per spike.
- [X] **SBOM** (`10-software-bill-of-materials.md`): every model you tried, with its exact version, provider, licence, who accessed it and when, how you call it (API or local), whether you use it and why, and its experiment card. Also list tools and services that are not in `requirements.txt`.
- [X] **Jira backlog export** (`docs/backlog/`): Markdown with the [Jira sync](../docs/JIRA_SYNC_SETUP.md), or `.xlsx` if the sync does not work.
- [X] **Demo** in class at the end-of-sprint presentation, 10 minutes or less.
- [X] **Final charter (v2)**, revised after the Sprint 1 feedback.
- [X] **Final user stories:** story map v2, story requirements for every epic, and a prioritized backlog estimated with planning poker. Take the roles from the ISO/IEC 5339 stakeholder categories.
- [X] **Test cases for your user stories:** for each story, a short test that checks its success criteria: the input or steps, and the expected result. Put them in the story requirements, next to the story.
- [X] **Baseline:** the most basic vector database and retrieval over your documents; add a generator only if needed. Its setup should be documented in `README.md`, with pinned `requirements.txt`, parameters in `config/rag.yaml`, and prompts, if any, in `prompts/`. Also record the baseline parameters in its experiment card, because `config/rag.yaml` will change.
- [X] **Q&A dataset v1** in `docs/eval/eval-set-v1.csv` (question, type, gold source, gold answer), with its data card in [`03-qa-data-report.md`](../Markdown%20Template/11-datasheets/03-qa-data-report.md), following Gebru et al., *Datasheets for Datasets*.
- [X] **Corpus datasheet:** your document sources' register entry or dataset report, completed.
- [X] **In the technical summary:** the metrics you chose (for retrieval, if applicable), why, the baseline score and the target from the charter, plus the baseline experiment card.
- [X] **In the design document:** the RAG pipeline (each stage and its parameters) and your user interface technology (for example Gradio or Streamlit).
- [X] **A mockup of the user interface**, as an image. It does not have to be connected to the system yet.

## Sprint 2 · Baseline

**Goal:** The charter and user stories are finalized. A first baseline retrieves relevant documents to the user queries and its performance has been measured. Go further if your workload allows.

**Submitted Commit:** 2e52859

**What we achieved:**


- Baseline results (10 in-scope development questions):
  - Long-context baseline, all six texts at once: judge score 0.80, 8 of 10 answers pass, mean response time 15.28 s. [E3](https://github.com/barissaka/chunky-502/blob/main/Markdown%20Template/12-experiment-cards/E3-claude-longcontext-baseline.md)
  - First RAG pipeline: judge score 0.61, 5 of 10 answers pass, mean response time 38.56 s. Recall@5 is 0.792 and Recall@8 is 0.917. [E1](https://github.com/barissaka/chunky-502/blob/main/Markdown%20Template/12-experiment-cards/E1-baseline.md)
  - On these questions the baseline scores higher. The gap is widest for questions that need several articles. The comparison document has the tables by question type, hop type and question. [Comparison Result](https://github.com/barissaka/chunky-502/blob/main/docs/eval/rag-vs-baseline-comparison.md)
- RAG pipeline: the six legal texts are prepared as article chunks, the embedding model runs locally, the LLM is hosted.
- Planning: the charter is revised after the Sprint 1 feedback, story map v2 has 13 stories (US-12 and US-13 are new), the story requirements of the three epics have test cases for every story, and the backlog is prioritised and estimated with planning poker. [User Stories](https://github.com/barissaka/chunky-502/tree/main/Markdown%20Template/06-user-stories)
- Data: Q&A dataset v1 with its data card, and the corpus datasheet. [Q&A Data Report](https://github.com/barissaka/chunky-502/blob/main/Markdown%20Template/11-datasheets/03-qa-data-report.md)
- Documents: [technical summary](https://github.com/barissaka/chunky-502/blob/main/Markdown%20Template/05-sprint-2/01-review-committee-technical-summary.md), [design document](https://github.com/barissaka/chunky-502/blob/main/Markdown%20Template/11-system-architecture-design-document.md), [spike notes](https://github.com/barissaka/chunky-502/tree/main/docs/spikes)), [SBOM](https://github.com/barissaka/chunky-502/blob/main/Markdown%20Template/10-software-bill-of-materials.md) and [the user interface mockup](https://github.com/barissaka/chunky-502/blob/main/docs/images/ui-mockup-v1.png).




