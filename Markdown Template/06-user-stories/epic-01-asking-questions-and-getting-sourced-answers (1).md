# Story Requirements for Epic 01 · Asking questions and getting sourced answers

<!-- Exported from Jira on 2026-11-10 (project CHUNKY). Jira is the source of truth for this backlog;
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
| S6 | US-12 Ask for a missing detail | As the General Directorate of Security (EGM), I want the assistant to ask the user for a detail that changes the penalty or the rule, so that citizens do not get a wrong fine and EGM does not give wrong information through the assistant. | Medium | 5 |  | Sprint 3 | To Do | [CHUNKY-223](https://chunky-502.atlassian.net/browse/CHUNKY-223) |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-01-1 | Turkish question gets a Turkish answer | Type "Hız limitini aşarsam ne kadar ceza öderim?" and send. | The answer is written in Turkish. |
| TC-01-2 | Everyday wording is understood | Type "kırmızı ışıkta geçtim" and send. | The answer gives the sanctions that the document set lays down for running a red light. |
| TC-01-3 | Answer or error, never a blank screen | Send any question; repeat with the answer service switched off. | With the service on, an answer appears. With the service off, an error message appears. The screen is never frozen or blank. |
| TC-01-4 | Empty message is not sent | Leave the question box empty and press send. | Nothing is sent and the interface asks the user to type a question. |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-02-1 | Answer rests only on the six texts | Ask an in-scope question that has a gold answer in the question set. | The answer matches the gold answer and cites only articles of the six texts. |
| TC-02-2 | Several articles are used together | Ask a question whose gold source lists two articles (one question with articles from two texts). | The answer uses all the articles named in the gold source. |
| TC-02-3 | Fine amount as written in the Law | Ask "Kemer takmamanın cezası nedir?" | The fine amount is the one written in the Law (as in the gold answer) and is stated in the answer. |
| TC-02-4 | Reference with text name, article number and quoted provision | Ask any in-scope question. | At least one reference shows the name of the text, the article number and the quoted provision. |
| TC-02-5 | Named article supports the answer | Open each article named in the answers of TC-02-1 to TC-02-3 in the official text. | Each article contains the provision that supports the answer. |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-03-1 | Follow-up uses the earlier answer | Ask about the penalty for running a red light, then send "peki ikinci seferde ne olur?" | The answer is about a second offence of running a red light, without repeating the first question. |
| TC-03-2 | All turns shown in order | Send three questions in one chat. | All three questions and answers are shown in order on one screen. |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-04-1 | New chat is empty | Ask a question, then select "New chat". | The conversation area is empty. |
| TC-04-2 | Previous chat is not used | After TC-04-1, send "peki ikinci seferde ne olur?" | The assistant does not know the earlier topic and asks what the user means or states it cannot answer. |
| TC-04-3 | Button always visible | Open the page, ask three questions, scroll the answers. | The "New chat" button is visible at all times. |

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

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-05-1 | Note names the six texts | Open the interface. | A short note names the six texts. |
| TC-05-2 | Official source opens | Select a text name. | The official source opens in a new tab. |
| TC-05-3 | Retrieval date shown | Look next to each text name. | The retrieval date from D1 is shown next to the name. |
| TC-05-4 | Replaced text is used | Replace one text with a newer version, deploy, and ask a question about a changed article. | The answer uses the new version. |
| TC-05-5 | Only listed texts are used | Ask a question that only an unlisted text could answer. | The assistant does not answer from the unlisted text. |

## S6 · US-12 Ask for a missing detail

**Acceptance criteria**

- When a question lacks a detail that changes the answer (vehicle type, licence class, place, repeat offence or fine year), the assistant shall ask one clarifying question and show the options as buttons.
- While a detail that changes the penalty is missing, the assistant shall not state a single fine amount as if it applied to every case.
- Where only a few options exist, the assistant shall answer all of them in a short table.
- Where the missing detail changes the answer only slightly, the assistant shall answer and state the assumption it made.
- When the user has answered the clarifying question, the assistant shall answer for the chosen option and shall not ask a second clarifying question.
- When no detail is missing, the assistant shall answer without asking.

**Sub-tasks**

| Sub-task | Owner | Estimate | Status | Jira |
|---|---|---|---|---|
| (no sub-tasks created in Jira yet) |  |  |  |  |

**Test cases**

| ID | Criterion checked | Steps | Expected result |
|---|---|---|---|
| TC-12-1 | Clarifying question with buttons | Ask a penalty question without the vehicle type. | The assistant asks one question and shows the options as buttons. |
| TC-12-2 | No single fine when a detail is missing | Repeat TC-12-1 and read the reply before pressing a button. | The reply gives no single fine amount as if it applied to every case. |
| TC-12-3 | Table for few options | Ask a question with two possible answers. | A short table shows both answers. |
| TC-12-4 | Assumption stated | Ask a question where the missing detail changes the answer only slightly. | The assistant answers and states the assumption it made. |
| TC-12-5 | No second question | Press a button in TC-12-1. | The answer fits the chosen option and no second question follows. |
| TC-12-6 | No question when nothing is missing | Ask a question with all details given. | The assistant answers directly. |
