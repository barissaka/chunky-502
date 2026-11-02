# Deliverables

**Project:** Traffic rules and penalties assistant · **Team:** Chunky

The deliverables below are the artifacts that prove the milestones in [Milestones](02-milestones.md). Each one carries the same number and name on both pages. From Sprint 2 on, each is due at least two days before its milestone, so that it can be reviewed before the milestone is recorded. The product is delivered in three builds: alpha (D7), beta (D9) and release candidate (D11).

The team writes no model card: no model is trained or fine-tuned. The question set and answer key (D2) have a datasheet (D13) that logs every decision behind their creation. The legal texts have no datasheet: they are used as published by their official sources, and D1 records those sources.

## Overview

| # | Deliverable | Kind | Due Date | Milestone it supports |
|---|---|---|---|---|
| D1 | Document set and Dataset Report | Solution | 21/10/2026 | M1 |
| D2 | Q&A Generation-Dataset v1 | Solution | 26/10/2026 | M2 |
| D3 | Default-state measurement report | Project management | 26/10/2026 | M2 |
| D4 | Project Charter v1 | Project management | 28/10/2026 | M3 |
| D5 | Long-context baseline experiment card | Solution | 11/11/2026 | M4 |
| D6 | RAG baseline experiment card | Solution | 18/11/2026 | M5, M6 |
| D7 | Alpha prototype | Solution | 18/11/2026 | M5, M6 |
| D8 | MVP validation experiment card | Solution | 09/12/2026 | M7, M8 |
| D9 | Beta release | Solution | 09/12/2026 | M7, M8 |
| D10 | Pilot test report | Project management | 22/12/2026 | M9 |
| D11 | Release candidate | Solution | 27/12/2026 | M10 |
| D12 | Final report | Project management | 27/12/2026 | M10 |
| D13 | Datasheet for Q&A Generation-Dataset v1 | Solution | 16/11/2026 | M5 |

## Sprint 1

| Project Deliverable #: | D1: Document set and Dataset Report |
|---|---|
| Description: | The final list of legal texts the assistant draws on (the Highway Traffic Law No. 2918, the Highway Traffic Regulation and the four regulations added to widen the document set (driver courses, health requirements for drivers, vehicle inspection, electric scooters)), the text of each stored as a file in the Git repository, and a report that records the source and size of each text. |
| Acceptance Criteria: | 1. Every text in the list is taken from its official source (the consolidated text on mevzuat.gov.tr or the Resmî Gazete), in its Word version where available and otherwise as a PDF, and its URL and retrieval date are recorded. 2. Every text is stored in the repository as its original file and one clean plain-text file. 3. The report states the number of articles and the token count of each text. 4. A check of 20 articles, chosen at random across the texts, against the official source finds 20 of 20 identical. 5. The list of texts in the report is the same as the list in the Scope Definition of [Project Executive Summary](01-project-executive-summary.md). |
| Due Date: | 21/10/2026 |
| Stakeholders: | Project team (AI developer role); Data provider: EGM Legal Department, which would keep these texts up to date after deployment |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D2: Q&A Generation-Dataset v1 |
|---|---|
| Description: | 40 questions with an answer key, used to evaluate retrieval and answers in every sprint: 30 questions the document set can answer and 10 it cannot. The questions are collected from real user questions (institutional FAQ pages, forums found by keyword search) and from target users; synthetic questions fill only question types with too few real questions and are labelled as synthetic. The answer key is written from the legal texts before any system is tested. Each question carries one type tag: answered from a single article; needs two or more articles of one text; needs articles from two or more texts; a violation described in the user's own words; out of scope. Each question also carries an ambiguity label: whether the question is ambiguous, that is, whether the answer key gives different answers depending on a condition the question does not state. The missing condition is one of four types (vehicle type, driver status, location, repeat offence), following Zamani et al. (2020). An ambiguous question also records its missing condition, a scripted user reply to the clarifying question and the answer key entry for that reply. The ambiguity labels are the reference against which the assistant's decision to ask a clarifying question is scored (D6, D8; Risk R-15). Example: a question about the penalty for drunk driving that does not say whether the driver is a commercial driver or whether it is a repeat offence, when the Law gives different sanctions for these cases. Stored as a file in the Git repository; every decision behind the set is logged in its datasheet (D13). |
| Acceptance Criteria: | 1. The file holds 30 in-scope and 10 out-of-scope questions, each with one type tag. 2. Diversity: each of the four in-scope types has at least 5 questions. 3. Representation: every text in D1 is the source of at least 3 questions, and at least 15 of the 30 in-scope questions are traced to a real user question whose source is recorded. 4. Every in-scope question has an answer key entry that names the supporting article or articles, and a second team member has checked 30 of 30 entries against the legal text. 5. Every out-of-scope question has the expected response "declines" recorded, and the out-of-scope group includes requests for advice on an individual case and prompt-injection attempts. 6. At least 5 of the 30 in-scope questions are follow-ups that depend on another question in the set. 7. Every question is labelled as ambiguous or not; 4 of the 30 in-scope questions are ambiguous, each with its missing condition and a scripted user reply to the clarifying question. 8. At most 10 of the 30 in-scope questions are synthetic, each labelled as such. |
| Due Date: | 26/10/2026 |
| Stakeholders: | Project team (AI developer role); Quality Team |
| Approving Stakeholder(s): | Business Analyst |

