# Story Requirements for Epic 03 · Web interface

<!-- Exported from Jira on 2026-10-24 (project CHUNKY). Jira is the source of truth for this backlog;
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
| S1 | US-09 Use the assistant in a web interface | As a driver, I want to use the assistant in my web browser, so that I need to install nothing. |  | 5 | Barış SAKA | Sprint 2 | To Do | [CHUNKY-125](https://chunky-502.atlassian.net/browse/CHUNKY-125) |
| S2 | US-11 Get an answer quickly | As a driver, I want to receive the answer within seconds, so that I can get it while I am preparing or checking a rule. |  | 3 |  | Sprint 3 | To Do | [CHUNKY-133](https://chunky-502.atlassian.net/browse/CHUNKY-133) |
| S3 | US-10 See example questions when I open the page | As a driving-licence candidate, I want to see example questions when I open the page, so that I know what to ask. |  | 2 |  | Sprint 4 | To Do | [CHUNKY-139](https://chunky-502.atlassian.net/browse/CHUNKY-139) |

## S1 · US-09 Use the assistant in a web interface

**Acceptance criteria**

- When the user opens the web address, the interface shall show a question box and an answer area.
- The system shall display all interface elements, including buttons, placeholders, and error messages, in Turkish.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Write all interface texts in Turkish and check them | Zehranur KUTLUYER |  | To Do | [CHUNKY-166](https://chunky-502.atlassian.net/browse/CHUNKY-166) |

## S2 · US-11 Get an answer quickly

**Acceptance criteria**

- When the user submits a question, the interface shall show a progress indicator until the answer appears.
- When the user submits a question, the assistant shall return the complete answer within 60 seconds.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Add the progress indicator |  |  | To Do | [CHUNKY-190](https://chunky-502.atlassian.net/browse/CHUNKY-190) |
| Measure the response time on the 40 questions and optimise if needed |  |  | To Do | [CHUNKY-191](https://chunky-502.atlassian.net/browse/CHUNKY-191) |

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
