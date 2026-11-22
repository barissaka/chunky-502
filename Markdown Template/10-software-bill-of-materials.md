# Software Bill of Materials

## Software Bill of Materials

This register is where you will keep track of all third party libraries, tools and models to be used during development. For more information: Producing Software Bill of Materials a.k.a SBOMs for Atlassian - Inside Atlassian

syft is an open source project where you can supply your requirements.txt or docker image to generate an SBOM table.

Checksums below were taken on 13 Nov 2026 with `pip download <package>==<version> --no-deps` and `pip hash` (SHA-256 of the wheel file), on macOS arm64 with Python 3.13. The rows from python-docx on are the RAG pipeline's dependencies (pinned in `pyproject.toml` and `requirements.txt`); their checksums were taken on 14 Nov 2026 the same way, for the Windows x64 / Python 3.12 wheels used on the host laptop.

| Package Name | Version | Description | License | Supplier | Package Checksum |
|---|---|---|---|---|---|
| anthropic | 2.8.0 | Python SDK for the Anthropic API; sends the baseline and judge requests (E3) | Apache-2.0 | Anthropic | SHA-256 `76ad332e2d500fc54d0112cf100544ad1a7605e71e092b98d9eb664d2b66e283` (anthropic-2.8.0-py3-none-any.whl) |
| deepeval | 4.3.4 | LLM evaluation framework; GEval metrics for answer correctness and the out-of-scope rubric (E3) | Apache-2.0 | Confident AI | SHA-256 `b3d15701c758134ad16d2e076fefe721f1574ebdefcce80bb10cbb04772569e3` (deepeval-4.3.4-py3-none-any.whl) |
| pandas | 3.1.1 | Tabular scoring and per-type breakdowns in eval.py (E3) | BSD-3-Clause (pip show leaves the License field empty; licence from the project's LICENSE file) | pandas development team (NumFOCUS) | SHA-256 `269716b079899a92953837d13ed215ef2d36dbf8dd3787faf617f1160a2f5062` (pandas-3.1.1-cp313-cp313-macosx_11_0_arm64.whl; platform-specific wheel, differs on other systems) |
| python-docx | 1.2.0 | Reads the six legal texts from Word in document order, tables included (`src/chunky/extract.py`) | MIT | python-openxml (Steve Canny) | SHA-256 `3fd478f3250fbbbfd3b94fe1e985955737c145627498896a8a6bf81f4baf66c7` (python_docx-1.2.0-py3-none-any.whl) |
| pyyaml | 6.0.3 | Reads `data/legal/documents.yaml` and `config/rag.yaml` | MIT | The YAML Project | SHA-256 `5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b` (pyyaml-6.0.3-cp312-cp312-win_amd64.whl; platform-specific wheel) |
| openpyxl | 3.1.5 | Reads the evaluation set Excel file; writes the run results as Excel (`05_answer_check.ipynb`) | MIT | openpyxl (Eric Gazoni, Charlie Clark) | SHA-256 `5282c12b107bffeef825f4617dc029afaf41d0ea60823bbb665ef3079dc79de2` (openpyxl-3.1.5-py2.py3-none-any.whl) |
| numpy | 2.5.4 | Vector store of the baseline: dense vectors on disk and exhaustive similarity search (AD-06, E1) | BSD-3-Clause | NumPy developers (NumFOCUS) | SHA-256 `a7b1b6353e36a7e50de2973a38d705c88ee93adcf120673cee7f45a4a3fa223a` (numpy-2.5.4-cp312-cp312-win_amd64.whl; platform-specific wheel) |
| torch | 2.15.0+cpu | Runs bge-m3 on the CPU (AD-04, E1) | BSD-3-Clause | PyTorch Foundation | SHA-256 `5af9fb357790db09e62484b12032304f046c22c4b1895ca88c4cf5987ea369ca` (torch-2.15.0+cpu-cp312-cp312-win_amd64.whl from download.pytorch.org/whl/cpu) |
| transformers | 5.23.0 | Loads the bge-m3 tokenizer and model (AD-04, E1) | Apache-2.0 | Hugging Face | SHA-256 `018e82fd07490ad5bb58414f65e31576033dc7f36bed10c574843f69b90991bf` (transformers-5.23.0-py3-none-any.whl) |
| huggingface-hub | 2.4.0 | Downloads the pinned bge-m3 revision and its `sparse_linear.pt` layer | Apache-2.0 | Hugging Face | SHA-256 `42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801` (huggingface_hub-2.4.0-py3-none-any.whl) |
| google-auth | 2.62.2 | Application Default Credentials for the Vertex AI calls (AD-03, E1) | Apache-2.0 | Google LLC | SHA-256 `e9bcdb0679b6a4369ac327c5c59f06d92f7b4cd2624e7100294c14632f55a36b` (google_auth-2.62.2-py3-none-any.whl) |
| requests | 2.34.2 | Sends the chat completions requests to Vertex AI (LLM gateway, AD-03, E1) | Apache-2.0 | Python Software Foundation | SHA-256 `2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0` (requests-2.34.2-py3-none-any.whl) |
| ipykernel | 7.4.0 | Jupyter kernel for the check notebooks (development only) | BSD-3-Clause | Project Jupyter | SHA-256 `a6757f790ddc5a6006b813d82da1a9dbb65b3a00f2b6607df776418c6566ec1c` (ipykernel-7.4.0-py3-none-any.whl) |
| nbstripout | 0.9.1 | Removes notebook outputs before each commit (development only) | MIT | nbstripout contributors | SHA-256 `ca027ee45742ee77e4f8e9080254f9a707f1161ba11367b82fdf4a29892c759e` (nbstripout-0.9.1-py3-none-any.whl) |
| streamlit | 1.67.0 | Web interface of the assistant (`src/ui/app.py`, US-09); installed from `src/ui/requirements.txt` | Apache-2.0 | Snowflake Inc. | SHA-256 `f29da87c443bfbdfc52738616e3d65745d438e718da8faf69e2be0da1e52ce64` (streamlit-1.67.0-py3-none-any.whl) |
| python-dotenv | 1.2.4 | Reads the optional `src/ui/.env` file (`CHUNKY_API_URL`) for the web interface; installed from `src/ui/requirements.txt` | BSD-3-Clause | Saurabh Kumar and python-dotenv contributors | SHA-256 `42269a8a5b3fd54ffa6f3d84b18abed50064717576b4ecf03dc4a55d8aa04fdc` (python_dotenv-1.2.4-py3-none-any.whl) |

### Tools and services not in requirements.txt

| Tool or service | Version | Use | Licence or terms | Supplier |
|---|---|---|---|---|
| Python | 3.12 | Runtime of the pipeline (`.venv` on each laptop) | PSF License | Python Software Foundation |
| Google Cloud Vertex AI (managed open models, MaaS) | service; region us-central1 | Serves the baseline generator gpt-oss-120b through the OpenAI-compatible chat completions endpoint; project `di502-rag-chatbot`, paid from the course credit | Google Cloud terms of service | Google LLC |
| Google Cloud CLI (`gcloud`) | 593.0.0 | `gcloud auth application-default login`, enabling the Vertex AI and Cloud Commerce Consumer Procurement APIs | Apache-2.0 | Google LLC |
| Hugging Face Hub | service | Source of the bge-m3 weights (unauthenticated download of the pinned revision) | Hugging Face terms of service; model under MIT | Hugging Face |
| Git / GitHub | — | Version control; repository `barissaka/chunky-502` | GPL-2.0 (Git); GitHub terms | Git project; GitHub (Microsoft) |
| Visual Studio Code with the Python and Jupyter extensions | — | Editor and notebook runner | MIT (extensions); Microsoft licence (VS Code) | Microsoft |

### Packages tried and not used

| Package | Version | Why it is not used |
|---|---|---|
| FlagEmbedding | 1.4.2 | Reference library for bge-m3; importing it failed on the host laptop because Windows Application Control blocked a DLL of its dependency `pyarrow` (`datasets`). bge-m3 is run directly with `transformers` instead (AD-04). Uninstalled. |
| qdrant-client | 1.20.0, 1.9.2 | Planned vector store (Spike 04); importing it failed because Windows Application Control blocked a DLL of `grpcio`. An older `grpcio` (1.62.3) loaded, but `qdrant-client` pulled the blocked version back in. Replaced by a numpy index (AD-06). Uninstalled. |
| grpcio, grpcio-tools | 1.85.1, 1.62.3 | Dependencies of `qdrant-client` (see above). Uninstalled. |

## AI Software Bill of Materials

This part of SBOM is where third party models will be documented. For models hosted on huggingface, you can use AI SBom Generator to generate an AI SBOM in the CycloneDX 1.6 json format, with other helpful metadata you can refer to.

When naming the model please specify all characteristics, including model version, size, and quantization. Include links to where you accessed the models weights and more details.

Specify what purpose each model will satisfy, who accessed this model, and when.

Finally mention the specific libraries used to interact with them, along with an associated experiment and the result, whether the model will be used or rejected and why.

| Model Name | Purpose | Accesser | Date of Access | Method of Interaction | Experiment and Results |
|---|---|---|---|---|---|
| Claude Sonnet 5.5 (`claude-sonnet-5-5`, released 28 Sep 2026; closed weights, size and quantization not published; 1M-token context) — https://platform.claude.com/docs/en/models/sonnet-5-5/overview | Baseline generator: answer the gold questions with all six legal texts in context, no retrieval | Ekin | Nov. 13, 2026 | Anthropic Messages API via the `anthropic` Python SDK 2.8.0 (`run.py`), prompt caching on the corpus | E3 — in-scope judge score 0.80 (8 of 10 pass), article recall 0.92, out-of-scope judge score 0.42; used as the reference baseline |
| Claude Opus 5.5 (`claude-opus-5-5`; closed weights, size and quantization not published) | LLM judge for answer correctness and the out-of-scope refusal rubric | Ekin | Nov. 13, 2026 | Anthropic Messages API via the `anthropic` SDK 2.8.0, wrapped as a DeepEval 4.3.4 custom model in `eval.py` (GEval) | E3 — sole scorer (no manual scores, D35): in-scope mean 0.80, out-of-scope 0.42 with the corrected rubric (D31), pass threshold 0.7; kept as judge for later runs |
| Claude (claude.ai assistant; model version not recorded for Oct.; Claude Opus 5.5 on 13 Nov) | Assisted building the gold Q&A set (questions, gold answers, references), and the E3 evaluation scripts; team made the final calls | Project team / Ekin | Oct. 24–27; Nov. 10–13 | claude.ai chat | Not part of the pipeline; outputs reviewed by the team (see Q&A Data Report) |
| BAAI/bge-m3 (XLM-RoBERTa-large based, about 568M parameters, FP32, not quantized; Hugging Face revision `5617a9f61b028005a4858fdac845db406aefb181`; dense 1,024-dim vectors and sparse lexical weights through `sparse_linear.pt`; 8,192-token input; MIT licence; supplier BAAI) — https://huggingface.co/BAAI/bge-m3 | Embedding model: embeds the 472 chunks and every question, dense and sparse, for hybrid retrieval | Özge | Nov. 14, 2026 | Local on the host laptop CPU; own `Embedder` in `src/chunky/index.py` with `transformers` 5.23.0 and `torch` 2.15.0 (FlagEmbedding could not be loaded) | E1 and E2 — hybrid retrieval, top 8: Recall@8 (hit rate) 1.00, article recall@8 0.92, MRR@8 0.76 on the 10 in-scope trial questions; used in the baseline, final choice in the Sprint 3 retrieval spike (AD-04) |
| openai/gpt-oss-120b (open weights, Apache-2.0; mixture of experts, about 117B total and 5.1B active parameters; weights released with MXFP4-quantized experts, serving precision on Vertex AI not published; 131,072-token context; supplier OpenAI, served by Google) — Vertex AI model `openai/gpt-oss-120b-maas` | Baseline answer generator: answers from the top 8 retrieved articles with article citations | Özge | Nov. 14, 2026 | Hosted, Vertex AI managed API (MaaS), us-central1; OpenAI-compatible chat completions endpoint called with `requests` 2.34.2 and `google-auth` 2.62.2 (`src/chunky/answer.py`); temperature 0, prompt `answer_v1` | E1 — on the 10 in-scope trial questions all answers cite a supporting article, citation recall 0.73, 4 invented citations in 2 answers, median answer time 26.6 s, mean 7,816 input / 920 output tokens; correctness scored with `eval.py`; used as the baseline generator, final backend in AD-03 |
| qwen/qwen3-235b-a22b-instruct-2507 (open weights, Apache-2.0; mixture of experts, 235B total and 22B active parameters; supplier Alibaba Qwen) — Vertex AI model `qwen/qwen3-235b-a22b-instruct-2507-maas` | Intended baseline generator (first choice) | Özge | Nov. 14, 2026 | Vertex AI managed API (MaaS), tried in us-south1 and through the global endpoint | Not used: every request returned HTTP 404 ("not found or your project does not have access"), and no managed-API card for the model is visible in the project's Model Garden; to be checked again in Sprint 3 |