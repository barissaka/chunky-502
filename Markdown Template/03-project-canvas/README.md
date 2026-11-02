# Project Canvas

**Project:** Traffic rules and penalties assistant · **Team:** Chunky · **Timeline:** 14/10/2026 – 30/12/2026 (4 sprints)

Drivers and driving-licence candidates in Türkiye ask a question about traffic rules and penalties in Turkish, in their own words, and get an answer that names the article of the law it rests on. The assistant is a retrieval-augmented generation (RAG) system over six texts of Turkish traffic legislation and runs on a team laptop.

*Cells marked with \* are the red cells.*

| [Scope\*](01-project-executive-summary.md) | [Milestones\*](02-milestones.md) | [Assumptions & Constraints\*](03-assumptions-and-constraints.md) |
|---|---|---|
| • Scope: a question-answering assistant in Turkish over six texts: Highway Traffic Law No. 2918, Highway Traffic Regulation and the regulations on driver courses, driver health, vehicle inspection and electric scooters<br>• Vision: one place to ask, with the article behind the answer<br>• Objectives: median time to a correct answer under 77 s; at least 80% correct answers and 80% supported article references on 30 questions; at least 7 of 10 pilot participants would use it again and rate it clear; 10 of 10 out-of-scope questions declined | • M1–M3 (Sprint 1): document set fixed, default state measured (77 s), charter v1 approved<br>• M4 (13/11) and M5 (20/11): long-context and RAG baselines, alpha<br>• M6 (23/11) and M8 (14/12): go/no-go checkpoints<br>• M7 (11/12): Objective 2 measured on the beta<br>• M9 (24/12): pilot completed<br>• M10 (30/12): release candidate accepted | • Assumptions A-01–A-06: official texts can be extracted by article; real sources yield enough questions; 10 participants take part twice; no amendment changes the answer key; terms of use permit collection; EGM can host on CPU-only hardware<br>• Constraints C-01–C-14: six texts only, as a snapshot; Turkish only; RAG; at most one clarifying question; runs on a 16 GB laptop with local models up to 4B; no link to EGM systems; $100 cloud budget; 4 sprints; 4 students × 7 h/week; no advice on an individual case; no personal data stored; query guard |

| [Major Activities](04-major-activities.md) | [Deliverables\*](05-deliverables.md) | [Dependencies](06-dependencies.md) |
|---|---|---|
| • 24 in-scope activities: document and question sets, retrieval index and RAG pipeline, out-of-scope handling, clarification and follow-ups, personal-data masking, web interface, baselines and evaluation, pilot, datasheet, project management<br>• 10 out-of-scope activities: training or fine-tuning, other legislation, other languages, personal record queries, advice on contesting a penalty, user accounts, multi-turn clarification, public release, market analysis, maintenance after the project | • Sprint 1: D1 Document set and Dataset Report, D2 Q&A Generation-Dataset v1, D3 Default-state measurement report, D4 Project Charter v1<br>• Sprint 2: D5 Long-context baseline experiment card, D6 RAG baseline experiment card, D7 Alpha prototype, D13 Datasheet for Q&A Generation-Dataset v1<br>• Sprint 3: D8 MVP validation experiment card, D9 Beta release<br>• Sprint 4: D10 Pilot test report, D11 Release candidate, D12 Final report | • Index building waits for the document set (21/10)<br>• Baseline and automated scoring wait for cloud model access (04/11)<br>• Alpha waits for local models running through Ollama (04/11)<br>• Beta waits for M6 (23/11); pilot waits for M8 and 10 confirmed participants (14/12)<br>• Release-candidate evaluation waits for the committee's unseen question set (23/12) |

