"""Convert a Jira 'Export Excel CSV (all fields)' of project CHUNKY into Volga's
docs/backlog epic-file format (one file per epic + _imported-unsorted.md).
Usage: python jira2md.py Jira.csv outdir
"""
import csv, re, sys, collections
from pathlib import Path

SRC, OUT = sys.argv[1], Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://chunky-502.atlassian.net/browse/"

rows = list(csv.reader(open(SRC, encoding="utf-8-sig")))
h = rows[0]
ix = {}
for i, c in enumerate(h):
    ix.setdefault(c, i)
sprint_cols = [i for i, c in enumerate(h) if c == "Sprint"]
ac_col = ix.get("Custom field (Acceptance Criteria)")

def cell(s):  # one-line, pipe-safe markdown cell
    s = (s or "").replace("\r", "").strip()
    s = re.sub(r"\s*\n+\s*", " ", s)
    return s.replace("|", "\\|")

def link(key): return f"[{key}]({BASE}{key})"
def hours(sec):
    try: return f"{int(sec)//3600}h" if sec else ""
    except ValueError: return ""

issues = {}
for r in rows[1:]:
    key = r[ix["Issue key"]]
    issues[key] = dict(
        key=key, type=r[ix["Issue Type"]], summary=r[ix["Summary"]].strip(),
        desc=r[ix["Description"]], prio=r[ix["Priority"]], status=r[ix["Status"]],
        owner=r[ix["Assignee"]], points=r[ix["Custom field (Story point estimate)"]],
        sprint=next((r[i] for i in sprint_cols if r[i]), ""), parent=r[ix["Parent key"]],
        est=hours(r[ix["Original estimate"]]), ac=r[ac_col] if ac_col is not None else "",
    )
    it = issues[key]
    m = re.split(r"\n*\s*Acceptance criteria:\s*", it["desc"], maxsplit=1, flags=re.I)
    if len(m) == 2:
        it["desc"], extra = m[0], m[1]
        it["ac"] = (it["ac"] + "\n" + extra).strip()
    it["points"] = re.sub(r"\.0$", "", it["points"])

children = collections.defaultdict(list)
for it in issues.values():
    if it["parent"]: children[it["parent"]].append(it)
for k in children: children[k].sort(key=lambda x: int(x["key"].split("-")[1]))

epics = sorted((i for i in issues.values() if i["type"] == "Epic"), key=lambda x: int(x["key"].split("-")[1]))
HEADER_NOTE = ("<!-- Exported from Jira on {date} (project CHUNKY). Jira is the source of truth for this backlog;\n"
               "     this file is a snapshot for the sprint deliverable and is regenerated before each sprint review. -->\n")
import datetime; today = datetime.date.today().isoformat()

def story_table(stories):
    out = ["| # | User story title | User story description | Priority | Points | Owner | Sprint | Status | Jira |",
           "|---|---|---|---|---|---|---|---|---|"]
    for n, s in enumerate(stories, 1):
        out.append(f"| S{n} | {cell(s['summary'])} | {cell(s['desc'])} | {cell(s['prio'])} | {cell(s['points'])} | {cell(s['owner'])} | {cell(s['sprint'])} | {cell(s['status'])} | {link(s['key'])} |")
    return out

def subtask_table(subs):
    out = ["| Sub-task | Owner | Estimate | Status | Jira |", "|---|---|---|---|---|"]
    for st in subs:
        out.append(f"| {cell(st['summary'])} | {cell(st['owner'])} | {cell(st['est'])} | {cell(st['status'])} | {link(st['key'])} |")
    return out

def task_table(tasks):
    out = ["| Task | Owner | Points | Sprint | Status | Jira |", "|---|---|---|---|---|---|"]
    for t in tasks:
        out.append(f"| {cell(t['summary'])} | {cell(t['owner'])} | {cell(t['points'])} | {cell(t['sprint'])} | {cell(t['status'])} | {link(t['key'])} |")
    return out

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def story_sections(stories):
    out = []
    for n, s in enumerate(stories, 1):
        out += ["", f"## S{n} · {s['summary']}", ""]
        if s["ac"].strip():
            items = [x.strip() for x in re.split(r"\n+|\s+-\s+(?=\S)", s["ac"]) if x.strip()]
            out += ["**Acceptance criteria**", ""] + [f"- {x.lstrip('-* ')}" for x in items] + [""]
        subs = [c for c in children.get(s["key"], []) if c["type"] in ("Subtask", "Sub-task")]
        tasks = [c for c in children.get(s["key"], []) if c["type"] == "Task"]
        if subs: out += ["**Sub-tasks**", ""] + subtask_table(subs)
        if tasks: out += ["", "**Tasks**", ""] + task_table(tasks)
    return out

written = []
for n, ep in enumerate(epics, 1):
    stories = [c for c in children.get(ep["key"], []) if c["type"] == "Story"]
    other = [c for c in children.get(ep["key"], []) if c["type"] == "Task"]
    lines = [f"# Story Requirements for Epic {n:02d} · {ep['summary']}", "", HEADER_NOTE.format(date=today),
             f"| Epic | {cell(ep['summary'])} |", "|---|---|",
             f"| Summary | {cell(ep['desc']) or '—'} |",
             f"| Document Owner | {cell(ep['owner'])} |",
             f"| Release Target (Sprint) | {cell(ep['sprint'])} |",
             f"| Status | {cell(ep['status'])} |",
             f"| Jira | {link(ep['key'])} |", "", "## Requirements", ""] + story_table(stories) + story_sections(stories)
    if other: lines += ["", "## Other tasks", ""] + task_table(other)
    fn = OUT / f"epic-{n:02d}-{slug(ep['summary'])}.md"
    fn.write_text("\n".join(lines) + "\n", encoding="utf-8"); written.append(fn.name)

# issues with no epic: tasks (with their sub-tasks) and stories
orphans = [i for i in issues.values() if not i["parent"] and i["type"] != "Epic"]
orphans.sort(key=lambda x: (x["sprint"] or "zz", int(x["key"].split("-")[1])))
lines = ["# Backlog items without an epic", "", HEADER_NOTE.format(date=today),
         "Engineering tasks (EN-xx) and other work that is planned by sprint rather than under a user-story epic.", ""]
by_sprint = collections.OrderedDict()
for o in orphans: by_sprint.setdefault(o["sprint"] or "No sprint", []).append(o)
for sp, items in by_sprint.items():
    lines += [f"## {sp}", ""] + task_table(items)
    for t in items:
        subs = children.get(t["key"], [])
        if subs: lines += ["", f"**Sub-tasks of {t['key']} · {t['summary']}**", ""] + subtask_table(subs)
    lines.append("")
(OUT / "_imported-unsorted.md").write_text("\n".join(lines) + "\n", encoding="utf-8"); written.append("_imported-unsorted.md")

covered = set()
for ep in epics:
    covered.add(ep["key"])
    for c in children.get(ep["key"], []):
        covered.add(c["key"]); covered.update(x["key"] for x in children.get(c["key"], []))
for o in orphans:
    covered.add(o["key"]); covered.update(x["key"] for x in children.get(o["key"], []))
print("files:", written); print("issues:", len(issues), "covered:", len(covered), "missing:", sorted(set(issues) - covered))
