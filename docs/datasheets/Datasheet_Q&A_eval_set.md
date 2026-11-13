# Datasheet: Traffic-Law RAG Q&A Gold Set
## Summary

The Traffic-Law RAG Q&A Gold Set has 40 hand-built questions for evaluating the project's RAG chatbot. 30 are in scope and 10 are out of scope. Each in-scope question comes with a gold answer, references at article, paragraph and clause level, and a verbatim quote from the source text. Each out-of-scope question comes with the behaviour the bot is expected to show instead of an answer. This datasheet is the Sprint 2 deliverable. It records what the set contains and every decision made while building it.

| Item            | Value                                                                                                                                                          |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Version         | v1.4 (last change 27 Oct 2026)                                                                                                                                 |
| Records         | 40 (30 in-scope, 10 out-of-scope)                                                                                                                              |
| Language        | Turkish content, English type labels                                                                                                                           |
| Source corpus   | 6 Turkish traffic-law texts (2918 sayılı KTK and 5 regulations)                                                                                                |
| Formats         | Word, CSV, JSONL, interactive HTML page                                                                                                                        |
| Companion files | Eval_Set_1.csv(the 40 records with axis tags, D23); Eval_Set_1_2_New_Questions.xlsx (23 candidate questions, not part of the set, D24–D25) |

## Motivation

The set exists to measure three things on a fixed, repeatable benchmark:

1. **Retrieval:** does the retriever bring back the articles named in the references (recall@k)?

2. **Answer quality:** does the answer agree with the gold answer, cite the right articles, and avoid adding facts the texts do not contain?

3. **Refusal:** when a question falls outside the six texts, does the bot say so instead of inventing an answer?

The question types and minimum counts come from the project task definition:

- 30 in-scope questions, with at least 5 of each of the four types and at least 3 per legal text.

- 10 out-of-scope questions, taken from FAQ topics the six texts cannot answer.

## Composition

All the task's distribution constraints are met: each type has at least 6 questions, and each legal text appears in at least 4. A question that cites several texts is counted once under each of them, so the text columns add up to more than 30.

| Type                              | IDs     | Questions | KTK    | KTY    | SAĞLIK | MUAYENE | KURS  | SKUTER |
|-----------------------------------|---------|-----------|--------|--------|--------|---------|-------|--------|
| Single article                    | S01–S08 | 8         | 2      | 2      | 1      | 1       | 1     | 1      |
| Several articles of one text      | S09–S14 | 6         | 1      | 0      | 1      | 1       | 2     | 1      |
| Articles of several texts         | S15–S22 | 8         | 7      | 5      | 3      | 1       | 3     | 1      |
| Violation in the user's own words | S23–S30 | 8         | 8      | 4      | 0      | 2       | 0     | 1      |
| **In-scope total**                |         | **30**    | **18** | **11** | **5**  | **5**   | **6** | **4**  |
| Out-of-scope                      | K01–K10 | 10        | —      | —      | —      | —       | —     | —      |

Fields in each record (JSONL key in brackets):

| Field                           | Content                                                                          |
|---------------------------------|----------------------------------------------------------------------------------|
| ID (id)                         | S01–S30 in scope, K01–K10 out of scope                                           |
| Type (type)                     | One of the five labels above                                                     |
| Texts (texts)                   | Source texts the answer draws on                                                 |
| Question (question)             | User question in Turkish                                                         |
| Gold answer (gold_answer)       | Reference answer; for out-of-scope questions, the expected behaviour             |
| References (references)         | Article, paragraph and clause, e.g. KTK m.48/5; empty for out-of-scope questions |
| Evidence quote (evidence_quote) | Verbatim sentence(s) from the source                                             |
| Note (note)                     | What the question tests, assumptions, known traps                                |

Four out-of-scope questions are flagged as boundary questions: K01 (danger reporting), K02 (vehicle imported from abroad), K08 (MTV) and K09 (kasko). For each of these the retriever is likely to fetch an article that looks relevant but does not answer the question.

### Tag columns (D23)

`Eval_Set_1.csv` adds 11 tag columns to the 40 records. They describe the records and do not change them.

