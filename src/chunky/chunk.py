"""Split the clean texts into one chunk per article (AD-08) with metadata.

Reads data/clean/*.txt and data/legal/documents.yaml, writes
data/chunks/chunks.jsonl (one JSON object per line).

Units that become chunks:
- articles in the body: "Madde 37", "Ek Madde 3", "Geçici Madde 27", "Madde 65/A";
- annexes: "1 SAYILI CETVEL", "EK-1", "(1) Sayili Liste" (articles inside an annex stay in it);
- the Law's "İŞLENEMEYEN HÜKÜMLER" section, as one chunk.

For an article, the lines just before the next article header are not part
of its text: they hold the next article's heading ("Amaç") and, at a
section break, the KISIM / BÖLÜM lines. These become the next chunk's
article_heading and section.

Sub-chunks for articles longer than the embedding model's input limit
(AD-08) are added in the indexing step, once the model is chosen.

Run from the repository root:  python -m chunky.chunk
"""

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CLEAN_DIR = ROOT / "data" / "clean"
DOCS_FILE = ROOT / "data" / "legal" / "documents.yaml"
OUT_FILE = ROOT / "data" / "chunks" / "chunks.jsonl"

# Article header; the dash varies: "–", "-", "—" and "‒" (KTY Art. 160)
ARTICLE = re.compile(r"^(?P<kind>Ek |Geçici |EK |GEÇİCİ )?(?:Madde|MADDE)\s+(?P<no>\d+(?:/[A-ZÇ])?)\s*[–\-—‒]")
SECTION = re.compile(r"^[A-ZÇĞİÖŞÜ ]+ (?:KISIM|BÖLÜM)$")          # "BİRİNCİ KISIM", "ON BİRİNCİ BÖLÜM"
# Starts of the units after the body, with (id part, label) builders
TAIL_UNITS = [
    (re.compile(r"^İŞLENEMEYEN HÜKÜMLER$"), lambda m: ("islenemeyen", "İşlenemeyen Hükümler")),
    (re.compile(r"^(\d+) SAYILI CETVEL$"), lambda m: (f"cetvel{m[1]}", f"{m[1]} Sayılı Cetvel")),
    (re.compile(r"^\((\d+)\) Sayılı Liste$"), lambda m: (f"liste{m[1]}", f"({m[1]}) Sayılı Liste")),
    (re.compile(r"^(?:\(Mülga[^)]*\) )?EK-(\d+)\*?$"), lambda m: (f"ek{m[1]}", f"EK-{m[1]}")),
]
ADDED_BY = re.compile(r"^\(Ek:[^)]*\)$")                              # "(Ek:6/12/2019-7196/42 md.)" before an annex
ANNOTATION_IN_TEXT = re.compile(r"\s*\((?:Değişik|Ek)[^)]*\)")       # "(Değişik başlık: RG-...)" in a heading
KIND = {"": ("m", "Madde"), "E": ("ekm", "Ek Madde"), "G": ("gm", "Geçici Madde")}  # by first letter: Ek / EK, Geçici / GEÇİCİ


def is_heading(line: str) -> bool:
    """An article heading is a short line that does not read like a sentence or a list item."""
    return (len(line) <= 120 and not line.endswith((".", ";", ","))
            and not re.match(r"^(\(?\d+\)|[a-zçğıöşü]\))", line) and " | " not in line)


def find_units(lines: list[str]) -> list[dict]:
    """Every unit start in the text, in order: body articles, then tail units."""
    units = []
    for i, line in enumerate(lines):
        for pattern, build in TAIL_UNITS:
            if m := pattern.match(line):
                part, label = build(m)
                start, floor = i, (units[-1]["start"] + 1 if units else 0)
                while start > floor and (lines[start - 1].isupper() or ADDED_BY.match(lines[start - 1])):
                    start -= 1                                # its title line or "(Ek:...)" note
                units.append({"start": start, "part": part, "label": label, "tail": True})
                break
        else:
            m = ARTICLE.match(line)
            in_tail = any(u["tail"] for u in units)          # articles inside an annex stay in it
            if m and not in_tail:
                prefix, word = KIND[(m["kind"] or "")[:1]]
                no = m["no"]
                part = prefix + no.replace("/", "")
                if any(u["part"] == part for u in units):    # a repeat is quoted old text (KTY Art. 80)
                    continue
                units.append({"start": i, "part": part, "label": f"{word} {no}", "tail": False})
    return units


