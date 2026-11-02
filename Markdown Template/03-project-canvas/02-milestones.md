# Milestones

**Project:** Traffic rules and penalties assistant · **Team:** Chunky

Each milestone below is a state that is true on its date. The deliverables that prove it are listed by number and name as they appear in [Deliverables](05-deliverables.md). Sprint dates are in [Release Plan](10-release-plan.md).

From Sprint 2 on, each milestone is dated at least two days after the deliverables that prove it are due, so that they can be reviewed before the milestone is recorded; the go/no-go checkpoints M6 and M8 come five days after their deliverables. M10 cannot move past 30/12/2026 (C-09), so D11 and D12 are due on 27/12/2026.

## Milestone table

| # | Project Milestone | Description | Expected Date | Associated Deliverable |
|---|---|---|---|---|
| M1 | Document set finalised | The list of legal texts the assistant draws on is fixed: the Highway Traffic Law No. 2918, the Highway Traffic Regulation and the four regulations added to widen the document set (driver courses, health requirements for drivers, vehicle inspection, electric scooters). Each text is taken from its official source and stored in the repository with its source, retrieval date, article count and token count. Product Owner approves the list, and the Scope Definition in [Project Executive Summary](01-project-executive-summary.md) names the same texts. | 21/10/2026 | D1 Document set and Dataset Report |
| M2 | Default state measured on question set v1 | Question set v1 is frozen: 30 in-scope and 10 out-of-scope questions, drawn from real user questions (institutional FAQ pages, forums) and input from target users, tagged by question type, with an answer key written from the legal texts. 10 participants have each answered 3 comparable questions with the official texts and a web search. The median time and the number of places consulted are recorded, and the default-state value of Objective 1 (77 seconds) is recorded. | 26/10/2026 | D2 Q&A Generation-Dataset v1; D3 Default-state measurement report |
| M3 | Charter v1 approved | All charter pages are filled in and refer to each other by number; this is the final version of the charter. Product Owner signs off the charter after the Sprint 1 review. | 28/10/2026 | D4 Project Charter v1 |
| M4 | Long-context baseline measured on the full question set | A long-context model that receives the full document set (D1), with no retrieval, has answered all 40 questions of D2. Correctness, article citation, refusal of out-of-scope questions, cost per question and response time are logged by question type in an experiment card. | 13/11/2026 | D5 Long-context baseline experiment card (due 11/11/2026) |
| M5 | Alpha answers the full question set end to end | A question typed in Turkish into the web interface returns an answer with its article reference. The RAG pipeline (one chunk per article) has run on all 40 questions of D2, and its results stand next to the long-context baseline (D5) in an experiment card. The 80% levels of Objective 2 are checked against these runs; they are not changed, because the charter is final at M3. The question set behind these runs is documented in its datasheet (D13). | 20/11/2026 | D6 RAG baseline experiment card; D7 Alpha prototype (both due 18/11/2026); D13 Datasheet for Q&A Generation-Dataset v1 (due 16/11/2026) |
| M6 | Checkpoint: go/no-go for beta | Product Owner reviews the alpha, its comparison with the long-context baseline and the Quality Team's Sprint 2 review, and records the decision on what changes before Sprint 3 starts. | 23/11/2026 | D6 RAG baseline experiment card; D7 Alpha prototype (both due 18/11/2026) |
| M7 | MVP validated: Objective 2 measured | The beta has answered the fixed set of 30 in-scope questions. The share of correct answers and the share of answers that name a supporting article are scored against the answer key (target: at least 80% each) and reported by question type next to both baselines. The decision to ask a clarifying question is scored against the ambiguity labels of D2 (precision and recall). | 11/12/2026 | D8 MVP validation experiment card; D9 Beta release (both due 09/12/2026) |
| M8 | Checkpoint: go/no-go for pilot | Product Owner and Business Analyst review the Objective 2 results and decide whether the beta goes to the pilot participants as it is. | 14/12/2026 | D8 MVP validation experiment card; D9 Beta release (both due 09/12/2026) |
| M9 | Pilot completed: Objectives 1, 3 and 4 measured | 10 participants have completed the timed usability test (3 questions each) and the post-test survey. The 10 out-of-scope questions have been run and checked automatically against the fixed refusal sentence. Median time to a correct answer, survey scores and refusal rate are recorded against their targets. | 24/12/2026 | D10 Pilot test report (due 22/12/2026) |
| M10 | Release candidate accepted | The release candidate has been evaluated on a question set the team has not seen and runs in the live demo. The Project Review Committee, acting for the AI customer, accepts it. | 30/12/2026 | D11 Release candidate; D12 Final report (both due 27/12/2026) |

## Where each objective is measured

Each target in [Project Executive Summary](01-project-executive-summary.md) that is measured later has a milestone that dates the measurement and a deliverable that holds the result.

| Objective | What is measured | Milestone | Deliverable that holds the result |
|---|---|---|---|
| 1 | Default state: median time and number of places consulted without the assistant | M2 (26/10/2026) | D3 Default-state measurement report |
| 1 | Median time to a correct answer with the assistant (target: under 77 seconds) | M9 (24/12/2026) | D10 Pilot test report |
| 2 | First trial runs; the 80% levels checked | M5 (20/11/2026) | D6 RAG baseline experiment card |
| 2 | Correct answers and supported article references on 30 questions (target: at least 80% each) | M7 (11/12/2026) | D8 MVP validation experiment card |
| 3 | Would use again and clarity rating (target: at least 7 of 10 participants each) | M9 (24/12/2026) | D10 Pilot test report |
| 4 | Refusal on 10 out-of-scope questions | M9 (24/12/2026) | D10 Pilot test report |

Evaluation takes place in every sprint: M2 in Sprint 1, M4 and M5 in Sprint 2, M7 in Sprint 3, M9 and M10 in Sprint 4.
