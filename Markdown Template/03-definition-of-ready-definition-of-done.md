# Definiton of Ready Definiton of Done

For each sprint, it is defined the full list of the definition of ready and the definition of done.

The "Column" cell names the AI life cycle stage (ISO/IEC 5338) of the work. Acceptance criteria belong to each story in Jira; the lists below apply to every item of the sprint.

## Sprint 1:

| Column | Definition of Ready |
|---|---|
| Data acquisition | The six official legal texts are named, with their official source and access checked; the terms of use of each question source are read; no personal data (names, licence plates) will be stored (C-12). |
| Labelling | The question schema is final: source, URL, access date, question type, in-scope or out-of-scope, ambiguity label. |
| Validation (default state) | Question set v1 is tagged; 12 people are invited and written confirmation is requested for 10; the test room, timer and survey form are ready. |
| All stages | Every story or task has an owner, a second named member who can take it over, story points and a "done when" sentence; the work fits 7 hours per person per week. |

| Column | Definition of Done |
|---|---|
| Data acquisition | The six texts are stored in the Git repository with source, retrieval date, article count and token count (D1); the article counts are checked against the official texts. |
| Labelling | At least 30 in-scope and 10 out-of-scope questions are tagged; the answer key is written from the legal texts; a second member has checked a sample of the answers (D2). |
| Validation (default state) | 10 participants answered 3 questions each; median time and number of places consulted are recorded (D3). |
| All stages | Project Charter v1 is approved by the Product Owner (D4); the architecture diagram and the first ADRs are reviewed; actual hours are logged; the sprint review is held and the risk register is checked. |

## Sprint 2:

| Column | Definition of Ready |
|---|---|
| Data acquisition | D1 is fixed and D2 is tagged and checked; the retrieval dates are recorded and the amendment dates are checked at the sprint start. |
| Labelling (development set) | The 10 development questions are chosen from D2: 8 in-scope questions that cover the question types (including one follow-up and one ambiguous question) and 2 out-of-scope questions; their ids are written in the configuration and frozen. |
| Design and development | The team laptop that runs the models is confirmed: the embedding model and the generation model are downloaded and run on it; the long-context model takes all six texts (255,138 tokens) and the question, checked with one test question; the evaluation script and its log format are agreed. |
| Verification | One long-context run with all six texts at once is planne; the measures to report are listed (Recall@k, correct answers, supporting article, declined out-of-scope questions, response time). |
| Stories and planning | The Sprint 1 review is done, Charter v1 is approved and the Sprint 1 feedback is listed; the stories of the sprint (US-01, US-09) have acceptance criteria and test cases written; the stakeholder roles of the stories are taken from the ISO/IEC 5339 categories. |

## Sprint 3:

| Column | Definition of Ready |
|---|---|
| Design and development | The go/no-go decision for the beta (M6) is recorded; the beta scope and the list of known problems from the alpha are written. |
| Verification | The question set for the formal run is frozen (40 questions, 5 penalty questions, 5 individual-case questions); the settings of the run are fixed; the run is planned at least 3 days before M7. |
| Deployment | The team laptop that runs the beta is set up and tested; the test sessions with the 10 pilot participants are planned; personal data masking is in place before logging (C-12). |
| All stories | US-02, US-06, US-07, US-08 and US-11 have acceptance criteria, test cases and points; the dependencies between them are written. |

| Column | Definition of Done |
|---|---|
| Design and development | The beta runs on a team laptop and the pilot participants can use it in the test sessions (D9); the prompt, chunking and retrieval settings are recorded. |
| Verification | One formal run of all questions is scored once; the card reports correct answers and supported article references on the 30 in-scope questions, the penalty questions, the refusals and the response times, next to D5 and D6 (D8); 10 of 10 out-of-scope questions are declined; every answer is returned within 60 seconds. |
| Stories | The acceptance criteria of US-02, US-06, US-07, US-08 and US-11 are met and their test cases passed; a second member reviewed the work; the Product Owner accepted it. |
| All stages | Actual hours are logged; the technical document and the ADRs are updated; the go/no-go material for the pilot is prepared. |

## Sprint 4:

| Column | Definition of Ready |
|---|---|
| Validation (pilot) | The go/no-go decision for the pilot (M8, 14/12/2026) is recorded; 10 participants confirmed in writing; the survey and the 10 out-of-scope questions are ready. |
| Verification | The question set that the team has not seen is supplied by the Project Review Committee (check by 23/12/2026); the release candidate scope is fixed. |
| All stories | US-03, US-04, US-05 and US-10 have acceptance criteria, test cases and points. |

| Column | Definition of Done |
|---|---|
| Validation (pilot) | The pilot is run and the results are reported against the Objective 1, 3 and 4 targets, as counts out of the participants who took part (D10). |
| Deployment | The release candidate is installed on the team laptop and the live demo script returns a response without an error for every question (D11). |
| Verification | The release candidate is evaluated on the unseen question set after the last change (D11). |
| Stories | The acceptance criteria of US-03, US-04, US-05 and US-10 are met and their test cases passed; the Product Owner accepted them. |
| All stages | The final report includes the limitations, such as the articles amended after retrieval (D12); the documents match the delivered system; no known critical problem is open; actual hours are logged; the retrospective is held. |
