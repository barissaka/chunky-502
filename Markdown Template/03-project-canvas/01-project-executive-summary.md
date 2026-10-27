# Project Executive Summary

**Project:** Traffic rules and penalties assistant · **Team:** Chunky

### Background

Road users in Türkiye are bound by the Highway Traffic Law No. 2918 [1], the Highway Traffic Regulation [2] and further regulations on driver courses [3], the health requirements for drivers [4], vehicle inspection [5] and electric scooters [6]. Together the six texts hold several hundred articles, written in legal language, and a single question can require reading several articles across more than one text.

Because laws are amended and fine amounts are revalued every year, a driver finds it difficult to tell which rule applies and where it is written. Drivers and driving-licence candidates therefore either read the legal texts themselves or rely on pages that do not show which article they rest on. The project exists to give them one place to ask a question and see the article behind the answer.

**Budget:** $100 of Google Cloud credits for hosted model calls; Azure is an alternative cloud option, and total cloud spending on both stays within $100.
**Duration:** 4 sprints.
**Timeline:** 14 October 2026 to 30 December 2026.

### 1. Stakeholders

| # | Stakeholder | Role (ISO 5339) | Perspective | Relationship to project | Benefit from project |
|---|---|---|---|---|---|
| 1 | Licensed drivers in Türkiye | AI user | Use | Ask about traffic rules, violations and penalties | An answer in one place, with the article it rests on |
| 2 | Driving-licence candidates | AI user | Use | Ask about rules while preparing for the licence exam and for their first months of driving | Learn each rule together with its official source |
| 3 | Driving-school instructors | AI user | Use | Secondary end-user group: look up rule details and the amounts written in the Law while teaching | Answer student questions from the Law rather than memory or last year's guide |
| 4 | General Directorate of Security (EGM) | AI customer | Use | Would commission the assistant for drivers and driving-licence candidates | Fewer repeated rule and penalty questions to its traffic units |
| 5 | EGM information technologies unit | AI application provider | Make (shared) | Would run the assistant for the public after deployment | Sees which rules and penalties road users ask about most |
| 6 | EGM Legal Department | Data provider | Make | Would keep the texts of the document set that the assistant draws on up to date after each amendment, taking them from the official consolidated texts | The assistant's answers follow the legal text in force |
| 7 | Ministry of Interior | Regulators / policy makers | Impact | Issues the Regulation; the General Directorate of Security is attached to it | Interest: road users receive rule and penalty information that matches the official text |
| 8 | Ministry of Transport and Infrastructure | Regulators / policy makers | Impact | Executes the Regulation jointly with the Ministry of Interior; responsible for road infrastructure and vehicle inspection | Interest: road users receive information on vehicle and road-use rules that matches the official text |
| 9 | Other road users (pedestrians, passengers, cyclists) | Community | Impact | Share the road with the drivers who use the assistant | Drivers around them know the rules that protect them |

Conflicts between stakeholders:

1. Drivers who have received a penalty want advice on whether and how to contest it. The assistant states what the texts in its document set say and gives no advice on an individual case (see Out of Scope under Major Activities).
2. Users may ask about related topics in other legislation, such as motor vehicle tax or comprehensive (kasko) insurance. The General Directorate of Security is responsible for traffic legislation, not for those topics. The assistant covers its document set only (see Out of Scope under Major Activities).

### 2. Project Vision

Drivers and driving-licence candidates in Türkiye settle a question about traffic rules and penalties in one place and in their own words, and see which article of the law the answer rests on, instead of searching legal texts and web pages that disagree with each other.

### 3. Objectives

| # | Objectives | Success Criteria | Business Outcomes |
|---|---|---|---|
| 1 (strategic) | By the end of Sprint 4, reduce the time drivers and driving-licence candidates need to find the right answer to a question about traffic rules or penalties, compared with searching the legal texts and the web. | Median time to reach a correct answer to a test question is under 77 seconds, the default-state value measured in D3, in which the same participants answered comparable questions with the official texts and a web search. Method: timed usability test with 10 participants, 3 questions each. Owner: Product Owner. End of Sprint 4. Maps to: task completion time in the usability test, supported by end-to-end response time and answer correctness. | Today participants look in several places to answer one question; in the Sprint 4 test they need only the assistant. |
| 2 (Phase-1 MVP) | By the end of Sprint 3, validate that an MVP assistant gives correct, source-backed answers to drivers' and licence candidates' questions about the rules and penalties in the six texts of the document set (see 4). | At least 80% of answers judged correct on a fixed set of 30 test questions; at least 80% of answers name the article they rest on, and the named article supports the answer. Levels: set by the team from its own research and its first trial runs in Sprint 2. Method: each answer is compared with an answer key written from the legal texts before testing. Owner: Business Analyst / Domain Expert (owns the answer key); scoring is automated (Architecture AD-12). End of Sprint 3. Maps to: answer correctness, retrieval quality and citation metrics in the experiment cards. | In the pilot, participants report needing no second source for at least 8 of 10 questions (post-test survey). |
| 3 | By the end of Sprint 4, drivers and licence candidates in the pilot prefer the assistant to their current way of looking up traffic rules and penalties. | At least 7 of 10 pilot participants say they would use the assistant again, and at least 7 of 10 rate the answers as clear (4 or 5 on a 5-point scale). Levels: team estimate. Method: post-test survey. Owner: Product Owner. End of Sprint 4. Maps to: survey scores. | At least half of pilot participants name the assistant as the first source they would turn to for a traffic-rule question (post-test survey). |
| 4 | By the end of Sprint 4, drivers and licence candidates are not misled when they ask something the document set cannot answer. | For 10 questions outside the document set, the assistant declines and states that the document set does not cover the topic. Level: team estimate. Method: scripted test set, each answer checked automatically against the fixed refusal sentence. Owner: Business Analyst / Domain Expert. End of Sprint 4. Maps to: refusal rate on out-of-scope questions. | No pilot participant reports receiving an out-of-topic response. |