| Project Deliverable #: | D3: Default-state measurement report |
|---|---|
| Description: | Results of the timed test in which participants answer questions with the official texts and a web search, without the assistant. It holds the default-state value of Objective 1: a median of 77 seconds. |
| Acceptance Criteria: | 1. 10 participants took part, each a licensed driver or a driving-licence candidate. 2. Each participant answered 3 questions from D2, and the time of all 30 attempts is recorded. 3. Each attempt is marked correct or incorrect against the D2 answer key. 4. The report states the median time to a correct answer and the median number of places consulted. 5. The default-state value written under Objective 1 in [Project Executive Summary](01-project-executive-summary.md) equals the median time in this report. |
| Due Date: | 26/10/2026 |
| Stakeholders: | Project Review Committee; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D4: Project Charter v1 |
|---|---|
| Description: | Final version of all Project Canvas pages. |
| Acceptance Criteria: | 1. Every cell marked as required in the canvas templates is filled. 2. Every objective has at least one numeric success criterion. 3. Every milestone in [Milestones](02-milestones.md) has an associated deliverable on this page under the same number and name. 4. The feedback given at the Sprint 0 pitch is listed item by item, each with the page that addresses it or the reason it is not addressed. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Project Review Committee; project team |
| Approving Stakeholder(s): | Product Owner |

## Sprint 2

| Project Deliverable #: | D5: Long-context baseline experiment card |
|---|---|
| Description: | Results of a long-context model that receives the full document set (D1), with no retrieval, on all 40 questions of D2. It is the comparison point for the RAG results in D6 and D8. |
| Acceptance Criteria: | 1. All 40 questions are run, and the model name, model version, prompt and settings are recorded. 2. Each in-scope answer is scored correct or incorrect automatically, against the D2 answer key (Architecture AD-12), and each named article is scored as supporting or not supporting the answer. 3. The card reports, by question type: share of correct answers, share of answers that name a supporting article, number of out-of-scope questions declined (of 10), mean cost per question in USD and median response time in seconds. |
| Due Date: | 11/11/2026 |
| Stakeholders: | Project team (AI developer role); Project Review Committee |
| Approving Stakeholder(s): | Business Analyst |