| Column | Values | Definition |
|---|---|---|
| Source Scope | Single article · Several articles of one text · Articles of several texts · None | How many articles or texts the evidence spans. Counted at article level: several paragraphs of one article count as one article |
| Hop Type | Single-hop · Parallel · Chain · Comparison · None | Parallel: independent facts side by side. Chain: one step's answer feeds the next. Comparison: two cases contrasted |
| Premise | Direct · With premise · False premise | Whether the user describes their own situation, or the question rests on a wrong assumption |
| Wording | Same terms · Different terms · N/A | Statute's terms or everyday words (ehliyet, scooter, kaldırım, çevirme…). N/A for out-of-scope questions |
| Phrasing | Natural question · Search query | Full sentence or search-style keywords |
| User | Novice – driver · Novice – vehicle owner · Novice – driver candidate · Novice – e-scooter user · Novice – parent | Who is asking |
| Language | TR · EN | Question language |
| Question Word | Yes/No · How many/much · When · What/Which · What happens/Penalty · How/What to do · Why | Type of the first question asked |
| Multi-part | Yes · No | The question contains more than one sub-question |
| Answerability | Answerable · Partially answerable · Unanswerable – out of domain · Unanswerable – out of domain (related provision exists) · Unanswerable – in domain · Unanswerable – sensitive request | Whether the six texts can answer the question |
| Time-sensitive | Yes · No | The answer relies on TL amounts revalued yearly (KTK Ek Madde 3) or on a recent amendment |

## Source corpus

Every answer comes from the six PDFs the team supplied on 24 Oct 2026, as they stood in those files. The texts were not refreshed from mevzuat.gov.tr afterwards.

| Code    | Text                                                                                      | PDF pages | Latest amendment seen in the file                                |
|---------|-------------------------------------------------------------------------------------------|-----------|------------------------------------------------------------------|
| KTK     | 2918 sayılı Karayolları Trafik Kanunu                                                     | 108       | 7574 sayılı Kanun, 12/2/2026 (fines in m.36, 47, 48, 51, 73, 78) |
| KTY     | Karayolları Trafik Yönetmeliği                                                            | 98        | RG 4/11/2025 (m.69 repealed)                                     |
| SAĞLIK  | Sürücü Adayları ve Sürücülerde Aranacak Sağlık Şartları ile Muayenelerine Dair Yönetmelik | 6         | RG 30/9/2021                                                     |
| MUAYENE | Araç Muayene İstasyonlarının Açılması, İşletilmesi ve Araç Muayenesi Hakkında Yönetmelik  | 13        | RG 9/10/2026 (wording changes, m.1–2)                            |
| KURS    | MEB Özel Motorlu Taşıt Sürücüleri Kursu Yönetmeliği                                       | 36        | RG 7/3/2017 (m.16/3)                                             |
| SKUTER  | Elektrikli Skuter Yönetmeliği                                                             | 11        | RG 2/12/2025 (m.16 geo-fencing rules)                            |

**Out-of-scope source.** The EGM Trafik Başkanlığı FAQ page (trafik.gov.tr/sss0) could not be fetched automatically, so the team supplied a PDF print of it. The print shows only 10 question titles. The answers are collapsed and the "Daha fazla göster" section is not expanded.

**Annex not in the corpus.** The penalty-point table referred to by KTY m.167 (Ek-35) is not in the KTY file. No penalty-point values appear anywhere in the set.

## Creation process

The set was built with an AI assistant (Claude) working from the supplied texts, and the project team made the final calls. Work ran from 24 to 27 Oct 2026. The assistant built each record in these steps:

1. Convert each PDF to plain text (pdftotext) and index the article headings.

2. Plan the type × text matrix before writing any question, so the minimum counts were guaranteed from the start.

3. Write each question, then find the governing articles by search and read them in full.

4. Write the gold answer only from what those articles say. Amounts, ages and periods are copied, not recalled.

5. Record the references down to paragraph and clause, plus a verbatim evidence quote.

6. Where text extraction could have garbled the source (tables), check the original PDF page visually.

7. Recount the distribution with a script after every change.

The team chose the source texts and the out-of-scope source, set the type labels, reworded four questions and asked for the answer revisions listed below. No lawyer has reviewed the set yet.

## Decision log

The table lists, in the order they were taken, the decisions that shaped the set. D01–D17 were taken while building v1.0. D18–D21 came with the later revisions. D22–D25 came from the 10 Nov 2026 review against the RAG test-set literature.

