# Major Activities

Expand on the scope definition by outlining the major activities required to complete the project. Structure these around the AI system life cycle stages of ISO/IEC 5338 [1], listed below.

Include activities such as project management, feature engineering, model training, performance evaluation and analysis.

Mark each activity as In Scope or Out of Scope to reduce ambiguity.

Add rows as required. The table should give a summary view; add narrative explanation below it where more detail is needed. Activities can be linked to Jira from this page.

## Life cycle stages
 
Give every activity one stage from this table. The stage names and the processes in each stage come from ISO/IEC 5338 [1]; the typical activities are paraphrased for this course.
 
| Stage | Typical activities | ISO/IEC 5338 processes in this stage |
|---|---|---|
| **Inception** | Define the problem, the AI customer's needs and the success criteria; set model requirements; decide whether AI is needed at all | 6.4.1 Business or mission analysis; 6.4.2 Stakeholder needs and requirements definition; 6.4.3 System requirements definition |
| **Design and development** | Architecture and design; acquire, label, explore, clean and prepare data; protect sensitive data; feature engineering; train and tune models; integrate components | 6.4.4–6.4.6; 6.4.7 Knowledge acquisition; 6.4.8 AI data engineering; 6.4.9 Implementation; 6.4.10 Integration |
| **Verification and validation** | Test the model and system before deployment; check them against the AI customer's needs | 6.4.11 Verification; 6.4.13 Validation |
| **Deployment** | Move the model and system into the environment where AI users reach it | 6.4.12 Transition |
| **Operation and monitoring** | Run the system; fix and retrain it when needed | 6.4.15 Operation; 6.4.16 Maintenance |
| **Continuous validation** | Monitor data drift, concept drift and other changing requirements after deployment; decide when to retrain | 6.4.14 Continuous validation |
| **Re-evaluation** | Review results against the original needs; feed changes back to Inception or Design and development | 6.3.8 Quality assurance; 6.4.2; 6.4.13 |
| **Retirement** | Decommission the system and its data | 6.4.17 Disposal |
 
Project management work (sprint planning, documentation, reviews, risk tracking) runs across every stage, as risk management and governance do in the standard [1]. Write **All stages** for these rows.
 
Stages group work in a rough order, but they need not happen one after another. In agile work, stages can run at the same time and can repeat [1].

## In Scope and Out of Scope

| Status | What it means | Question it answers |
|---|---|---|
| **In Scope** | Work the team will do | What will we build or carry out? |
| **Out of Scope** | Work the team will not do at all | What are we deliberately not building? |

An out-of-scope activity is not the same as a constraint. A constraint is a rule that limits how the in-scope work is done; it goes in [Assumptions & Constraints](03-assumptions-and-constraints.md). If you want to show that the project's scope is narrow (for example, you plan no information-elicitation phase), list that here as Out of Scope. Limits on the system's inputs, such as a user-input boundary or English-only text, are constraints.

## Activities that come from a constraint

Many constraints create work and remove work at the same time. Write the decision as three statements, one per place, each pointing to the others:

| Where | What it says | Example wording |
|---|---|---|
| Constraint ([Assumptions & Constraints](03-assumptions-and-constraints.md)) | The rule the system must obey | "The system shall not persist personally identifiable information (e.g., names, email addresses, national ID numbers) in any database, log, or vector index." |
| In Scope (this page) | The work you do because of the constraint | "Implement PII detection and masking on user inputs before logging." "Configure logs to retain only anonymised interaction data." |
| Out of Scope (this page) | The features you give up because of it | "User accounts, personal profiles, and saved conversation history linked to an identity." |

**Do not skip the In Scope row.** Users will type names, emails or account numbers into a chatbot whether you invite them to or not. A rule such as "no PII stored" is not true just because you did not build a profile feature; enforcing it takes work. That work belongs here, in the backlog and in the estimates. Count its effort in [Cost & Funding](07-cost-and-funding.md).

The uncertain part becomes a risk in [Risks](11-risks.md), and the in-scope activity is its mitigation. For the example above, the risk is "Users submit PII in free-text queries, and it ends up in logs or the retrieval index".

## Knock-on effect on user stories

Once a constraint is in the charter, a user story that contradicts it is an inconsistency between documents. The review error types call this an External Inconsistency. For example, "As a returning analyst, I want to see my previous questions" contradicts a no-PII rule. Either drop such a story, or rewrite it so the history lives only in the session and is not stored.