| Project Deliverable #: | D6: RAG baseline experiment card |
|---|---|
| Description: | Results of the first RAG pipeline (one chunk per article) on all 40 questions of D2, set side by side with D5. It holds the first trial runs against which the Objective 2 levels are checked. |
| Acceptance Criteria: | 1. All 40 questions are run through the pipeline of D7, and the generation model, embedding model, reranking model, number of retrieved chunks (k), number of chunks kept after reranking and prompt are recorded. 2. The card reports the five measures of D5, by question type, in one table with the D5 values. 3. The card reports Recall@k: the share of in-scope questions for which at least one supporting article of the answer key is among the retrieved chunks. 4. At least one run uses the same generation model as D5. 5. For each of the two 80% levels of Objective 2, the card states the measured value next to the level. 6. The card reports the precision and recall of the decision to ask a clarifying question against the ambiguity labels of D2, and answer accuracy after clarification. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project team (AI developer role); Project Review Committee; Quality Team |
| Approving Stakeholder(s): | Business Analyst |

| Project Deliverable #: | D7: Alpha prototype |
|---|---|
| Description: | First integrated build of the assistant: a web chat interface connected to the RAG pipeline over the document set of D1. It runs on a team laptop. |
| Acceptance Criteria: | 1. A question typed in Turkish into the web interface returns an answer in Turkish: 40 of 40 D2 questions return a response without an error. 2. Every answer to an in-scope question shows at least one article reference (name of the text and article number). 3. The number of distinct article IDs in the index equals the number of articles reported in D1 (550). 4. A second team member starts the alpha from a clean copy of the repository by following the README: yes or no. |
| Due Date: | 18/11/2026 |
| Stakeholders: | AI customer: General Directorate of Security (EGM); AI users: drivers and driving-licence candidates |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D13: Datasheet for Q&A Generation-Dataset v1 |
|---|---|
| Description: | A datasheet for the question set and answer key of D2, kept in the [Datasheets](../11-datasheets/README.md) pages, that logs every decision that led to the dataset: why it was created, where the questions came from, how they were selected, labelled and checked, and what its limits are. It follows the questions of Gebru et al., "Datasheets for Datasets" (2021). |
| Acceptance Criteria: | 1. Motivation: the purpose of the set (measurement of Objectives 2 and 4) and who created it are stated. 2. Collection: every source is listed with its URL, access date, the keywords used to search it and the result of the terms-of-use check (A-05). 3. Selection: the numbers of questions collected, rejected and kept are stated, with the reason for each group of rejected questions (for example, procedural FAQ questions that the six texts cannot answer). 4. Composition: one table gives the number of questions by question type, by source text, real or synthetic, follow-up or not, and ambiguous or not with the type of missing condition; every number matches the D2 file. 5. Synthetic questions: for each, how it was written (by hand, or with a named model and prompt) and which question type needed it. 6. Labelling and answer key: the definitions of the five question types and of the ambiguity label, who wrote the answer key and the result of the second member's check (30 of 30). 7. Privacy: forum questions are stored without user names or licence plates (C-12). 8. Versioning and maintenance: the freeze date of v1 (26/10/2026), the D1 retrieval dates the answer key rests on and the effect of an amendment (C-02, R-05). 9. Known limitations, including how far the set represents the questions of real users. |
| Due Date: | 16/11/2026 |
| Stakeholders: | Project team (AI developer role); Quality Team; Project Review Committee |
| Approving Stakeholder(s): | Product Owner |

## Sprint 3

| Project Deliverable #: | D8: MVP validation experiment card |
|---|---|
| Description: | Results of the beta (D9) on the fixed set of 30 in-scope questions and the 10 out-of-scope questions of D2. It holds the measurement of Objective 2. |
| Acceptance Criteria: | 1. All 40 questions are run on the build delivered as D9, and the settings are recorded. 2. Each in-scope answer is scored automatically against the D2 answer key; the scoring configuration and threshold are recorded. 3. The card states the share of correct answers and the share of answers that name a supporting article, each next to its Objective 2 target. 4. The card reports the five measures of D5 and Recall@k by question type, in one table with the D5 and D6 values. 5. The card reports the precision and recall of the decision to ask a clarifying question against the ambiguity labels of D2, and answer accuracy after clarification, next to the D6 values. |
| Due Date: | 09/12/2026 |
| Stakeholders: | AI customer: General Directorate of Security (EGM); Project Review Committee; Quality Team |
| Approving Stakeholder(s): | Business Analyst |

