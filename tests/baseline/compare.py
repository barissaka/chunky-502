"""RAG ile baseline (E3) karşılaştırması: aynı 10 kapsam içi soru, aynı hakem ve rubrik.

Kullanım:
  python compare.py --rag rag/scores_rag.csv --baseline llm/run1/scores.csv --out rag/comparison
Çıktı: rag/comparison.csv (soru bazında) ve rag/comparison.md (özet tablolar)

Not: fıkra metrikleri (para_*) ve yanlış ret oranı karşılaştırmaya alınmaz:
RAG madde düzeyinde atıf veriyor ve henüz kapsam bayrağı (pred_in_scope) yok.
"""
import argparse
import pandas as pd

METRICS = ["judge_score", "art_P", "art_R", "art_F1"]


def load(path, label):
    d = pd.read_csv(path)
    d = d[d.scope == "in"].copy()
    if "judge_score" not in d:
        raise SystemExit(f"{path}: judge_score sütunu yok; eval.py --judge ile çalıştırılmalı")
    d["judge_pass"] = d.judge_score >= 0.7
    keep = ["id", "type", "hop_type"] + METRICS + ["judge_pass", "latency_s"]
    return d[keep].rename(columns={c: f"{c}_{label}" for c in METRICS + ["judge_pass", "latency_s"]})


def fmt(x):
    return "—" if pd.isna(x) else f"{x:.2f}"


def main():
    ap = argparse.ArgumentParser()
    here = __import__("pathlib").Path(__file__).resolve().parent
    ap.add_argument("--rag", default=str(here / "rag" / "scores_rag.csv"))
    ap.add_argument("--baseline", default=str(here / "llm" / "run1" / "scores.csv"))
    ap.add_argument("--out", default=str(here / "rag" / "comparison"))
    a = ap.parse_args()

    r, b = load(a.rag, "rag"), load(a.baseline, "base")
    m = r.merge(b.drop(columns=["type", "hop_type"]), on="id", how="outer", indicator=True)
    if (m["_merge"] != "both").any():
        raise SystemExit("İki dosyadaki soru kimlikleri uyuşmuyor: "
                         + ", ".join(m.loc[m["_merge"] != "both", "id"]))
    m = m.drop(columns="_merge")
    m["judge_diff"] = (m.judge_score_rag - m.judge_score_base).round(3)
    m.to_csv(a.out + ".csv", index=False, encoding="utf-8-sig")

    lines = ["# RAG vs baseline (E3): 10 in-scope questions, same judge (claude-opus-5-5); E3 judged before D32 added one rubric step", ""]
    lines += ["| Metric | RAG | Baseline (E3) | Difference |", "|---|---|---|---|"]
    for k in METRICS:
        x, y = m[f"{k}_rag"].mean(), m[f"{k}_base"].mean()
        lines.append(f"| {k} | {fmt(x)} | {fmt(y)} | {fmt(x - y)} |")
    lines.append(f"| judge pass (≥ 0.7) | {int(m.judge_pass_rag.sum())} / {len(m)} | {int(m.judge_pass_base.sum())} / {len(m)} | |")
    lines.append(f"| mean latency (s) | {fmt(m.latency_s_rag.mean())} | {fmt(m.latency_s_base.mean())} | |")

    for col, title in [("type", "By question type"), ("hop_type", "By hop type")]:
        g = m.groupby(col)
        lines += ["", f"## {title}", "", f"| {col} | n | Judge RAG | Judge baseline | Article R RAG | Article R baseline |", "|---|---|---|---|---|---|"]
        for k, d in g:
            lines.append(f"| {k} | {len(d)} | {fmt(d.judge_score_rag.mean())} | {fmt(d.judge_score_base.mean())} "
                         f"| {fmt(d.art_R_rag.mean())} | {fmt(d.art_R_base.mean())} |")

    lines += ["", "## Per question", "", "| ID | Judge RAG | Judge baseline | Difference | Article R RAG | Article R baseline |", "|---|---|---|---|---|---|"]
    for _, x in m.sort_values("id").iterrows():
        lines.append(f"| {x.id} | {fmt(x.judge_score_rag)} | {fmt(x.judge_score_base)} | {fmt(x.judge_diff)} "
                     f"| {fmt(x.art_R_rag)} | {fmt(x.art_R_base)} |")
    lines += ["", "Paragraph metrics and the false-refusal rate are left out: the RAG system cites at article level and has no in_scope flag yet."]
    open(a.out + ".md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))
    print(f"\nKaydedildi: {a.out}.csv, {a.out}.md")


if __name__ == "__main__":
    main()
