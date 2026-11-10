# Story Requirements for Epic 03 · Web interface

<!-- Exported from Jira on 2026-11-10 (project CHUNKY). Jira is the source of truth for this backlog;
     this file is a snapshot for the sprint deliverable and is regenerated before each sprint review. -->

| Epic | Web interface |
|---|---|
| Summary | The web page through which users use the assistant: question box and answer area, Turkish interface texts, example questions, progress indicator and response time. Done when: US-09 to US-11 are done and every question of the live demo script returns a response without an error. |
| Document Owner |  |
| Release Target (Sprint) |  |
| Status | To Do |
| Jira | [CHUNKY-118](https://chunky-502.atlassian.net/browse/CHUNKY-118) |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Status | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | US-09 Use the assistant in a web interface | As a driver, I want to use the assistant in my web browser, so that I need to install nothing. |  | 5 | Barış SAKA | Sprint 2 | In Progress | [CHUNKY-125](https://chunky-502.atlassian.net/browse/CHUNKY-125) |
| S2 | US-11 Read the full answer within one minute | As a driver, I want to see that the assistant is working on my question and to read the full answer within one minute, so that I do not wonder whether the page is stuck while I am preparing or checking a rule. |  | 3 |  | Sprint 3 | To Do | [CHUNKY-133](https://chunky-502.atlassian.net/browse/CHUNKY-133) |
| S3 | US-10 See example questions when I open the page | As a driving-licence candidate, I want to see example questions when I open the page, so that I know what to ask. |  | 2 |  | Sprint 4 | To Do | [CHUNKY-139](https://chunky-502.atlassian.net/browse/CHUNKY-139) |

## S1 · US-09 Use the assistant in a web interface

**Acceptance criteria**

- When the user opens the web address, the interface shall show a question box and an answer area.
- The system shall display all interface elements, including buttons and placeholders in Turkish.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Write all interface texts in Turkish and check them | Zehranur KUTLUYER |  | To Do | [CHUNKY-166](https://chunky-502.atlassian.net/browse/CHUNKY-166) |

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-09-1 | Question box and answer area | Open the web address in a browser with nothing installed. | A question box and an answer area are shown. |
| TC-09-2 | Everything in Turkish | Go through the page: buttons, placeholder, and an error message (stop the service). | All interface text is in Turkish. |

## S2 · US-11 Read the full answer within one minute

**Acceptance criteria**

- When the user submits a question, the interface shall show a progress indicator until the answer is displayed.
- When the user submits a question, the assistant shall display the complete answer within 60 seconds.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Add the progress indicator |  |  | To Do | [CHUNKY-190](https://chunky-502.atlassian.net/browse/CHUNKY-190) |
| Measure the response time on the 40 questions and optimise if needed |  |  | To Do | [CHUNKY-191](https://chunky-502.atlassian.net/browse/CHUNKY-191) |

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-11-1 | Progress indicator | Send a question and watch the screen. | A progress indicator shows from sending until the answer appears. |
| TC-11-2 | Complete answer within 60 seconds | Send the 40 questions of the question set and time each one. | Every complete answer appears within 60 seconds. |

## S3 · US-10 See example questions when I open the page

**Acceptance criteria**

- When the user opens the interface with an empty chat, the interface shall show at least 3 example questions.
- When the user selects an example question, the interface shall send it as the user's question.
- When the user sends the first question, the interface shall hide the examples.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Choose at least 3 example questions |  |  | To Do | [CHUNKY-204](https://chunky-502.atlassian.net/browse/CHUNKY-204) |
| Add the example buttons that send the question and hide after the first question |  |  | To Do | [CHUNKY-205](https://chunky-502.atlassian.net/browse/CHUNKY-205) |

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-10-1 | At least 3 examples | Open the interface with an empty chat. | At least 3 example questions are shown. |
| TC-10-2 | Example is sent | Select an example question. | It is sent as the user's question and an answer appears. |
| TC-10-3 | Examples hidden after first question | Send the first question. | The examples are hidden. |
