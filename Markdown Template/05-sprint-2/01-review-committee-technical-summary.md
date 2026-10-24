# Sprint 2: Review Committee Technical Summary

**Note: this document uses HTML tags to disable rendering of instructions. View the raw file for further details.**

**Suggestion: You can use tools like [marp](https://github.com/marp-team/marp-cli) to convert this to a presentation for your end-of-sprint demo.**

<!--
- This is a document where you will summarize experiments ran this sprint, their metrics, and results. Experiments are recorded in detail in experiment cards in the Markdown Template/12-experiment-cards/ folder. You should only link the relevant experiment here and report it's main results in here.
- Keep the summary to two pages at most. Link to details rather than repeating them: config/rag.yaml holds only the product configuration, each experiment card records the parameter space it tested, the tested combinations are in W&B, and decisions are in the design document.
-->

| Team | Sprint | Last updated |
|---|---|---|
|  |  | yyyy-mm-dd |

## 1. Summary

<!-- In 3 to 5 sentences: what you tried this sprint, the main result compared with the baseline and the target, and what you will do next. -->

**Decisions this sprint:** <!-- Links to the decision records in the design document, for example D3, D4. -->

## 2. Metrics

<!-- Fill this in during Sprint 2. Change it later only if a metric changes, and explain why in section 1. Take each target from the charter's success criteria. -->

| Metric | Why it fits | Target |
|---|---|---|
|  |  |  |

## 3. Results

<!--
- Include the baseline, the best experiment from earlier sprints if it is not the baseline, and every experiment run this sprint. In the Sprint column, write the sprint each experiment ran in.
- Each row shows the experiment's best combination. Link that run in W&B.
- Run every row on the same evaluation set. If the set changes, run the baseline and the earlier best again on the new set.
- Run the best combination again n times with different seeds. Report each score as the mean ± std over those repeats, and bold the best value in each column.
- Write "null" for missing or failed outputs, and explain it under the table. Do not record them as 0.
- Leave out deprecated experiments.
- In Sprint 4, add a row for the product configuration in config/rag.yaml.
-->

**Evaluation set:** `docs/eval/eval-set-v?.csv`

| Experiment | Sprint | Best run (W&B) | Metric 1 | Metric 2 | Repeats (n) |
|---|---|---|---|---|---|
| Target (charter) | — | — |  |  | — |
| [E1 Baseline](../12-experiment-cards/E1-baseline.md) | 2 | link |  |  |  |
| [E2 short-name](../12-experiment-cards/E2-short-name.md) |  | link |  |  |  |

**Best configuration:** <!-- From Sprint 3 on. Link its W&B run, and say whether config/rag.yaml now uses it. -->

## 4. User story test results

<!-- From Sprint 3 on. Add one row for each user story you have built. The tests themselves are in the story requirements. -->

| Story | Result | Note |
|---|---|---|
|  | pass / fail |  |

## Checklist before submitting

- [ ] The summary is two pages or shorter.
- [ ] Every row in Results links to an experiment card. Every card from this sprint either has a row or is marked deprecated.
- [ ] Every decision in section 1 has a record in the design document.
