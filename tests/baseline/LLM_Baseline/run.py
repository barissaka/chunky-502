"""LLM baseline koşusu (E3): tüm dokümanlar bağlamda, Claude'a soruları sorar, cevapları kaydeder.

Kullanım (tests/baseline klasöründen):
  python llm/run.py --count-only                      # korpusun token sayısı, ücretsiz
  python llm/run.py --runs 1 --out llm/run2/results.jsonl
Varsayılanlar: sorular ../trial_full_20.json, metinler llm/corpus/, prompt llm/prompts/baseline_v1_system.txt
Gerekli: pip install anthropic ; ANTHROPIC_API_KEY ortam değişkeni
docs/ klasöründe: KTK.txt, KTY.txt, MUAYENE.txt, KURS.txt, SAĞLIK.txt, SKUTER.txt
"""
import argparse, datetime, hashlib, importlib.metadata as md, json, pathlib, re, time
import anthropic

# Sistem promptu prompts/ klasöründeki dosyadan okunur. Değiştirmek için yeni dosya ekle, eskisini düzenleme.


def load_docs(folder):
    docs = {}
    for p in sorted(pathlib.Path(folder).glob("*.txt")):
        docs[p.stem.upper()] = p.read_text(encoding="utf-8")
    if not docs:
        raise SystemExit(f"{folder} içinde .txt bulunamadı")
    return docs


def parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def main():
    ap = argparse.ArgumentParser()
    here = pathlib.Path(__file__).resolve().parent
    ap.add_argument("--questions", default=str(here.parent / "trial_full_20.json"))
    ap.add_argument("--docs", default=str(here / "corpus"))
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--out", default=str(here / "run2" / "results.jsonl"))
    ap.add_argument("--prompt", default=str(here / "prompts" / "baseline_v1_system.txt"))
    ap.add_argument("--count-only", action="store_true", help="sadece korpusun token sayısını yazdır, soru sorma")
    ap.add_argument("--limit", type=int, default=None, help="sadece ilk N soruyu sor (deneme için)")
    a = ap.parse_args()

    if not a.count_only and pathlib.Path(a.out).exists():
        raise SystemExit(f"{a.out} zaten var; önceki sonuçların üzerine yazmamak için başka bir --out ver")
    if not a.count_only:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    docs = load_docs(a.docs)
    questions = json.load(open(a.questions, encoding="utf-8"))[: a.limit]
    context = "<dokumanlar>\n" + "\n\n".join(
        f'<dokuman kod="{k}">\n{v}\n</dokuman>' for k, v in docs.items()) + "\n</dokumanlar>"
    prompt_text = pathlib.Path(a.prompt).read_text(encoding="utf-8")
    system = prompt_text.format(codes=", ".join(docs))
    client = anthropic.Anthropic(max_retries=6)  # 429/529 hatalarında otomatik bekleyip tekrar dener

    if a.count_only:
        c = client.messages.count_tokens(model=a.model, system=system,
                                         messages=[{"role": "user", "content": context}])
        print(f"Korpus + sistem promptu: {c.input_tokens:,} token")
        return

    sha = lambda b: hashlib.sha256(b).hexdigest()[:16]
    meta = {
        "started_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "model": a.model, "runs": a.runs, "n_questions": len(questions),
        "questions_file": a.questions, "questions_sha256": sha(pathlib.Path(a.questions).read_bytes()),
        "prompt_file": a.prompt, "prompt_sha256": sha(prompt_text.encode()),
        "docs_sha256": {k: sha(v.encode()) for k, v in docs.items()},
        "packages": {p: md.version(p) for p in ["anthropic"]},
        "results_file": a.out,
    }
    tot = {"input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0, "cache_write_tokens": 0, "latency_s": 0.0}

    with open(a.out, "w", encoding="utf-8") as f:
        for run in range(1, a.runs + 1):
            for q in questions:
                t0 = time.time()
                # Not: Sonnet 5.5 varsayılan dışı temperature/top_p/top_k değerlerinde 400 hatası verir,
                # bu yüzden temperature gönderilmiyor; tekrarlanabilirlik 3 koşuyla ölçülüyor.
                # max_tokens geniş tutuldu: model uyarlanabilir düşünme (adaptive thinking) kullanabilir.
                r = client.messages.create(
                    model=a.model, max_tokens=16000,
                    system=system,
                    messages=[{"role": "user", "content": [
                        # dokümanlar her çağrıda aynı -> prompt cache ile maliyet düşer
                        {"type": "text", "text": context, "cache_control": {"type": "ephemeral"}},
                        {"type": "text", "text": f"Soru: {q['question']}"},
                    ]}],
                )
                # yanıtta düşünme blokları olabilir; yalnızca metin bloklarını al
                raw = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
                parsed = parse_json(raw) or {}
                rec = {
                    "run": run, "id": q["id"], "model": a.model,
                    "answer": parsed.get("answer", raw),
                    "citations": parsed.get("citations", []),
                    "pred_in_scope": parsed.get("in_scope"),
                    "parse_ok": bool(parsed),
                    "latency_s": round(time.time() - t0, 2),
                    "input_tokens": r.usage.input_tokens,
                    "output_tokens": r.usage.output_tokens,
                    "cache_read_tokens": getattr(r.usage, "cache_read_input_tokens", 0) or 0,
                    "cache_write_tokens": getattr(r.usage, "cache_creation_input_tokens", 0) or 0,
                    "stop_reason": r.stop_reason,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
                for k in tot: tot[k] += rec[k]
                # tahmini maliyet: Sonnet 5.5 — girdi 2 $/M, cache yazma 2,5 $/M, cache okuma 0,2 $/M, çıktı 10 $/M
                cost = (rec["input_tokens"] * 2 + rec["cache_write_tokens"] * 2.5
                        + rec["cache_read_tokens"] * 0.2 + rec["output_tokens"] * 10) / 1e6
                tot_cost = getattr(main, "_cost", 0) + cost; main._cost = tot_cost
                print(f"run{run} {q['id']} ok={rec['parse_ok']} {rec['latency_s']}s | "
                      f"cache yazma={rec['cache_write_tokens']:,} okuma={rec['cache_read_tokens']:,} "
                      f"çıktı={rec['output_tokens']:,} | ~{cost:.2f} $ (toplam ~{tot_cost:.2f} $)")

    meta["finished_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    meta["totals"] = {k: round(v, 1) for k, v in tot.items()}
    meta_path = pathlib.Path(a.out).with_suffix(".meta.json")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Meta bilgiler: {meta_path}")


if __name__ == "__main__":
    main()
