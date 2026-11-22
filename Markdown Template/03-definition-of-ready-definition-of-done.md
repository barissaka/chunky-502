# Definiton of Ready Definiton of Done

For each sprint, it is defined the full list of the definition of ready and the definition of done.

The "Column" cell names the AI life cycle stage (ISO/IEC 5338) of the work. Acceptance criteria belong to each story in Jira; the lists below apply to every item of the sprint.

## Sprint 1:

| Column | Definition of Ready |
|---|---|
| Design and development (6.4.7 Knowledge acquisition) | The six official legal texts are named, with their official source and access checked; the terms of use of each question source are read; no personal data (names, licence plates) will be stored (C-12). |
| Design and development (6.4.8 AI data engineering) | The question schema is final: source, URL, access date, question type, in-scope or out-of-scope, ambiguity label. |
| Verification and validation (6.4.13 Validation) | Question set v1 is tagged; 12 people are invited and written confirmation is requested for 10; the test room, timer and survey form are ready. |
| Inception (6.4.2 Stakeholder needs and requirements definition) | Every story or task has an owner, story points and a "done when" sentence; the work fits 7 hours per person per week. |

| Column | Definition of Done |
|---|---|
| Design and development (6.4.7 Knowledge acquisition) | The six texts are stored in the Git repository with source, retrieval date, article count and token count (D1); the article counts are checked against the official texts. |
| Design and development (6.4.8 AI data engineering) | At least 30 in-scope and 10 out-of-scope questions are tagged; the answer key is written from the legal texts; a second member has checked a sample of the answers (D2). |
| Verification and validation (6.4.13 Validation) | 10 participants answered 3 questions each; median time is recorded (D3). |
| Re-evaluation (6.3.8 Quality assurance) | Project Charter v1 is approved by the Product Owner (D4); the architecture diagram and the first ADRs are reviewed; the sprint retrospective is held.|

## Sprint 2:

| Column | Definition of Ready |
|---|---|
| Design and development (6.4.7 Knowledge acquisition) | D1 is fixed and D2 is tagged and checked; the retrieval dates are recorded and the amendment dates are checked at the sprint start. |
| Design and development (6.4.8 AI data engineering) | The 10 development questions are chosen from D2: their ids are written in the configuration and frozen. |
| Design and development (6.4.5 Design definition) | The embedding model runs locally on a team laptop and the hosted LLM on Google Cloud is reachable; the long-context model takes all six texts and the question, checked with one test question; the evaluation script and its log format are agreed. |
| Verification and validation (6.4.11 Verification) | One long-context run with all six texts at once is planned; the measures to report are listed (Recall@k, correct answers, supporting article, response time). |
| Inception (6.4.2 Stakeholder needs and requirements definition) | The Sprint 1 review is done, Charter v1 is approved and the Sprint 1 feedback is listed; the stories of the sprint (US-01, US-09) have acceptance criteria and test cases written; the stakeholder roles of the stories are taken from the ISO/IEC 5339 categories. |

| Column | Definition of Done |
|---|---|
| Design and development (6.4.9 Implementation) | The retrieval index with one chunk per article of all six texts is built; the RAG pipeline returns the answer.; the alpha runs end to end with the embedding model on a team laptop and the LLM on Google Cloud: a Turkish question returns a Turkish answer with its article reference (D7); the model versions are pinned in the configuration; the user interface technology is chosen. |
| Verification and validation (6.4.11 Verification) | The long-context baseline is run once with all six texts on the 10 development questions and logged with response time and memory use (D5); the RAG pipeline is run on the same 10 questions and Recall@k is calculated; the results are reported as counts out of 10 by question type.; |
| Design and development (6.4.8 AI data engineering) | The question set is in `docs/eval/eval-set-v1.csv` with question, type, gold source and gold answer. |
| Design and development (6.4.4 System architecture definition) | The technical summary names the metrics, why they were chosen, the baseline score and the target from the charter; the design document describes each stage of the RAG pipeline with its parameters and the interface technology; a mockup of the user interface exists as an image. |
| Inception (6.4.2 Stakeholder needs and requirements definition) | The charter is revised after the Sprint 1 feedback and frozen as the final charter; story map v2 is in the repository; the story requirements of every epic list each story's tasks, success criteria and test cases next to the story; the backlog is prioritised.|
| Verification and validation (6.4.11 Verification, 6.4.13 Validation) | The acceptance criteria of US-01 and US-09 are met and their test cases passed; |
| Re-evaluation (6.3.8 Quality assurance) | Open problems have their own Jira items; actual hours are logged; the sprint review is held; the go/no-go material for the beta is prepared; every Sprint 2 deliverable is uploaded by 14/11/2026 and linked from the welcome page; the burndown chart and the Jira backlog export are in the sprint folder. |