| ID  | Date        | Decision                                                                                                                                                                                                                                                                                                                                                                     | Rationale                                                                                                                                                                                                                                                                                                                                                                                | Affects                       |
|-----|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| D01 | 24 Oct 2026 | Build the set as a gold evaluation set (questions + gold answers + references), not a training set                                                                                                                                                                                                                                                                           | The task is to measure the RAG pipeline; gold references make recall@k computable                                                                                                                                                                                                                                                                                                        | Whole set                     |
| D02 | 24 Oct 2026 | Take answers only from the six supplied texts, never from memory or the web                                                                                                                                                                                                                                                                                                  | Answers must be checkable against the corpus the bot retrieves from                                                                                                                                                                                                                                                                                                                      | All gold answers              |
| D03 | 24 Oct 2026 | Plan a type × text matrix before writing questions                                                                                                                                                                                                                                                                                                                           | Guarantees ≥5 per type and ≥3 per text by construction, not by luck                                                                                                                                                                                                                                                                                                                      | Composition                   |
| D04 | 24 Oct 2026 | Use one fixed record schema: ID, type, texts, question, gold answer, references, evidence quote, note                                                                                                                                                                                                                                                                        | Same fields for humans (Word/CSV) and code (JSONL)                                                                                                                                                                                                                                                                                                                                       | All records                   |
| D05 | 24 Oct 2026 | Give references at paragraph and clause level, written as KTK m.48/5, KTY m.125/f-15                                                                                                                                                                                                                                                                                         | Article-level references are too coarse to score retrieval of long articles                                                                                                                                                                                                                                                                                                              | References                    |
| D06 | 24 Oct 2026 | Write "violation in the user's own words" questions in everyday Turkish without legal terms ("scooter", "kaldırım", "sarıdan kırmızıya")                                                                                                                                                                                                                                     | Tests semantic retrieval when the user's words differ from the statute's (e-skuter, yaya yolu, kırmızı ışık)                                                                                                                                                                                                                                                                             | S23–S30                       |
| D07 | 24 Oct 2026 | Use the EGM Trafik Başkanlığı FAQ as the out-of-scope source, via a PDF print                                                                                                                                                                                                                                                                                                | Team's choice; the page could not be fetched automatically                                                                                                                                                                                                                                                                                                                               | K01–K07                       |
| D08 | 24 Oct 2026 | Exclude EGM FAQ questions 1–3 from the out-of-scope list                                                                                                                                                                                                                                                                                                                     | The texts partly answer them: honorary traffic inspectors in KTK Ek Madde 6, fine appeals referred to the Kabahatler Kanunu in KTY m.160. Labelling them out of scope would penalise a correct bot                                                                                                                                                                                       | Out-of-scope list             |
| D09 | 24 Oct 2026 | Use EGM FAQ 4–10 (7 questions), then add MTV, kasko and HGS from the team's own examples                                                                                                                                                                                                                                                                                     | FAQ gave only 7 true out-of-scope items; the team's "how to contest a fine" example was not used for the reason in D08                                                                                                                                                                                                                                                                   | K01–K10                       |
| D10 | 24 Oct 2026 | For out-of-scope questions, record the expected behaviour (say the topic is not covered, cite nothing, invent no figures) instead of an answer                                                                                                                                                                                                                               | There is no gold answer to compare against; refusal is what is scored                                                                                                                                                                                                                                                                                                                    | K01–K10                       |
| D11 | 24 Oct 2026 | Flag boundary questions (K01, K02, K08, K09) and name the misleading article in the note                                                                                                                                                                                                                                                                                     | These are where hallucination is most likely; the note helps diagnose retrieval errors                                                                                                                                                                                                                                                                                                   | K01, K02, K08, K09            |
| D12 | 24 Oct 2026 | Use amounts as written in the supplied texts (post-7574 amendments); where a text still shows an old figure (KTK m.34: 235 TL / 488 TL), keep it and note the yearly revaluation                                                                                                                                                                                             | The set must match the corpus; the note stops evaluators marking a correct, text-faithful answer as outdated                                                                                                                                                                                                                                                                             | S14, S23–S30                  |
| D13 | 24 Oct 2026 | Do not resolve conflicts between texts; the gold answer states both provisions with their sources                                                                                                                                                                                                                                                                            | Deciding which norm prevails is legal interpretation, outside the bot's job                                                                                                                                                                                                                                                                                                              | S15, S18                      |
| D14 | 24 Oct 2026 | Treat penalty-point values as out of scope                                                                                                                                                                                                                                                                                                                                   | KTY Ek-35 (the point table) is not in the corpus                                                                                                                                                                                                                                                                                                                                         | S18, S25                      |
| D15 | 24 Oct 2026 | Add a note to every question whose answer lives in a table                                                                                                                                                                                                                                                                                                                   | PDF-to-text extraction breaks tables; these questions test chunking                                                                                                                                                                                                                                                                                                                      | S04, S06                      |
| D16 | 24 Oct 2026 | Publish the set in four formats: HTML page, CSV (UTF-8 BOM), JSONL and Word                                                                                                                                                                                                                                                                                                  | HTML for browsing, CSV for Excel, JSONL for the eval pipeline, Word at the team's request                                                                                                                                                                                                                                                                                                | Distribution                  |
| D17 | 24 Oct 2026 | Use the English type labels from the task definition; keep all content in Turkish                                                                                                                                                                                                                                                                                            | Matches the project spec; the corpus and users are Turkish                                                                                                                                                                                                                                                                                                                               | Type field                    |
| D18 | 25 Oct 2026 | Check the KTY m.100 speed table against the PDF image, not the extracted text                                                                                                                                                                                                                                                                                                | Extracted text put the bicycle row next to the dangerous-goods values (30/50/60/70); the image shows 30/45/45/no motorway                                                                                                                                                                                                                                                                | S06, S25                      |
| D19 | 25 Oct 2026 | When the question leaves a key fact open, list every case (e.g. S25 gives the result for every possible speed limit)                                                                                                                                                                                                                                                         | Team asked for answers covering all possibilities; also shows whether the bot states its assumptions                                                                                                                                                                                                                                                                                     | S12, S18, S25                 |
| D20 | 25 Oct 2026 | Keep the question type tied to the cited articles; reclassify when references change                                                                                                                                                                                                                                                                                         | Type is a property of the evidence, not the wording                                                                                                                                                                                                                                                                                                                                      | S06 (kept), S15 (changed)     |
| D21 | 27 Oct 2026 | Correct the earlier note on the S15 conflict: the 10% tolerance and KTK m.51 agree at a 50 km/h limit and clash only at higher limits                                                                                                                                                                                                                                        | Arithmetic check showed the original note overstated the conflict                                                                                                                                                                                                                                                                                                                        | S15                           |
| D22 | 10 Nov 2026 | Review the set against the literature review "Building test datasets for RAG" (method families A–E and its three validation checks)                                                                                                                                                                                                                                          | Check coverage against published practice before the set is used as the fixed benchmark. Found: every record has question, gold answer and evidence; good everyday-wording coverage (S23–S30). Gaps: no search-query phrasing, no false-premise or in-domain unanswerable questions, no expert or non-Turkish users, no time-sensitivity label, and a Type field that mixes several axes | Whole set (no record changed) |
| D23 | 10 Nov 2026 | Tag the 40 records on 11 independent axes (source scope, hop type, premise, wording, phrasing, user, language, question word, multi-part, answerability, time-sensitive) in a separate analysis file; the Type field and all record contents stay as they are                                                                                                                | Lets results be reported per slice. Source scope is counted at article level, so it differs from Type only for S11 (all references are in KURS m.15). K02 and K09 are tagged as out of scope with a related provision, in line with D11                                                                                                                                                  | Analysis file only            |
| D24 | 10 Nov 2026 | Draft 23 candidate questions (N01–N23) for the gaps in D22: search queries, false premises, chain and comparison questions, expert and English-speaking users, time-sensitive and conflicting-source cases (e.g. N16: KTK m.48/9 gives 5 years, KTY m.97 still says 2), an in-domain unanswerable question, "why" and "what to do" questions, and a contrastive pair for S08 | Shows what closing each gap would take. Answers come only from the six texts (D02); each candidate records why it was added                                                                                                                                                                                                                                                              | Candidate file only           |
| D25 | 10 Nov 2026 | Keep the original 40-record set as the gold set; do not merge N01–N23. The candidates stay in their own file                                                                                                                                                                                                                                                                 | Team's final decision. The original set meets the task definition (30 + 10, D03) and has been through team review, which the candidates have not. Keeps results comparable with earlier runs                                                                                                                                                                                             | Whole set (unchanged)         |