def split_preamble(lines: list[str], start: int, end: int) -> tuple[int, str | None, list[str]]:
    """Look at the lines just before an article header (lines[start:end]).

    Returns (where the previous text ends, heading of the article, section lines).
    """
    sec = None
    for i in range(end - 1, max(start, end - 8) - 1, -1):    # a section block is a few lines long
        if SECTION.match(lines[i]):
            sec = i
    heading = None
    if end - 1 >= start and is_heading(lines[end - 1]) and (sec is None or end - 1 > sec + 1):
        heading = ANNOTATION_IN_TEXT.sub("", lines[end - 1]).rstrip(":").strip()
    if sec is not None:
        return sec, heading, lines[sec:end - 1 if heading else end]
    return (end - 1 if heading else end), heading, []


def update_section(state: dict, section_lines: list[str]) -> None:
    """Fold KISIM / BÖLÜM lines into the current section path."""
    marker, titles = None, []
    for line in section_lines + ["END KISIM"]:
        if SECTION.match(line):
            if marker:
                text = f"{marker} – {' '.join(titles)}".rstrip(" –")
                if marker.endswith("KISIM"):
                    state["kisim"], state["bolum"] = text, None
                else:
                    state["bolum"] = text
            marker, titles = line, []
        else:
            titles.append(line)


def chunk_document(name: str, doc: dict) -> list[dict]:
    lines = (CLEAN_DIR / f"{name}.txt").read_text(encoding="utf-8").splitlines()
    units = find_units(lines)
    state = {"kisim": None, "bolum": None}
    chunks = []
    for k, u in enumerate(units):
        nxt = units[k + 1] if k + 1 < len(units) else None
        end = nxt["start"] if nxt else len(lines)
        if nxt and not nxt["tail"]:                    # the next article's heading/section lines are not ours
            end = split_preamble(lines, u["start"] + 1, end)[0]
        heading = None
        if not u["tail"]:
            prev_end = units[k - 1]["start"] + 1 if k else 0
            _, heading, section_lines = split_preamble(lines, prev_end, u["start"])
            update_section(state, section_lines)
        article_id = f"{doc['doc_code']}-{u['part']}"
        chunks.append({
            "chunk_id": article_id,
            "article_id": article_id,
            "doc_code": doc["doc_code"],
            "doc_title": doc["doc_title"],
            "doc_type": doc["doc_type"],
            "article_label": u["label"],
            "article_heading": heading,
            "section": None if u["tail"] else " > ".join(s for s in (state["kisim"], state["bolum"]) if s) or None,
            "source_url": doc["source_url"],
            "accessed": str(doc["accessed"]),
            "version_date": str(doc["version_date"]),
            "text": "\n".join(lines[u["start"]:end]),
        })
    return chunks


def main() -> None:
    docs = {d["file"]: d for d in yaml.safe_load(DOCS_FILE.read_text(encoding="utf-8"))["documents"]}
    all_chunks = []
    for name, doc in docs.items():
        chunks = chunk_document(name, doc)
        all_chunks.extend(chunks)
        n_articles = sum(1 for c in chunks if c["article_label"].split()[0] in ("Madde", "Ek", "Geçici"))
        print(f"{name:25} {len(chunks):4} chunks ({n_articles} articles, {len(chunks) - n_articles} other)")
    ids = [c["chunk_id"] for c in all_chunks]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise SystemExit(f"Duplicate chunk ids: {dupes}")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8", newline="\n") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"{len(all_chunks)} chunks -> {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