## Rules

1. Every activity has exactly one stage from the life cycle table above, spelled as there, or **All stages** for project management work.
2. Every activity is marked In Scope or Out of Scope.
3. Every Out of Scope row says why in its Description, as row 2 below does.
4. Every constraint in [Assumptions & Constraints](03-assumptions-and-constraints.md) that creates work has at least one In Scope row here, and every constraint that removes features has at least one Out of Scope row here.
5. Rows created by a constraint name the constraint ID in their Description (for example "Because of C-03").
6. User authentication and PII storage, if you do not plan them, are listed as Out of Scope.
7. Activities do not increase the scope of the project beyond the first proposal.

## What doesn't belong here

- **Rules the system must obey** go in [Assumptions & Constraints](03-assumptions-and-constraints.md) as constraints.
- **What could go wrong** with an activity goes in [Risks](11-risks.md).
- **The order in which activities must happen**, when one blocks another, goes in [Dependencies](06-dependencies.md).
- **Effort in person-hours** goes in [Cost & Funding](07-cost-and-funding.md).

## Activities
 
| # | Stage | Activity | Description | Status | Jira Task |
|---|---|---|---|---|---|
| 1 | Inception | Define the assistant's purpose, users and success criteria | Completed as part of project chartering (see Project Executive Summary). | In Scope | |
| 2 | Inception | Market/competitive analysis of existing traffic-information products | Not needed for an academic proof-of-concept. | Out of Scope | |
| 3 | Inception | Measure the default state for Objective 1 | 10 participants each answer 3 comparable questions with the official texts and a web search; median time and number of places consulted are recorded (M2, D3). 12 people are invited so that 2 are in reserve. Mitigation for R-03. | In Scope | |
| 4 | Design and development | Build the document set from official sources | Because of C-01. The six texts are taken from their official consolidated versions (the Word version where available, otherwise the PDF) and stored with source, retrieval date, article count and token count (M1, D1); the original file and one clean .txt file per text are kept in the repository; the token count is 255,138 in total (tiktoken o200k_base). Checks A-01. Mitigation for R-01. | In Scope | |
| 5 | Design and development | Record the retrieval date of each text and check amendment dates at each sprint start | Because of C-02. The retrieval date of each text is recorded in D1. At the start of each sprint, the last amendment date of each text on its official source is compared with that date. The document set and the answer key are not updated when a text is amended; the questions affected are listed as a limitation in the final report (D12). Mitigation for R-05. | In Scope | |
| 6 | Design and development | Collect and tag question set v1 and write its answer key | Because of C-01, C-05 and C-13. 30 in-scope and 10 out-of-scope questions selected from the EGM FAQ page and public forums (searched by keyword), kept in their original wording with source, URL, access date and question type; the terms of use of each source are read before collecting. The answer key is written from the legal texts (M2, D2). FAQ answers are not added to the document set; FAQ questions that the six texts cannot answer go to the out-of-scope group, together with questions asking for advice on an individual case and prompt-injection attempts. Synthetic questions may fill question types with too few real questions; they are labelled as synthetic, are at most 10 of the 30 in-scope questions, are checked by the Business Analyst / Domain Expert and have answer keys written from the legal texts. At least 5 of the 30 in-scope questions are follow-ups that depend on another question in the set. Every question is labelled as ambiguous or not and, if ambiguous, with the missing condition (vehicle type, driver status, location, repeat offence); 4 of the 30 in-scope questions are ambiguous, and each has a scripted user reply to the clarifying question. Checks A-02 and A-05. Mitigation for R-02 and R-06. | In Scope | |
| 7 | Design and development | Split the texts into one chunk per article and build the retrieval index | Because of C-04. Articles longer than the embedding input limit get retrieval-only sub-chunks with the same article ID (Architecture AD-08). | In Scope | |
| 8 | Design and development | Build the RAG answer pipeline with article reference and quoted provision | Because of C-04, C-05 and C-14. Retrieved articles are reranked, and answers are generated only from the top-ranked articles and name the article they rest on (Features 1–3). The language, embedding and reranking models run locally through Ollama; the language model is reached through a provider-agnostic gateway (Architecture AD-03). | In Scope | |
| 9 | Design and development | Out-of-scope handling | Because of C-01, C-05 and C-11. The assistant declines questions outside the document set and requests for advice on an individual case (Feature 4). Mitigation for R-07. | In Scope | |
| 10 | Design and development | Mask personal data in user inputs before logging | Because of C-12. Names, national ID numbers and licence plates are detected and masked before any log write. Mitigation for R-10. | In Scope | |
| 11 | Design and development | Build the Turkish web interface | Because of C-03. A question typed in Turkish returns an answer in Turkish with its article reference (D7). | In Scope | |
| 12 | Verification and validation | Run the long-context baseline on the full question set | Because of C-04 and C-06. A long-context model with a context window of at least 1 million tokens, hosted on Google Cloud or Azure, receives the document set with no retrieval, at three sizes: Law only (77,985 tokens), Law + Regulation (179,015) and the full set (255,138). Correctness, article citation, refusal, cost per question and response time are logged by question type (M4, D5). The Law-only run goes first and its cost is checked before the larger runs. Mitigation for R-04. | In Scope | |
| 13 | Verification and validation | Evaluate the RAG pipeline against the answer key | Results by question type, next to the long-context baseline (M5, D6; M7, D8). Measures Objective 2. The ask decision is reported as precision (the assistant asked and asking was needed) and recall (asking was needed and the assistant asked) on the ambiguity labels, together with answer accuracy after clarification (steps 1 and 3 of Zhang & Choi, 2025 [3]). Answers are scored automatically against the answer key by a hosted judge model that differs from the answer-generating model; the scoring configuration and threshold are fixed before M5 (Architecture AD-12). Because of C-06, the versions of the hosted models and the tags of the local Ollama models are pinned in the configuration for the runs in rows 12 and 13, and each run is scheduled at least 3 days before its milestone. Mitigation for R-11, R-12, R-13 and R-17. | In Scope | |
| 14 | Verification and validation | Run the pilot: timed usability test, post-test survey and out-of-scope test | 10 participants, 3 questions each; 10 out-of-scope questions reviewed against the expected response (M9, D10). Measures Objectives 1, 3 and 4. | In Scope | |
| 15 | Verification and validation | Evaluate the release candidate on a question set the team has not seen | M10, D11, D12. | In Scope | |
| 16 | Deployment | Run the prototype on the host laptop for the pilot and the live demo; track the spend of hosted model calls weekly | Because of C-06, C-08 and C-14. PC 2 is the spare host; a local-model configuration is kept ready in case there is no internet connection (Architecture AD-03). Budget alerts are set at 50% and 75% of the credit. Mitigation for R-08, R-18 and R-20. | In Scope | |
| 17 | Deployment | Configure logs to keep only anonymised interaction data | Because of C-12. Mitigation for R-10. | In Scope | |
| 18 | All stages | Project management: sprint planning, charter, reviews and risk tracking | Project Charter v1, the final version of the charter (M3, D4), go/no-go checkpoints (M6, M8), risk register reviewed at each sprint start; the Scrum Master rotates each sprint, owners and contacts are spread over the four members, and every deliverable has a second named member who can take it over. Because of C-09 and C-10. Mitigation for R-09. | In Scope | |
| 19 | Design and development | Coverage of other legislation (compulsory insurance, motor vehicle tax, customs) and of the EGM FAQ answers | Because of C-01: the document set is limited to the six texts; FAQ questions are used only in the question set. | Out of Scope | |
| 20 | Design and development | Languages other than Turkish | Because of C-03. | Out of Scope | |
| 21 | Design and development | Handle follow-up questions within a session | Because of C-05 and C-12. The earlier turns of the same session are passed to retrieval and generation, so that a follow-up question that leaves out its topic is understood. The history lives only in the session and is not stored. Mitigation for R-14. | In Scope | |
| 22 | Design and development | Training or fine-tuning a language model | Because of C-04 (the solution is RAG) and C-08 (the budget does not cover training). | Out of Scope | |
| 23 | Design and development | Personal penalty, licence and vehicle record queries | Because of C-07: the assistant has no connection to EGM systems or e-Devlet. | Out of Scope | |
| 24 | Design and development | Advice on contesting an individual penalty | Because of C-11: the assistant states what the texts say and gives no advice on an individual case. | Out of Scope | |
| 25 | Design and development | User accounts, authentication and saved conversation history | Because of C-12: these would require storing personal data. | Out of Scope | |
| 26 | Deployment | Public release on the official EGM web page | Because of C-07 and C-09: the project delivers a release candidate shown in a live demo; public release would be done by the AI application provider. | Out of Scope | |
| 27 | Operation and monitoring | Updating the document set and the answer key after an amendment, and maintaining the assistant after the project ends | Because of C-02 and C-09: the document set is a fixed snapshot for the whole project. After deployment, the EGM information technologies unit would review reported answers (row 32) and fix the assistant, and the data provider (EGM Legal Department) would update the texts; an amendment published in the Resmî Gazete or a reported wrong answer would be the maintenance trigger. | Out of Scope | |
| 28 | Design and development | Clarification handling for ambiguous questions | Because of C-05. Before answering, the assistant checks whether a missing condition changes the answer: vehicle type (disambiguation), driver status (personal), location (spatial) and repeat offence (domain-specific), following the clarification types of Zamani et al. (2020) [2]. If one missing condition changes the answer, it asks one question and offers the options as buttons; if there are only a few options, it answers all of them in a short table; if the gap is small, it answers and states its assumption. Mitigation for R-15. | In Scope | |
| 29 | Design and development | Clarification dialogues of more than one turn | Because of C-05: after one clarifying question the assistant answers and states the condition it assumed. | Out of Scope | |
| 30 | Design and development | Query guard | Because of C-11 and C-13. Rule-based checks for prompt injection and for requests for advice on an individual case run before retrieval; a scope gate on the retrieval score sends questions outside the document set to the fixed refusal reply. Mitigation for R-07 and R-16. | In Scope | |
| 31 | Design and development | Fixed notice on fine amounts on the chat page | Feature 3: amounts are shown as written in the texts, and the notice states that fine amounts are revalued every year. | In Scope | |
| 32 | Design and development | Disclaimer, answer-report button and logging of reported answers | Because of C-11 and C-12. The chat page shows a permanent notice that the assistant can make mistakes and gives no advice on an individual case; every answer has a button to report it as wrong or out of scope; a reported answer is logged with its question after personal data is masked (row 10), and reported answers are reviewed weekly during the pilot. Mitigation for R-07, R-14, R-15 and R-16. | In Scope | |
| 33 | Inception | Identify the runtime environment of the AI customer | The hardware and hosting conditions under which the EGM information technologies unit would run the assistant are recorded, and the assistant is built to run under them. Checks A-06. Mitigation for R-19. | In Scope | |
 
