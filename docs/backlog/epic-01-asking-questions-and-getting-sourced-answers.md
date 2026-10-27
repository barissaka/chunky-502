# Story Requirements for Epic 01 · Asking questions and getting sourced answers

<!-- Exported from Jira on 2026-10-27 (project CHUNKY). Jira is the source of truth for this backlog;
     this file is a snapshot for the sprint deliverable and is regenerated before each sprint review. -->

| Epic | Asking questions and getting sourced answers |
|---|---|
| Summary | Users ask in their own Turkish words, receive a correct answer with its article, continue the conversation, and see what the assistant covers. Done when: US-01 to US-05 are done and the Objective 2 targets are met in D8. |
| Document Owner |  |
| Release Target (Sprint) |  |
| Status | To Do |
| Jira | [CHUNKY-116](https://chunky-502.atlassian.net/browse/CHUNKY-116) |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Status | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | US-01 Ask in my own words | As a driver, I want to ask a question about traffic rules or penalties in my own Turkish sentences, so that I do not need to know legal terms or article numbers before I ask. |  | 8 | özge çalışkan | Sprint 2 | To Do | [CHUNKY-124](https://chunky-502.atlassian.net/browse/CHUNKY-124) |
| S2 | US-02 Get a correct answer with its sources | As a driving-licence candidate, I want a correct answer drawn from the official legal texts together with the article it rests on, so that I can rely on it and check it myself when I prepare for the exam. |  | 8 |  | Sprint 3 | To Do | [CHUNKY-129](https://chunky-502.atlassian.net/browse/CHUNKY-129) |
| S3 | US-03 Ask a follow-up question | As a driver, I want to ask a follow-up question about the answer I just received, so that I do not need to repeat my earlier question. |  | 5 |  | Sprint 4 | To Do | [CHUNKY-136](https://chunky-502.atlassian.net/browse/CHUNKY-136) |
| S4 | US-04 Start a new chat | As a driver, I want to open a new chat whenever I want, so that my next question is not mixed with the previous topic. |  | 2 |  | Sprint 4 | To Do | [CHUNKY-137](https://chunky-502.atlassian.net/browse/CHUNKY-137) |
| S5 | US-05 Know what the assistant covers and how current it is | As a driving-licence candidate, I want to see which legal texts the assistant covers, how current they are, and open them, so that I know what I can ask, whether the rules are up to date, and can read the full text if I want. |  | 5 |  | Sprint 4 | To Do | [CHUNKY-138](https://chunky-502.atlassian.net/browse/CHUNKY-138) |

## S1 · US-01 Ask in my own words

**Acceptance criteria**

- When the user submits a question written in Turkish, the assistant shall return an answer in Turkish.
- When the user describes a violation in everyday words (for example, "kırmızı ışıkta geçtim"), the assistant shall return the sanctions the document set lays down for it.
- When the user submits a question, the assistant shall return either an answer or an error message, and the interface shall not freeze or show a blank screen.
- If the user submits an empty message, then the assistant shall not send it and shall ask the user to type a question.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Write the prompt rule for sanctions and block empty messages in the interface | özge çalışkan |  | To Do | [CHUNKY-163](https://chunky-502.atlassian.net/browse/CHUNKY-163) |
| Test 10 everyday-word questions, with and without Turkish characters | Ekin Deniz Öztürk |  | To Do | [CHUNKY-164](https://chunky-502.atlassian.net/browse/CHUNKY-164) |

## S2 · US-02 Get a correct answer with its sources

**Acceptance criteria**

- When the user asks an in-scope question, the assistant shall base the answer only on the six texts of the document set.
- Where the answer needs several articles, from one text or from more than one text, the assistant shall use all of them in the answer.
- While the assistant answers a penalty question, the assistant shall state the fine amount as written in the Law.
- When the assistant answers an in-scope question, the assistant shall show at least one reference with the name of the text and the article number, and the quoted provision of that article.
- When the assistant names an article, that article shall contain the provision that supports the answer.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Analyse wrong answers of D6 and tune chunking, k and prompt |  |  | To Do | [CHUNKY-178](https://chunky-502.atlassian.net/browse/CHUNKY-178) |
| Improve retrieval for questions that need several articles; show the quoted provision |  |  | To Do | [CHUNKY-179](https://chunky-502.atlassian.net/browse/CHUNKY-179) |
| Test 5 penalty questions and re-run the 30 in-scope questions |  |  | To Do | [CHUNKY-180](https://chunky-502.atlassian.net/browse/CHUNKY-180) |

## S3 · US-03 Ask a follow-up question

**Acceptance criteria**

- When the user sends a follow-up that refers to an earlier answer (for example, "peki ikinci seferde ne olur?"), the assistant shall use the earlier questions and answers of the same chat to answer it.
- While a chat is open, the assistant shall show all questions and answers of that chat in order on one screen.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Keep the turns in the session and turn a follow-up into a stand-alone question |  |  | To Do | [CHUNKY-197](https://chunky-502.atlassian.net/browse/CHUNKY-197) |
| Show all questions and answers of the open chat in order on one screen |  |  | To Do | [CHUNKY-198](https://chunky-502.atlassian.net/browse/CHUNKY-198) |
| Test 10 follow-up questions |  |  | To Do | [CHUNKY-199](https://chunky-502.atlassian.net/browse/CHUNKY-199) |

## S4 · US-04 Start a new chat

**Acceptance criteria**

- When the user selects "New chat", the interface shall show an empty conversation.
- When a new chat is opened, the assistant shall not use any question or answer of the previous chat to produce answers.
- While a chat is open, the "New chat" button shall be visible on the screen.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Add the always visible 'New chat' button that clears the history |  |  | To Do | [CHUNKY-200](https://chunky-502.atlassian.net/browse/CHUNKY-200) |
| Test that the earlier chat is not used |  |  | To Do | [CHUNKY-201](https://chunky-502.atlassian.net/browse/CHUNKY-201) |

## S5 · US-05 Know what the assistant covers and how current it is

**Acceptance criteria**

- When the user opens the interface, the interface shall show a short note that names the six texts of the document set.
- When the user selects a text name, the interface shall open its official source in a new tab.
- Where a text has a retrieval date recorded in D1, the interface shall display that date next to the text name.
- When a text of the document set is replaced by a newer consolidated version, the assistant shall use the new version for answers after the next deployment.
- The assistant shall not use any text that is not listed in the document set.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| Write the note and build the panel with six names, retrieval dates and links |  |  | To Do | [CHUNKY-202](https://chunky-502.atlassian.net/browse/CHUNKY-202) |
| Write the re-indexing steps and test with one changed article |  |  | To Do | [CHUNKY-203](https://chunky-502.atlassian.net/browse/CHUNKY-203) |