| Project Deliverable #: | D9: Beta release |
|---|---|
| Description: | Build of the assistant that the pilot participants use in the Sprint 4 test. It contains the four features of the Scope Definition: questions in the user's own words, article reference, sanctions for a violation and out-of-scope handling. |
| Acceptance Criteria: | 1. On the 30 in-scope questions of D2, at least 80% of answers are correct and at least 80% of answers name an article that supports the answer (Objective 2; results in D8). 2. Every answer to an in-scope question shows the article reference and the quoted provision. 3. 40 of 40 D2 questions return a response without an error. 4. Every item recorded in the go/no-go decision of M6 is closed or has a recorded reason for staying open. |
| Due Date: | 09/12/2026 |
| Stakeholders: | AI customer: General Directorate of Security (EGM); AI users: pilot participants (drivers and driving-licence candidates) |
| Approving Stakeholder(s): | Product Owner; Business Analyst |

## Sprint 4

| Project Deliverable #: | D10: Pilot test report |
|---|---|
| Description: | Results of the timed usability test and the post-test survey with the pilot participants, and of the out-of-scope test. It holds the measurements of Objectives 1, 3 and 4 and the survey counts for the business outcomes. |
| Acceptance Criteria: | 1. 10 participants completed 3 timed questions each with the beta (30 attempts) and the post-test survey, and the report states how many of them also took part in D3. 2. The report states the median time to a correct answer, next to the target of under 77 seconds, the default-state value of D3 (Objective 1). 3. The report states how many participants would use the assistant again and how many rate the answers 4 or 5 for clarity on the 5-point scale, each next to the target of 7 of 10 (Objective 3). 4. The report states how many of the 10 out-of-scope questions were declined with the expected response, as checked automatically against the fixed refusal sentence (Objective 4). 5. The report gives the survey count for each business outcome of Objectives 1 to 4. 6. Every survey question cites the published instrument or source it is taken from. |
| Due Date: | 22/12/2026 |
| Stakeholders: | AI customer: General Directorate of Security (EGM); Project Review Committee |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D11: Release candidate |
|---|---|
| Description: | Final build of the assistant, with the changes made after the pilot. It is the build shown in the live demo. |
| Acceptance Criteria: | 1. Re-run after the last change, on the 30 in-scope questions of D2: at least 80% of answers are correct and at least 80% name an article that supports the answer. 2. 10 of 10 out-of-scope questions of D2 are declined with a statement that the document set does not cover the topic (Objective 4). 3. The question set supplied by the Project Review Committee, not seen by the team before, is run in full and every answer is recorded. 4. In the live demo, every question of the demo script returns a response without an error. |
| Due Date: | 27/12/2026 |
| Stakeholders: | AI customer: General Directorate of Security (EGM); AI users: drivers and driving-licence candidates |
| Approving Stakeholder(s): | Project Review Committee, acting for the AI customer; Product Owner |

| Project Deliverable #: | D12: Final report |
|---|---|
| Description: | Report of the project's results against its objectives, with the lessons learned. |
| Acceptance Criteria: | 1. For each of the four objectives, the report states the target, the measured value and the deliverable that holds the measurement (D3, D8, D10 or D11). 2. Every metric in the report links to an experiment card (D5, D6 or D8) or to D10. 3. The lessons learned section has at least one entry for each of the four sprints. |
| Due Date: | 27/12/2026 |
| Stakeholders: | Project Review Committee; AI customer: General Directorate of Security (EGM) |
| Approving Stakeholder(s): | Project Review Committee |