Objectives 1–4 cover performance, quality, adoption/UX and safety/compliance in turn.

### 4. Scope Definition

A question-answering assistant for six texts of Turkish traffic legislation, used in Turkish by drivers and driving-licence candidates. It is intended for the official EGM web page after the project; within the project it runs on a team laptop.

The document set consists of the Highway Traffic Law No. 2918 [1], the Highway Traffic Regulation [2], the Regulation on Private Motor Vehicle Driver Courses [3], the Regulation on the Health Requirements and Examinations of Driver Candidates and Drivers [4], the Regulation on Vehicle Inspection Stations and Vehicle Inspection [5] and the Electric Scooter Regulation [6].

| # | Feature | What the user can do with it | Objective(s) it serves |
|---|---|---|---|
| 1 | Questions in the user's own words | Ask in Turkish about a traffic rule, a violation or a penalty and get an answer in Turkish | 1, 2, 3, 4 |
| 2 | Article reference | See which article of which text each answer rests on and read the quoted provision | 2 |
| 3 | Sanctions for a violation | Describe a violation and see the sanctions the document set lays down for it: the fine as written in the Law, penalties, licence withdrawal and vehicle ban; amounts are shown as written in the texts, and a notice on the chat page states that fine amounts are revalued every year | 1, 2 |
| 4 | Out-of-scope handling | Get a statement that the assistant cannot answer when the question lies outside the document set | 4 |

## References

[1] *Karayolları Trafik Kanunu* (Highway Traffic Law), Law No. 2918, adopted 13 Oct. 1983, *Resmî Gazete*, 18 Oct. 1983. Consolidated text: Presidency Legislation Information System, mevzuat.gov.tr.

[2] *Karayolları Trafik Yönetmeliği* (Highway Traffic Regulation), *Resmî Gazete*, no. 23053 (mükerrer), 18 Jul. 1997. Consolidated text: Presidency Legislation Information System, mevzuat.gov.tr.

[3] *Millî Eğitim Bakanlığı Özel Motorlu Taşıt Sürücüleri Kursu Yönetmeliği* (Regulation on Private Motor Vehicle Driver Courses of the Ministry of National Education), *Resmî Gazete*, no. 28661, 29 May 2013. Consolidated text: Presidency Legislation Information System, mevzuat.gov.tr.

[4] *Sürücü Adayları ve Sürücülerde Aranacak Sağlık Şartları ile Muayenelerine Dair Yönetmelik* (Regulation on the Health Requirements and Examinations of Driver Candidates and Drivers), *Resmî Gazete*, no. 26301, 26 Sep. 2006. Consolidated text: Presidency Legislation Information System, mevzuat.gov.tr.

[5] *Araç Muayene İstasyonlarının Açılması, İşletilmesi ve Araç Muayenesi Hakkında Yönetmelik* (Regulation on the Opening and Operation of Vehicle Inspection Stations and on Vehicle Inspection), *Resmî Gazete*, no. 31356, 6 Jan. 2021. Consolidated text: Presidency Legislation Information System, mevzuat.gov.tr.

[6] *Elektrikli Skuter Yönetmeliği* (Electric Scooter Regulation), *Resmî Gazete*, no. 31454, 14 Apr. 2021. Consolidated text: Presidency Legislation Information System, mevzuat.gov.tr.

[7] H. Zamani, S. Dumais, N. Craswell, P. Bennett and G. Lueck, "Generating Clarifying Questions for Information Retrieval," in *Proc. The Web Conference (WWW 2020)*, 2020.

[8] M. J. Q. Zhang and E. Choi, "Clarify When Necessary: Resolving Ambiguity Through Interaction with LMs," in *Findings of NAACL 2025*, 2025.
