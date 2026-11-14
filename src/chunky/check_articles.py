"""Check that the stored plain-text legal texts match their official source PDFs.

Picks N articles at random (fixed seed, spread over the six texts in proportion to
their article counts), extracts each article from the stored .txt and from the
source PDF (pdftotext -layout), normalises both and compares them.

Usage:  python src/check_articles.py [--seed 502] [--n 20] [--out docs/eval/article-check.md]
Needs:  poppler's pdftotext on PATH.

Normalisation removes what differs by construction between the two extractions:
page breaks, page headers/footers, footnote markers glued to words ("zorunludur.34"),
hyphenation at line ends and whitespace. Everything else must be identical.
"""
import argparse, random, re, subprocess, sys, unicodedata
from pathlib import Path

TEXTS = {
    "01_kanun_2918": "Karayolları Trafik Kanunu (2918)",
    "02_trafik_yonetmeligi": "Karayolları Trafik Yönetmeliği",
    "03_meb_surucu_kursu": "MEB Özel Motorlu Taşıt Sürücüleri Kursu Yönetmeliği",
    "04_surucu_saglik": "Sürücü Adayları ve Sürücülerde Aranacak Sağlık Şartları Yönetmeliği",
    "05_arac_muayene": "Araç Muayene Yönetmeliği",
    "06_elektrikli_skuter": "Elektrikli Skuter Yönetmeliği",
}
HEAD = re.compile(r"^\s*(?:Madde|MADDE)\s+(\d+)\s*(?:[–\-]|$)", re.M)


def split_articles(text: str) -> dict[int, str]:
    """Return {article_no: article_text} for the first occurrence of every article heading."""
    heads = [(m.start(), int(m.group(1))) for m in HEAD.finditer(text)]
    arts: dict[int, str] = {}
    for i, (pos, no) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(text)
        if no not in arts:  # repeated numbers (annex tables, "Ek Madde") keep the first
            arts[no] = text[pos:end]
    return arts


def pdf_text(pdf: Path) -> str:
    out = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    return out


def normalise(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.replace("\f", "\n")
    s = re.sub(r"(?<=[a-zçğıöşüA-ZÇĞİÖŞÜ.,;:)])\d{1,3}(?=\s)", "", s)   # footnote markers glued to text
    s = re.sub(r"-\n\s*", "", s)                                        # hyphenation at line end
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def first_diff(a: str, b: str, ctx: int = 40) -> str:
    n = min(len(a), len(b))
    i = next((k for k in range(n) if a[k] != b[k]), n)
    return f"…{a[max(0,i-ctx):i+ctx]}… | …{b[max(0,i-ctx):i+ctx]}…"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=502)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--data", default="data/legal")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    data = Path(a.data)

    txt_arts, pdf_arts = {}, {}
    for key in TEXTS:
        txt_arts[key] = split_articles((data / f"{key}.txt").read_text(encoding="utf-8"))
        pdf_arts[key] = split_articles(pdf_text(data / "pdf" / f"{key}.pdf"))

    # proportional allocation of N articles, at least one per text
    counts = {k: len(v) for k, v in txt_arts.items()}
    total = sum(counts.values())
    alloc = {k: max(1, round(a.n * c / total)) for k, c in counts.items()}
    while sum(alloc.values()) > a.n:
        k = max(alloc, key=alloc.get); alloc[k] -= 1
    while sum(alloc.values()) < a.n:
        k = max(counts, key=lambda k: counts[k] / alloc[k]); alloc[k] += 1

    rng = random.Random(a.seed)
    rows, identical = [], 0
    for key, k in alloc.items():
        for no in sorted(rng.sample(sorted(txt_arts[key]), k)):
            t = normalise(txt_arts[key][no])
            p = pdf_arts[key].get(no)
            if p is None:
                rows.append((key, no, len(t), "not found in PDF extraction", "")); continue
            p = normalise(p)
            if t == p:
                identical += 1; rows.append((key, no, len(t), "identical", ""))
            else:
                rows.append((key, no, len(t), "differs", first_diff(t, p)))

    lines = [f"Article check — seed {a.seed}, {a.n} articles, {identical}/{a.n} identical", "",
             "| # | Text | Article | Chars | Result | First difference (stored \\| official) |",
             "|---|---|---|---|---|---|"]
    for i, (key, no, ln, res, d) in enumerate(rows, 1):
        lines.append(f"| {i} | {TEXTS[key]} | Madde {no} | {ln} | {res} | {d.replace('|', '\\|')} |")
    lines += ["", f"Articles per text: " + ", ".join(f"{TEXTS[k].split(' (')[0]} {counts[k]}" for k in TEXTS)]
    report = "\n".join(lines)
    print(report)
    if a.out:
        Path(a.out).write_text(report + "\n", encoding="utf-8")
    sys.exit(0 if identical == a.n else 1)


if __name__ == "__main__":
    main()
