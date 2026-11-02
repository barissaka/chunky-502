"""Extract clean text from the Word sources (D1).

Reads data/legal/word/*.docx and writes one UTF-8 text file per document
to data/clean/, one line per paragraph or table row.

What is removed:
- footnotes (Word keeps them outside the body, so they are never read),
- note markers: footnote references, their repeats (NOTEREF fields) and
  superscript runs such as "(11)" or "8",
- the notes block at the end of a text and the amendment-history table
  that follows it ("Yönetmeliğin Yayımlandığı Resmî Gazete..."),
- "Ekleri için tıklayınız" link lines.

Tables inside the text (for example the speed-limit table in KTY Art. 100)
are kept in reading order, one row per line, cells separated by " | ".

Run from the repository root:  python -m chunky.extract
"""

import re
import unicodedata
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "data" / "legal" / "word"
OUT_DIR = ROOT / "data" / "clean"

# First row of an amendment-history table
HISTORY_TABLE = re.compile(r"Yayımlandığı Resmî Gazete|Değiştiren Kanunun")
# Lines that open the notes block before that table
NOTES_START = re.compile(
    r"^_{3,}$"                                  # separator line: _________
    r"|^Ekleri? için tıklayınız\.?$"            # link to annexes on the website
    r"|EK VE DEĞİŞİKLİK GETİREN MEVZUAT"        # heading of the Law's history table
    r"|YÜRÜRLÜĞE GİRİŞ$|GÖSTERİR TABLO$"
)
# Article header: "Madde 5 –", "MADDE 16/A-", "Ek Madde 2 –", "GEÇİCİ MADDE 1–"
ARTICLE_HEADER = re.compile(r"^(?:Ek |Geçici |EK |GEÇİCİ )?(?:Madde|MADDE)\s+\d+(?:/[A-ZÇ])?\s*[–\-—]")


def clean(text: str) -> str:
    """Normalise spaces and drop unassigned code points left by encoding errors."""
    text = "".join(c for c in text if unicodedata.category(c) != "Cn")
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def is_marker(run: Run) -> bool:
    """Footnote references, superscript note markers, or raised text (files converted from HTML)."""
    if run._r.find(qn("w:footnoteReference")) is not None or run.font.superscript:
        return True
    pos = run._r.rPr.find(qn("w:position")) if run._r.rPr is not None else None
    return pos is not None and int(pos.get(qn("w:val"), "0")) > 0


def paragraph_text(p: Paragraph) -> str:
    parts = []
    instr, in_noteref = "", False             # a NOTEREF field repeats a footnote number
    for r in p._p.iter(qn("w:r")):           # also finds runs inside hyperlinks
        fld = r.find(qn("w:fldChar"))
        if fld is not None:
            kind = fld.get(qn("w:fldCharType"))
            if kind == "begin":
                instr = ""
            elif kind == "separate":
                in_noteref = "NOTEREF" in instr
            elif kind == "end":
                in_noteref = False
            continue
        if r.find(qn("w:instrText")) is not None:
            instr += r.find(qn("w:instrText")).text or ""
            continue
        run = Run(r, p)
        if in_noteref or is_marker(run):
            parts.append(" " if run.text.isspace() else "")  # drop note markers
        else:
            parts.append(run.text)
    return clean("".join(parts))


def table_lines(t: Table) -> list[str]:
    lines = []
    for row in t.rows:
        cells, seen = [], set()
        for cell in row.cells:               # merged cells repeat; keep them once
            if id(cell._tc) in seen:
                continue
            seen.add(id(cell._tc))
            cells.append(" ".join(paragraph_text(p) for p in cell.paragraphs).strip())
        if any(cells):
            lines.append(" | ".join(cells))
    return lines


def blocks(path: Path) -> list[tuple[str, object]]:
    """Body content in reading order: ("p", text) or ("t", Table)."""
    d = docx.Document(path)
    out = []
    for el in d.element.body.iterchildren():
        if el.tag == qn("w:p"):
            text = paragraph_text(Paragraph(el, d))
            if text:
                out.append(("p", text))
        elif el.tag == qn("w:tbl"):
            out.append(("t", Table(el, d)))
    return out


def drop_notes_and_history(items: list[tuple[str, object]]) -> list[tuple[str, object]]:
    """Remove the amendment-history table and the notes block just before it."""
    for h, (kind, obj) in enumerate(items):
        if kind == "t" and HISTORY_TABLE.search(" ".join(c.text for c in obj.rows[0].cells)):
            break
    else:
        return items                          # no history table in this text
    # Walk back to the last article header; the notes block starts at the
    # earliest marker line found on the way. No marker: only the table goes.
    start, i = h, h - 1
    while i >= 0 and not (items[i][0] == "p" and ARTICLE_HEADER.match(items[i][1])):
        if items[i][0] == "p" and NOTES_START.search(items[i][1]):
            start = i
        i -= 1
    return items[:start] + items[h + 1:]


def extract(path: Path) -> list[str]:
    lines = []
    for kind, obj in drop_notes_and_history(blocks(path)):
        if kind == "p":
            if not NOTES_START.match(obj):    # stray "Ekleri için tıklayınız"
                lines.append(obj)
        else:
            lines.extend(table_lines(obj))
    return lines


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(SRC_DIR.glob("*.docx")):
        lines = extract(path)
        out = OUT_DIR / f"{path.stem}.txt"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"{path.stem:25} {len(lines):5} lines -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