## Revision history

Newest first. Every change below was made in all four formats.

| Version | Date        | Change                                                                                                                                                                                                                                                                                               | Records       |
|---------|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| v1.4    | 10 Nov 2026 | No record changed, so the four formats are unchanged. Datasheet updated with decisions D22–D25 (literature review, axis tagging, 23 candidate questions kept outside the set) and two companion analysis files                                                                                       | None          |
| v1.4    | 27 Oct 2026 | KTK m.51 added to the references; type changed from "Several articles of one text" to "Articles of several texts"; answer now works out where the 10% tolerance and the KTK fine bands agree and where they clash. Distribution became 8 / 6 / 8 / 8                                                 | S15           |
| v1.3    | 25 Oct 2026 | Team reworded three questions; answers rewritten to cover every case. S12 adds monocular drivers, aphakia and the shared eye rules. S18 adds the 2nd and 3rd 100-point cases and the point-carry rules. S25 drops the stated 50 km/h limit and gives results for limits of 20, 30, 40, 50, 70 and 82 | S12, S18, S25 |
| v1.3    | 25 Oct 2026 | Answer now gives the fine amounts as written in KTK m.34, plus the KTK m.35 rules (5% per month late fee, months rounded up, yearly revaluation, the President's 20% power), Ek Madde 3 revaluation and the 7-working-day permit in KTY m.125/f-15                                                   | S27           |
| v1.2    | 25 Oct 2026 | Question broadened to "Hız sınırları nedir?"; answer now covers the full KTY m.100 table and paragraphs 2–8. Type unchanged (single article)                                                                                                                                                         | S06           |
| v1.1    | 24 Oct 2026 | Type labels switched to the English labels from the task definition                                                                                                                                                                                                                                  | All           |
| v1.0    | 24 Oct 2026 | First release: 30 in-scope + 10 out-of-scope questions                                                                                                                                                                                                                                               | All           |

## Known limitations

- **No legal review.** No lawyer has checked the answers. They were built by one AI-assisted pass and reviewed by the team.

- **Frozen corpus.** The answers reflect the six PDFs as supplied on 24 Oct 2026. Any amendment published since then is not in the set.

- **Amounts may differ from current practice.** Some fines in the texts (e.g. KTK m.34) are not yet revalued. The real amounts are higher under KTK Ek Madde 3.

- **Synthetic questions.** The questions are written by hand, not sampled from real user logs. Their wording may not match how users actually ask.

- **Coverage gaps.** The 10 Nov 2026 review (D22) found no search-query questions, no false-premise or in-domain unanswerable questions, no expert or non-Turkish users and no time-sensitivity label. Candidate questions for these gaps exist (N01–N23) but are not part of the set (D25).

- **Missing annex.** Without KTY Ek-35, nothing in the set tests penalty points.

- **Long gold answers.** The rewritten S06, S12, S18, S25 and S27 answers list many cases. Exact-match scoring will be unfair on these, so a rubric or LLM judge is needed.

- **Single reference style.** References use one notation (m.48/5). A bot that cites correctly but in another style needs normalising before scoring.

- **Text conflicts.** S15 and S18 have no single correct legal outcome. They should be scored on whether both provisions are given with their sources.

## Intended uses

The set is meant for offline evaluation of this project's RAG chatbot, rerun after each pipeline change. It is not meant for training, fine-tuning or legal advice.

| What to score       | Records | Suggested measure                                                                     |
|---------------------|---------|---------------------------------------------------------------------------------------|
| Retrieval           | S01–S30 | Recall@k: share of references articles found in the top-k chunks                      |
| Answer faithfulness | S01–S30 | Rubric or LLM judge against gold_answer: key facts present, nothing outside the texts |
| Citation accuracy   | S01–S30 | Cited articles match references after normalising the notation                        |
| Refusal             | K01–K10 | Refusal rate; any invented figure or citation counts as a failure                     |
| Breakdowns          | All     | Report each score by type and by text to find weak spots                              |