## Example (illustrative only)
 
An excerpt from a longer table for a legal research assistant (a RAG chatbot over legal documents). It shows the rows created by constraints C-03 and C-04 in the example on `03-assumptions-and-constraints.md`.
 
| # | Stage | Activity | Description | Status | Jira Task |
|---|---|---|---|---|---|
| 7 | Design and development | Mask PII in user inputs before logging | Because of C-03. Detect names, emails and ID numbers in queries and mask them before any log write. Mitigation for R-03. | In Scope | (link) |
| 8 | Deployment | Configure logs to keep only anonymized interaction data | Because of C-03. | In Scope | (link) |
| 12 | Design and development | User accounts, personal profiles and saved conversation history | Because of C-03: these would require storing PII. | Out of Scope | |
| 13 | Design and development | Multi-turn dialogue memory | Because of C-04: the system handles single-turn questions only. | Out of Scope | |

## Checklist before submitting

- [ ] Every activity has one ISO/IEC 5338 life cycle stage, or All stages (rule 1)
- [ ] Every activity is marked In Scope or Out of Scope (rule 2)
- [ ] Every Out of Scope row says why (rule 3)
- [ ] Every work-creating constraint in [Assumptions & Constraints](03-assumptions-and-constraints.md) has an In Scope row, and every feature-removing constraint has an Out of Scope row (rule 4)
- [ ] Rows created by a constraint name its ID (rule 5)
- [ ] User authentication and PII storage are listed as Out of Scope if you do not plan them (rule 6)
- [ ] No activity goes beyond the first proposal's scope (rule 7)

## References

[1] ISO/IEC JTC 1/SC 42, *ISO/IEC 5338:2023 Information technology — Artificial intelligence — AI system life cycle processes*, 1st ed. Geneva, Switzerland: ISO and IEC, Dec. 2023.

[2] H. Zamani, S. Dumais, N. Craswell, P. Bennett and G. Lueck, "Generating Clarifying Questions for Information Retrieval," in *Proc. The Web Conference (WWW 2020)*, 2020.

[3] M. J. Q. Zhang and E. Choi, "Clarify When Necessary: Resolving Ambiguity Through Interaction with LMs," in *Findings of NAACL 2025*, 2025.
