# E<n>: <experiment title>

**Note: this document uses HTML tags to disable rendering of instructions. View the raw file for further details.**

<!--
- Save one card per experiment as E<n>-<short-name>.md.
- Runs with the same setup count as one experiment.
- Never move or delete a card. When a later experiment supersedes it, change its status to deprecated.
-->

| Date | Author(s) | Status |
|---|---|---|
| yyyy-mm-dd |  | completed / deprecated (superseded by E?) |

**Aim:**
<!-- The question you want to answer, and what you compare against: the baseline or another configuration. -->

**Setup:**
<!--
Links only:
- The public W&B sweep or project. W&B records every combination you tested, including the fixed parameters.
- The evaluation set version.
- The prompt files. To change a prompt, add a new file to prompts/ instead of editing the old one.
-->

**Design:**
<!-- The parameter space you tested. Add one row for each parameter you varied. For the baseline, give the single value each main parameter had. Then give the search method (grid, random or Bayesian) and the number of runs. -->

| Parameter | Values or range tested | Best value |
|---|---|---|
|  |  |  |

**Search method and runs:**

**Summary of Results:**
<!-- The main scores go in the results table of the technical summary. Put the breakdown here: scores by question type, and failures by cause. -->

| Failure cause | Count | % of failures |
|---|---|---|
|  |  |  |

**Discussion and Conclusion:**
<!-- What the numbers mean and what you will do next. Link the decision they led to (D?), if any. -->
