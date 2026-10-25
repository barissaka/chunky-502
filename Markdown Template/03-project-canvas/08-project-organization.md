# Project Organization

**Project:** Traffic rules and penalties assistant · **Team:** Chunky

This page shows who does what in Team Chunky, and how the team relates to the people who govern, review and influence the project. Team members hold the template's project roles, with Product Owner and Scrum Master as defined in the Scrum Guide [1]. Stakeholders outside the team are named with the stakeholder roles of ISO/IEC 5339 [3].

## 1. Project Team Structure

The project has no sponsor and no single manager: every member manages the project in some capacity. The Scrum Team is one team with no sub-teams or hierarchy inside it [1].

**Governance**

- **Project Review Committee:** course instructors (Tuğba Taşkaya Temizel).
- **Peer review group:** the DI 502 team assigned to us reviews our documents at Sprints 2-4.

**Scrum Team: Chunky** 

- Product Owner: Zehranur Aymaz Kutluyer
- Scrum Master: one member per sprint, rotating among all four members
- Data Scientists (Developers): Barış Saka, Zehranur Aymaz Kutluyer, Ekin Deniz Öztürk, Özge Çalışkan
- Business Analyst / Domain Expert: Ekin Deniz Öztürk
- Data Science Architect: Özge Çalışkan

**Outside stakeholders**

- Data provider: EGM Legal Department in the deployment scenario; within the project, the texts are taken from the Presidency Legislation Information System (mevzuat.gov.tr). Team contact: Barış Saka.
- AI partner: Google Cloud or Azure (hosted models) and the open-source model hub (local models). Team contact: Özge Çalışkan.
- AI users: pilot participants (drivers and driving-licence candidates). Team contact: Ekin Deniz Öztürk.

The [Project Executive Summary](01-project-executive-summary.md) names the General Directorate of Security (EGM) as the AI customer of the deployment scenario. Within DI 502, the AI customer who accepts the deliverables is the course instructors and the peer groups.

## 2. Roles and Responsibilities

