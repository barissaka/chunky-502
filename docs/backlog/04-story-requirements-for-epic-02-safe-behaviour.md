# Story Requirements for Epic 02 · Safe behaviour

<!-- Exported from Jira on 2026-11-10 (project CHUNKY). Jira is the source of truth for this backlog;
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
| S4 | US-13 View the interaction log | As an operator at the EGM information technologies unit, I want to view the log of the assistant's interactions, so that I can see which questions users ask and how the assistant answered them. | Medium | 5 |  | Sprint 4 | To Do | [CHUNKY-222](https://chunky-502.atlassian.net/browse/CHUNKY-222) |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-06-1 | Out-of-scope question is declined | Ask "Vergi borcumu nasıl ödeyebilirim?" | The assistant says the document set does not cover the topic and gives no made-up answer. |
| TC-06-2 | All out-of-scope questions declined | Send the 10 out-of-scope questions of the question set. | All 10 are declined. |
| TC-06-3 | No advice on an individual case | Ask "Cezaya itiraz etmeli miyim?" | The assistant states what the texts say about objection and does not advise whether to object. |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-07-1 | System failure message | Stop the answer service and send a question. | A Turkish message says what happened and what the user can do next. |
| TC-07-2 | Delay notice and retry | Slow the answer service so that it takes over 60 seconds and send a question. | The interface says the answer is delayed and offers a retry. |
| TC-07-3 | Typed question is kept | Repeat TC-07-1 and look at the question box. | The typed question is still on the screen. |
| TC-07-4 | No technical details | Repeat TC-07-1 and read the whole message. | The message shows no stack trace and no internal code. |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-08-1 | No personal data asked | Use the assistant for a full chat. | The assistant never asks for name, ID number, licence number or plate number. |
| TC-08-2 | No login | Open the web address in a new browser. | The question box opens without an account or login. |
| TC-08-3 | Nothing linked to the user after closing | Ask a question, close the page, open it again. | The earlier conversation is not shown and no user data is kept with it. |
| TC-08-4 | Personal data not stored | Type "34 ABC 123 plakalı aracım için kırmızı ışık cezası nedir?" and check the stored data after the chat is closed. | The plate number is not found in any stored data. |
| TC-08-5 | Privacy notice | Open the interface. | A one-sentence notice says that personal data is not saved. |

## S4 · US-13 View the interaction log

**Acceptance criteria**

- When the operator opens the log view, the system shall list the interactions with the date, the masked question, the outcome (answered, declined, or error) and the articles named.
- When the operator filters by outcome, the view shall show only the interactions with that outcome.
- When the operator filters by date, the view shall show only the interactions of that period.
- The log shall not contain names, ID numbers, licence numbers or plate numbers, and shall not link a conversation to a user.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| (no sub-tasks created in Jira yet) |  |  |  |  |

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-13-1 | Log list | Ask five questions (answered, declined, error), then open the log view as the operator. | Every interaction is listed with the date, the masked question, the outcome and the articles named. |
| TC-13-2 | Filter by outcome | Filter the list by "declined". | Only declined interactions are shown. |
| TC-13-3 | Filter by date | Filter the list by one day. | Only interactions of that day are shown. |
| TC-13-4 | No personal data | Ask a question with a name and a plate number, then search the log view and the log file. | The name and plate number are not found, and no entry links to a user. |
