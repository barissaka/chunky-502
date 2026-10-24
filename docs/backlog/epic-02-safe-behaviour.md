# Story Requirements for Epic 02 · Safe behaviour

<!-- Exported from Jira on 2026-10-24 (project CHUNKY). Jira is the source of truth for this backlog;
     this file is a snapshot for the sprint deliverable and is regenerated before each sprint review. -->

| Epic | Safe behaviour |
|---|---|
| Summary | The assistant declines outside its documents, explains failures in plain language, and keeps personal data private. Done when: US-06 to US-08 are done and 10 of 10 out-of-scope questions are declined in D10. |
| Document Owner |  |
| Release Target (Sprint) |  |
| Status | To Do |
| Jira | [CHUNKY-117](https://chunky-502.atlassian.net/browse/CHUNKY-117) |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Status | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | US-06 Decline when the assistant does not know | As a driver, I want the assistant to say so when my question is outside its documents, so that I am not misled by a made-up answer. |  | 5 |  | Sprint 3 | To Do | [CHUNKY-130](https://chunky-502.atlassian.net/browse/CHUNKY-130) |
| S2 | US-07 Understand what went wrong | As a driver, I want a clear message when something fails, so that I know whether to wait, retry or rephrase. |  | 5 |  | Sprint 3 | To Do | [CHUNKY-131](https://chunky-502.atlassian.net/browse/CHUNKY-131) |
| S3 | US-08 Keep my personal data private | As a driver, I want my personal data not to be saved, so that I can ask about my own violations without worry. |  | 3 |  | Sprint 3 | To Do | [CHUNKY-132](https://chunky-502.atlassian.net/browse/CHUNKY-132) |

## S1 · US-06 Decline when the assistant does not know

**Acceptance criteria**

- When the user asks a question that the document set does not cover, the assistant shall state that the document set does not cover the topic, and shall not give a made-up answer.
- If the user asks for advice on an individual case (for example, whether to contest a penalty), then the assistant shall state what the texts say and shall not advise on the case.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Design and implement out-of-scope detection with the Turkish decline statement |  |  | To Do | [CHUNKY-181](https://chunky-502.atlassian.net/browse/CHUNKY-181) |
| Implement the individual-case rule |  |  | To Do | [CHUNKY-182](https://chunky-502.atlassian.net/browse/CHUNKY-182) |
| Test 10 out-of-scope and 5 individual-case questions |  |  | To Do | [CHUNKY-183](https://chunky-502.atlassian.net/browse/CHUNKY-183) |

## S2 · US-07 Understand what went wrong

**Acceptance criteria**

- If the assistant cannot produce an answer because of a system failure, then the interface shall show an error message in Turkish that says what happened and what the user can do next.
- If the answer takes longer than 60 seconds, then the interface shall tell the user that the answer is delayed and offer a retry.
- If an error occurs, then the interface shall keep the user's typed question on the screen.
- The interface shall not show technical details (stack traces, internal codes) in the error message.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| List failure cases and write the Turkish message for each |  |  | To Do | [CHUNKY-184](https://chunky-502.atlassian.net/browse/CHUNKY-184) |
| Implement the error handling, delay notice (60 s) and retry button; keep the typed question |  |  | To Do | [CHUNKY-185](https://chunky-502.atlassian.net/browse/CHUNKY-185) |
| Simulate each failure |  |  | To Do | [CHUNKY-186](https://chunky-502.atlassian.net/browse/CHUNKY-186) |

## S3 · US-08 Keep my personal data private

**Acceptance criteria**

- The assistant shall not ask for the user's name, ID number, licence number or plate number.
- The assistant shall not require an account or login.
- When the user closes the chat page, the system shall not keep the conversation content linked to the user.
- Where the user types personal data into a question, the assistant shall not store it beyond the open chat.
- The interface shall show a one-sentence privacy notice that says personal data is not saved.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Decide what logs may contain and keep the history in the open session only |  |  | To Do | [CHUNKY-187](https://chunky-502.atlassian.net/browse/CHUNKY-187) |
| Mask personal data before it is logged |  |  | To Do | [CHUNKY-188](https://chunky-502.atlassian.net/browse/CHUNKY-188) |
| Add the privacy notice and review logs and API calls |  |  | To Do | [CHUNKY-189](https://chunky-502.atlassian.net/browse/CHUNKY-189) |