| Project Role | Responsibilities | Assigned to |
|---|---|---|
| Product Owner | Sets and communicates the product goal of the assistant. Writes the user stories in the Jira Product Backlog, orders them, and refines them with the team so the backlog stays visible and understood. Decides which features of the Scope Definition enter each sprint. Owns the success criteria of Objectives 1 and 3 in the [Project Executive Summary](01-project-executive-summary.md): the time-to-answer measurement and the post-test survey. | Zehranur Aymaz Kutluyer |
| Scrum Master | Held by one member per sprint, rotating among all four members; the holder is named at each sprint planning and recorded in Jira. Runs sprint planning, the weekly progress meeting, the sprint review and the retrospective. Tracks impediments in Jira and gets them removed. Together with the Product Owner, checks that stories meet the INVEST criteria before planning [2]. Makes sure the team's Quality Team review of its assigned group and the rebuttal to our own review are submitted on time. | One member per sprint (rotating): Barış Saka, Zehranur Aymaz Kutluyer, Ekin Deniz Öztürk, Özge Çalışkan |
| Business Analyst / Domain Expert | Collects real questions that drivers and licence candidates ask about traffic rules and penalties from social media and blogs, classifies them with the question types of D2 (answered from a single article; two or more articles of one text; articles from two or more texts; a violation described in the user's own words; out of scope) and hands them to the Product Owner as draft stories. Builds the evaluation set: 30 in-scope questions and 10 questions outside the document set. Records, for each question, which article of which text answers it, and writes the answer key from the legal texts before testing. As Domain Expert, owns the success criteria of Objectives 2 and 4: writes and owns the answer key against which answers are scored automatically. Recruits the 10 test participants and schedules the sessions. | Ekin Deniz Öztürk |
| Data Science Architect | Owns the RAG architecture of the assistant. Makes and records in Confluence the technical design decisions for the pipeline: parsing the legal texts and chunking them by article, embedding and retrieval, prompt design, answer generation with a language model reached through a provider-agnostic gateway (local quantized model or hosted model, Architecture AD-03), and citation of the source article. Leads the implementation of these core components and integrates them into one working pipeline. Reviews and merges code on GitHub. Design decisions are discussed with the Data Scientists at sprint planning; the role gives no authority over other members. | Özge Çalışkan |
| Data Scientist | Turns backlog items into working increments of the assistant across the pipeline (data preparation, retrieval, answer generation, chat interface), working with the Data Science Architect. Plans the sprint and adapts the plan daily towards the Sprint Goal. Runs the experiments and records the runs, dataset versions and model versions in Weights & Biases. Runs the evaluation set against each increment and checks it against the Definition of Done. | Barış Saka, Zehranur Aymaz Kutluyer, Ekin Deniz Öztürk, Özge Çalışkan |
| Project Review Committee | Reviews the project charter and the sprint deliverables, and assesses the final product at the live demo. | Course instructors |
| AI customer | Accepts the final product (live demo, end of Sprint 4). The go/no-go decision on the MVP (M8) is made by the Product Owner and the Business Analyst / Domain Expert. The peer groups review our documents at Sprints 2-4 and fill in our Review page. Contact: Zehranur Aymaz Kutluyer. | Course instructors and peer groups |
| Data provider | Keeps the texts of the document set up to date in the deployment scenario; within the project, the official consolidated texts are taken from the Presidency Legislation Information System (mevzuat.gov.tr). Contact: Barış Saka, who downloads the texts, checks their terms of use, records the version date of each text and checks for amendments before each sprint. | EGM Legal Department (deployment scenario); Presidency Legislation Information System (within the project) |
| AI partner | Google Cloud or Azure hosts the long-context baseline, the judge model and a hosted language model if one is chosen, within the $100 limit. The open-source model hub provides the local language, embedding and reranking models. Contact: Özge Çalışkan, who tracks the credit usage. | Google Cloud or Azure; open-source model hub |
| AI user | Ask traffic-rule and penalty questions in the timed usability test (default state in Sprint 1, assistant in Sprint 4) and answer the post-test survey. Contact: Ekin Deniz Öztürk, who recruits the 10 participants and schedules the sessions. | Pilot participants (drivers and driving-licence candidates) |

Notes:

- **Group Manager** and **Project Lead** are deleted: in a team of four, coordination is covered by the Scrum Master and the Data Science Architect, and progress against the success criteria is tracked by the owners of each objective (Product Owner for Objectives 1 and 3, Domain Expert for Objectives 2 and 4).
- **Data Science Architect** is added as a new role because no template role covers this work. The template's Team Lead only coordinates an area; this role also designs and builds the core RAG pipeline that the other Data Scientists extend.
- **Domain Expert** is held together with Business Analyst because the [Project Executive Summary](01-project-executive-summary.md) names a Domain Expert as the owner of Objectives 2 and 4, and no other template role covers writing the answer key from the legal texts.

## References

[1] K. Schwaber and J. Sutherland, *The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game*, Nov. 2020. [Online]. Available: https://scrumguides.org/scrum-guide.html (accessed Oct. 7, 2026).

[2] A. Ben Salem, "Creating the Perfect User Story with INVEST Criteria," Scrum-Master·Org, Dec. 5, 2023 (updated Jun. 20, 2024). [Online]. Available: https://scrum-master.org/en/creating-the-perfect-user-story-with-invest-criteria/ (accessed Oct. 5, 2026).

[3] ISO/IEC JTC 1/SC 42, *ISO/IEC 5339:2024 Information technology — Artificial intelligence — Guidance for AI applications*, 1st ed. Geneva, Switzerland: International Organization for Standardization and International Electrotechnical Commission, Jan. 2024. UK implementation: BS ISO/IEC 5339:2024, London, UK: BSI Standards Limited, 2024.