## Sprint 3:

| Column | Definition of Ready |
|---|---|
| Design and development (6.4.6 System analysis) | The go/no-go decision for the beta (M6) is recorded; the beta scope and the list of known problems from the alpha are written. |
| Verification and validation (6.4.11 Verification) | The question set for the formal run is frozen (40 questions, 5 penalty questions, 5 individual-case questions); the 8 ambiguous questions with their scripted replies are listed for US-12; the settings of the run are fixed; the run is planned at least 3 days before M7. |
| Deployment (6.4.12 Transition) | 	The team laptop that runs the beta (with the local embedding model) is set up and tested and reaches the hosted LLM on Google Cloud; the test sessions with the 10 pilot participants are planned; personal data masking is in place before logging (C-12). |
| Inception (6.4.2 Stakeholder needs and requirements definition) | US-02, US-06, US-07, US-08, US-11 and US-12  have acceptance criteria, test cases and points; the dependencies between them are written. |

| Column | Definition of Done |
|---|---|
| Design and development (6.4.10 Integration) | The beta runs with the embedding model on a team laptop and the LLM on Google Cloud and the pilot participants can use it in the test sessions (D9); the prompt, chunking and retrieval settings are recorded.; the question endpoint returns the answer and the interface page is connected to it. |
| Verification and validation (6.4.11 Verification) | One formal run of all questions is scored once; the card reports correct answers and supported article references on the 30 in-scope questions, the penalty questions, the refusals and the response times, next to D5 and D6 (D8); 10 of 10 out-of-scope questions are declined; every answer is returned within 60 seconds; the share of correct clarifying questions on the 8 ambiguous questions is reported |
| Verification and validation (6.4.11 Verification, 6.4.13 Validation) | The acceptance criteria of US-02, US-06, US-07, US-08, US-11 and US-12 are met and their test cases passed; a second member reviewed the work; the Product Owner accepted it. |
| Re-evaluation (6.3.8 Quality assurance) | Actual hours are logged; the technical document and the ADRs are updated; the go/no-go material for the pilot is prepared. |

## Sprint 4:

| Column | Definition of Ready |
|---|---|
| Verification and validation (6.4.13 Validation) | The go/no-go decision for the pilot (M8, 14/12/2026) is recorded; 10 participants confirmed in writing; the survey and the 10 out-of-scope questions are ready. |
| Verification and validation (6.4.11 Verification) | The question set that the team has not seen is supplied by the Project Review Committee (check by 23/12/2026); the release candidate scope is fixed. |
| Inception (6.4.2 Stakeholder needs and requirements definition) | US-03, US-04, US-05, US-10 and US-13 have acceptance criteria, test cases and points. |

| Column | Definition of Done |
|---|---|
| Verification and validation (6.4.13 Validation) | The pilot is run and the results are reported against the Objective 1, 3 and 4 targets, as counts out of the participants who took part (D10). |
| Deployment (6.4.12 Transition) | 	The release candidate is installed on the team laptop with the hosted LLM on Google Cloud reachable and the live demo script returns a response without an error for every question (D11). |
| Verification and validation (6.4.11 Verification) | The release candidate is evaluated on the unseen question set after the last change (D11). |
| Verification and validation (6.4.11 Verification, 6.4.13 Validation) | The acceptance criteria of US-03, US-04, US-05, US-10 and US-13 are met and their test cases passed; the Product Owner accepted them. |
| Re-evaluation (6.3.8 Quality assurance) | The final report includes the limitations, such as the articles amended after retrieval (D12); the documents match the delivered system; no known critical problem is open; actual hours are logged; the retrospective is held. |
