# Software Bill of Materials

## Software Bill of Materials

This register is where you will keep track of all third party libraries, tools and models to be used during development. For more information: Producing Software Bill of Materials a.k.a SBOMs for Atlassian - Inside Atlassian

syft is an open source project where you can supply your requirements.txt or docker image to generate an SBOM table.

Checksums below were taken on 13 Nov 2026 with `pip download <package>==<version> --no-deps` and `pip hash` (SHA-256 of the wheel file), on macOS arm64 with Python 3.13.

| Package Name | Version | Description | License | Supplier | Package Checksum |
|---|---|---|---|---|---|
| anthropic | 2.8.0 | Python SDK for the Anthropic API; sends the baseline and judge requests (E3) | Apache-2.0 | Anthropic | SHA-256 `76ad332e2d500fc54d0112cf100544ad1a7605e71e092b98d9eb664d2b66e283` (anthropic-2.8.0-py3-none-any.whl) |
| deepeval | 4.3.4 | LLM evaluation framework; GEval metrics for answer correctness and the out-of-scope rubric (E3) | Apache-2.0 | Confident AI | SHA-256 `b3d15701c758134ad16d2e076fefe721f1574ebdefcce80bb10cbb04772569e3` (deepeval-4.3.4-py3-none-any.whl) |
| pandas | 3.1.1 | Tabular scoring and per-type breakdowns in eval.py (E3) | BSD-3-Clause (pip show leaves the License field empty; licence from the project's LICENSE file) | pandas development team (NumFOCUS) | SHA-256 `269716b079899a92953837d13ed215ef2d36dbf8dd3787faf617f1160a2f5062` (pandas-3.1.1-cp313-cp313-macosx_11_0_arm64.whl; platform-specific wheel, differs on other systems) |

## AI Software Bill of Materials

This part of SBOM is where third party models will be documented. For models hosted on huggingface, you can use AI SBom Generator to generate an AI SBOM in the CycloneDX 1.6 json format, with other helpful metadata you can refer to.

When naming the model please specify all characteristics, including model version, size, and quantization. Include links to where you accessed the models weights and more details.

Specify what purpose each model will satisfy, who accessed this model, and when.

Finally mention the specific libraries used to interact with them, along with an associated experiment and the result, whether the model will be used or rejected and why.

| Model Name | Purpose | Accesser | Date of Access | Method of Interaction | Experiment and Results |
|---|---|---|---|---|---|
| BAAI/bge-large-en-v1.5 | Embedding text chunks for use in the vector database | Volga | Oct. 6 | Run on GPU on server; interact via langchain integration of chromadb | Experiment 1 |
| Gemma 3 4b Q4_K_M | Generate answers given a context | Volga | Oct. 6 | Run on GPU on server; interact via api calls to Ollama host |   |
| Claude Sonnet 5.5 (`claude-sonnet-5-5`, released 28 Sep 2026; closed weights, size and quantization not published; 1M-token context) — https://platform.claude.com/docs/en/models/sonnet-5-5/overview | Baseline generator: answer the gold questions with all six legal texts in context, no retrieval | Ekin | Nov. 13, 2026 | Anthropic Messages API via the `anthropic` Python SDK 2.8.0 (`run.py`), prompt caching on the corpus | E3 — in-scope judge score 0.80 (8 of 10 pass), article recall 0.92, out-of-scope judge score 0.42; used as the reference baseline |
| Claude Opus 5.5 (`claude-opus-5-5`; closed weights, size and quantization not published) | LLM judge for answer correctness and the out-of-scope refusal rubric | Ekin | Nov. 13, 2026 | Anthropic Messages API via the `anthropic` SDK 2.8.0, wrapped as a DeepEval 4.3.4 custom model in `eval.py` (GEval) | E3 — sole scorer (no manual scores, D35): in-scope mean 0.80, out-of-scope 0.42 with the corrected rubric (D31), pass threshold 0.7; kept as judge for later runs |
| Claude (claude.ai assistant; model version not recorded for Oct.; Claude Opus 5.5 on 13 Nov) | Assisted building the gold Q&A set (questions, gold answers, references), and the E3 evaluation scripts; team made the final calls | Project team / Ekin | Oct. 24–27; Nov. 10–13 | claude.ai chat | Not part of the pipeline; outputs reviewed by the team (see Q&A Data Report) |
