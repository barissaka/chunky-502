# Sprint 2 Retrospective

**Team:** Chunky (Barış Saka, Ekin Deniz Öztürk, Özge Çalışkan, Zehranur Aymaz Kutluyer)
**Sprint:** Sprint 2, 28 October 2026 – 14 November 2026 (planned end 17 November 2026; the submission was moved forward to 14 November 2026)
**Retrospective held on:** 14 November 2026

## Retrospective Board

| What went well? | What went bad? | Action | Assigned to |
|---|---|---|---|
| The sprint goal was met: the RAG baseline runs end to end (472 article chunks, bge-m3 hybrid retrieval, gpt-oss-120b on Vertex AI), the long-context baseline (E3) ran on the same 10 development questions, and the two were compared with the same judge. Retrieval reached Recall@8 = 1.00 against the target of 0.80. All 12 sprint items (43 story points) were closed in Jira. | The submission was moved forward by three days, from 17/11 to 14/11. To finish on time, some acceptance criteria were reduced at the end of the sprint: the interface is not yet connected to the question endpoint (EN-15), the RAG pipeline was not run once more with the long-context model (EN-08), and the Objective 2 levels were not written into the charter (EN-08). | Carry every reduced criterion into a Sprint 3 work item with an owner at sprint planning (the endpoint connection is already EN-16). Plan each sprint against an internal deadline three days before the official one, so that a change of date does not cut scope. | Zehranur Aymaz Kutluyer |
| The Sprint 1 actions were turned into Jira items and carried out: the sprint walkthrough and deliverables checklist (EN-27) and the capacity check (EN-28); the build items also moved through In Progress on the board, which they had not done in Sprint 1. | The instructor's feedback during the sprint changed the work plan: six items (9 story points) were added after the sprint had started (EN-20, EN-21, EN-22, EN-23, EN-27, EN-28), and the scope grew from 34 to 43 points. | Record each feedback point as a Jira item within one day of receiving it, and keep about 20% of each sprint's capacity free for such changes when the sprint is planned. | Ekin Deniz Öztürk |
| We met three times a week, and each member worked on their own branch and merged through pull requests (18 pull requests in this sprint) instead of committing directly to the main branch as in Sprint 1. | Members worked about 10 hours a week, above the 7 hours of constraint C-10, for the second sprint in a row. | At Sprint 3 planning, decide either to raise C-10 to the real figure with an entry in the charter change log, or to reduce the Sprint 3 scope until it fits 7 hours per member per week. | Özge Çalışkan |
| Cloud spending stayed small: about $3.50 of the $200 Google Cloud budget ($50 of credits for each of the four members). | Work was concentrated at the end of the sprint: 39 of the 54 commits were made on 10–14/11, 25 of the 43 story points were closed on 14/11, and the acceptance criteria of several items were written into Jira only on 14/11. | Use one of the three weekly meetings as a status check: every item's Jira status is updated there, and an item moves to In Progress only when its acceptance criteria are written (Definition of Ready). | Barış Saka |
| Three spikes prepared this sprint's design decisions: the vector store (spike 04, for AD-06), the evaluation library (spike 05, for AD-12) and the chat interface framework (spike 06, Streamlit chosen). |  |  |  |

## Lessons Learned

**Process**
1. A deadline can move. Planning against an internal deadline a few days before the official one keeps the scope intact when the date changes; when scope must still be cut, the reduced criteria are written into the next sprint's items instead of being dropped.
2. Feedback from the instructor arrives during the sprint and changes the plan. Reserving part of the capacity for it, and turning each feedback point into a Jira item at once, keeps the sprint scope visible and realistic.
3. Acceptance criteria belong in the work item before the work starts. Written at the end, they describe what was done rather than what was planned.
4. The 7-hours-per-week constraint was exceeded in both sprints. A constraint that does not hold should either be changed openly in the charter or enforced by smaller sprint scopes.

**Development environment**
5. Working on personal branches and merging through pull requests worked well, and we will keep it.

**Team collaboration**
6. Three short meetings a week kept everyone informed; one of them will now be used to update the Jira board, so that the burndown shows the real pace of the work.
7. Turning the last retrospective's actions into Jira items made sure they were carried out; we will do the same with the actions above.
