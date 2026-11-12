# Chunky — Turkish traffic rules and penalties assistant

**DI 502 Data Informatics Project · METU Informatics Institute · Fall 2026 · Team Chunky**

Chunky answers single-turn questions in Turkish about road-traffic rules, procedures and penalties, and cites the articles (*madde*) of the legislation it used. It is a retrieval-augmented generation (RAG) system over six legal texts (Kanun 2918 and five regulations), running entirely on a team laptop with open-weight models served by Ollama. When the answer is not in the texts, it says so instead of guessing.

Team: see [Team Members](Markdown%20Template/02-team-members.md). Project documentation lives in this repository as Markdown and is mirrored to Confluence on every push to `main`.

## Status

| Sprint | Dates | State |
|---|---|---|
| Sprint 1 | until 27 Oct 2026 | project canvas, user stories, system design v1 |
| Sprint 2 | 28 Oct – 18 Nov | baseline retrieval, evaluation set, first experiment |
| Sprint 3 | 18 Nov – 9 Dec | full pipeline, beats the baseline |
| Sprint 4 | 9 – 30 Dec | final product and demo |

The code arrives in Sprint 2. Until then this repository holds the documentation and the configuration skeleton.

## Repository layout

```
Markdown Template/          project documentation (synced to Confluence)
  03-project-canvas/        charter: summary, milestones, risks, release plan
  04-sprint-1/ 05-sprint-2/ sprint README, retrospective, review pages
  06-user-stories/          user story maps and epic requirements
  10-software-bill-of-materials.md
  11-datasheets/            third-party dataset register, dataset and Q&A reports
  11-system-architecture-design-document.md
  12-experiment-cards/      one card per experiment; README is the index
config/rag.yaml             product configuration: chunking, models, top-k, prompt variant
prompts/                    prompt files, one version per file (never edited in place)
data/                       local corpus and evaluation set (not committed; see datasheets)
src/                        application code (indexer, retriever, query guard, UI)
tests/                      pytest tests
docs/
  spikes/                   research spikes
  eval/                     evaluation results per sprint
  backlog/                  Jira exports
requirements.txt            Python dependencies (pinned from Sprint 2)
```

## Running the system

*To be completed in Sprint 2 with the baseline. The instructions below are the target shape.*

Requirements: Python 3.11, [Ollama](https://ollama.com) installed on the host laptop (Windows), 16 GB RAM; no GPU needed.

```bash
# 1. Environment
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt

# 2. Models (served locally by Ollama)
ollama pull qwen3-embedding:0.6b
ollama pull qwen3:4b

# 3. Build the index from the legal texts in data/
python -m src.index

# 4. Start the assistant
python -m src.app

# 5. Evaluation and tests
python -m src.evaluate            # writes results to docs/eval/
pytest
```

No API keys are required: every model runs on the laptop. Random seeds and LLM settings (temperature, thinking mode) are set in `config/rag.yaml` so that runs are reproducible.

## Where to look

- **What we are building and why:** [Project Executive Summary](Markdown%20Template/03-project-canvas/01-project-executive-summary.md)
- **How it is built:** [System Architecture Design Document](Markdown%20Template/11-system-architecture-design-document.md)
- **What has been tried:** [Experiment Cards](Markdown%20Template/12-experiment-cards/README.md)
- **Where the data comes from:** [Datasheets](Markdown%20Template/11-datasheets/README.md)
- **Sprint reports:** [Sprint 1](Markdown%20Template/04-sprint-1/README.md), [Sprint 2](Markdown%20Template/05-sprint-2/README.md)
- **Confluence:** https://chunky-502.atlassian.net
- **Jira backlog (project key CHUNKY):** https://chunky-502.atlassian.net/jira/software/projects/CHUNKY/boards/1/backlog
- **Course repository and templates:** https://github.com/volgasezen/di502

## Working agreements

- Documentation is Markdown in this repository; Confluence is a mirror, edited only here.
- One branch per feature, named after the Jira issue (e.g. `CHUNKY-12-query-guard`); commit messages start with the issue key; merged into `main` with `--no-ff`.
- Parameters live in `config/rag.yaml`; experiment parameter spaces live in the experiment cards and W&B.

## RAG development environment (Windows)

Requirements: Git, Python 3.12, and VS Code with the Python and Jupyter extensions.

```powershell
git clone https://github.com/barissaka/chunky-502.git
cd chunky-502
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
nbstripout --install
```

If `Activate.ps1` fails with "running scripts is disabled on this system", run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

`nbstripout --install` removes notebook outputs before each commit. It applies only to your own clone, so every team member needs to run it once.

In notebooks, select `.venv` as the kernel. To check the setup, run `notebooks/00_setup_check.ipynb`.