| [Cost & Funding](07-cost-and-funding.md) | [Project Organization\*](08-project-organization.md) | [Facilities and Resources](09-facilities-and-resources.md) |
|---|---|---|
| • Initial cost estimate: 308 person-hours of the 308 available (4 members × 7 h × 11 weeks); up to $100 of hosted model calls<br>• Source of funding: in-kind effort of the four students; $100 Google Cloud credit (Azure as an alternative, within the same $100); member-owned laptops; public data | • Stakeholders: drivers, licence candidates and driving-school instructors (AI users); EGM (AI customer); EGM IT unit (AI application provider); EGM Legal Department (data provider); Ministries of Interior and of Transport; other road users<br>• Team structure: one Scrum Team, no hierarchy; reviewed by the course instructors and a peer group<br>• Roles: Product Owner Zehranur Aymaz Kutluyer; Business Analyst / Domain Expert Ekin Deniz Öztürk; Data Science Architect Özge Çalışkan; Data Scientists: all four members, including Barış Saka; Scrum Master rotates each sprint | • Host laptop (PC 1, 16 GB RAM, CPU inference through Ollama); spare hosts PC 2 and PC 4<br>• Google Cloud project with $100 of credits; Azure as an option<br>• mevzuat.gov.tr, the EGM FAQ page and public forums<br>• GitHub, Jira, Confluence, Weights & Biases |

| [Release Plan](10-release-plan.md) | [Risks](11-risks.md) | Result |
|---|---|---|
| • Sprint 1 (14–28/10): Pre-alpha<br>• Sprint 2 (04–18/11): Alpha 0.1, used by the team<br>• Sprint 3 (25/11–09/12): Beta 0.5, for the 10 pilot participants<br>• Sprint 4 (16–30/12): Release candidate 1.0, shown in the live demo<br>• The gaps between sprints are review periods and hold the go/no-go checkpoints | • 20 risks across the five layers (data, model, infrastructure, integration, people / process)<br>• 6 high risks (score 12), each with a trigger, contingency plan and owner: too few real questions, too few participants, out-of-scope questions answered, Objective 2 not met, automated scoring disagrees with the answer key, slow answers on the laptop<br>• No critical risk | • Problem: drivers and licence candidates cannot easily tell which rule applies and where it is written, because texts are amended and fines are revalued every year<br>• Value: one answer in Turkish with the article and the quoted provision, faster than searching the texts and the web<br>• Impacted: drivers, licence candidates, instructors, EGM and its traffic units, other road users<br>• Conflicts: advice on contesting a penalty and questions on other legislation are declined (C-11, C-01) |

## Subpages

- [Project Executive Summary](01-project-executive-summary.md)
- [Milestones](02-milestones.md)
- [Assumptions & Constraints](03-assumptions-and-constraints.md)
- [Major Activities](04-major-activities.md)
- [Deliverables](05-deliverables.md)
- [Dependencies](06-dependencies.md)
- [Cost & Funding](07-cost-and-funding.md)
- [Project Organization](08-project-organization.md)
- [Facilities & Resources](09-facilities-and-resources.md)
- [Release Plan](10-release-plan.md)
- [Risks](11-risks.md)
- [Software Bill of Materials](../10-software-bill-of-materials.md)
- [Datasheets](../11-datasheets/README.md)

## Glossary

| Term | Meaning |
|---|---|
| Document set | The six legal texts the assistant draws on, as retrieved on the dates recorded in D1 (C-01, C-02) |
| Question set (D2) | 40 questions with an answer key: 30 in scope and 10 out of scope |
| Question type | One tag per question: answered from a single article; two or more articles of one text; articles from two or more texts; a violation described in the user's own words; out of scope |
| Answer key | The correct answer and supporting article(s) for each in-scope question, written from the legal texts before any system is tested |
| Ambiguity label | Whether a question is ambiguous: the answer key gives different answers depending on a condition the question does not state (vehicle type, driver status, location or repeat offence). Ambiguous questions also record the missing condition, a scripted user reply and the answer for that reply. The labels are the reference for scoring the assistant's decision to ask a clarifying question (R-15) |
| Follow-up question | A question that depends on an earlier question of the same session |
| Synthetic question | A question written by the team to fill a question type with too few real questions; labelled as such, at most 10 of 30 |
| Long-context baseline | A hosted model that reads the full document set with no retrieval; the comparison point for the RAG results (D5) |
| Recall@k | Share of in-scope questions for which at least one supporting article is among the k retrieved chunks |
| Query guard | Rule-based checks before retrieval for prompt injection and requests for advice on an individual case (C-13) |
