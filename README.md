# Chunky — Turkish traffic rules and penalties assistant

**DI 502 Data Informatics Project · METU Informatics Institute · Fall 2026 · Team Chunky**

Chunky answers single-turn questions in Turkish about road-traffic rules, procedures and penalties, and cites the articles (*madde*) of the legislation it used. It is a retrieval-augmented generation (RAG) system over six legal texts (Kanun 2918 and five regulations), running on a team laptop. The Sprint 2 baseline embeds the texts locally with bge-m3 and generates answers with an open-weight model (gpt-oss-120b) served by Google Cloud Vertex AI. When the answer is not in the texts, it says so instead of guessing.

Team: see [Team Members](Markdown%20Template/02-team-members.md). Project documentation lives in this repository as Markdown and is mirrored to Confluence on every push to `main`.

## Status

| Sprint | Dates | State |
|---|---|---|
| Sprint 1 | until 27 Oct 2026 | project canvas, user stories, system design v1 |
| Sprint 2 | 28 Oct – 18 Nov | baseline retrieval, evaluation set, first experiment |
| Sprint 3 | 18 Nov – 9 Dec | full pipeline, beats the baseline |
| Sprint 4 | 9 – 30 Dec | final product and demo |

Sprint 2 adds the baseline pipeline: text extraction, chunking, the index and answering with citations (see [Running the baseline](#running-the-baseline-sprint-2)).

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

## Running the baseline (Sprint 2)

Requirements: the [RAG development environment](#rag-development-environment-windows) below (Windows, Python 3.12, `.venv`), the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install), access to the team's Google Cloud project `di502-rag-chatbot`, and about 5 GB of free disk space for the embedding model. No GPU is needed.

```powershell
# 1. Dependencies (pinned) and the project package
pip install -r requirements.txt
pip install -e . --no-deps

# 2. Google Cloud login, once per laptop (no API key is stored)
gcloud auth application-default login
gcloud auth application-default set-quota-project di502-rag-chatbot

# 3. Build the index from data/chunks/chunks.jsonl into index/bge-m3/ (not committed)
#    The first run downloads bge-m3 into the Hugging Face cache; indexing takes about 6 minutes on CPU.
python -m chunky.index
```

4. Run `notebooks/04_index_check.ipynb` (index and retrieval checks) and `notebooks/05_answer_check.ipynb` (answers the 10 trial questions and writes the results to `docs/eval/runs/`, also in the format of the team's `eval.py`).

Parameters (embedding model and revision, `top_k`, sparse weight, LLM, temperature, prompt version) are in `config/rag.yaml`; prompts are in `prompts/`. The baseline and its results are described in [E1](Markdown%20Template/12-experiment-cards/E1-baseline.md).

Notes:
- On Linux, install the CPU build of PyTorch first (`pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu`); on Windows and macOS the default wheel is fine.
- If Windows reports *"An Application Control policy has blocked this file"* when a package is imported, see AD-06 in the [design document](Markdown%20Template/11-system-architecture-design-document.md); `FlagEmbedding` and `qdrant-client` are not used for this reason.

## Running the web interface

The chat interface (Streamlit) calls the same pipeline as `notebooks/05_answer_check.ipynb`: retrieval on this laptop, answer from the model in `config/rag.yaml`. Complete [Running the baseline](#running-the-baseline-sprint-2) first (index built, Google Cloud login done).

```powershell
cd src\ui
pip install -r requirements.txt
python -m streamlit run app.py
```

The page opens at http://localhost:8501. The first question takes about a minute longer because the embedding model is loaded into memory. Run the command from `src\ui` so the theme in `src/ui/.streamlit/config.toml` is applied. Stop the interface with `Ctrl+C` in the terminal.

Settings (model, prompt, `top_k`) are read from `config/rag.yaml`; the interface has no separate settings. If `CHUNKY_API_URL` is set in `src/ui/.env` (copy `.env.example`), the interface sends questions to a `/ask` service instead.

## Running the tests

The automated tests are in `tests/` and run with pytest (installed by `pip install -r requirements.txt`). They call no model and need no index or Google Cloud login.

```powershell
python -m pytest tests
```

`tests/test_guard.py` checks the decline path (US-06): the code that recognises the fixed out-of-scope reply and the no-advice notice, and that the prompt set in `config/rag.yaml` contains both sentences. Whether the model declines the right questions is measured in `notebooks/06_decline_check.ipynb`.

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