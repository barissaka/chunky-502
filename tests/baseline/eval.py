"""Değerlendirme: atıf metrikleri (kural tabanlı) + LLM-judge (DeepEval GEval).

Kullanım:
  python eval.py --questions trial_full_20.json --results results.jsonl --judge claude-opus-5-5
  python eval.py ... --no-judge        # sadece atıf/kapsam metrikleri (API gerektirmez)
Gerekli: pip install deepeval pandas
"""
import argparse, json, pathlib, re
import pandas as pd

FAILURE_CAUSES = [
    "missing_key_fact",      # gold cevaptaki bir şart/süre/tutar/istisna eksik
    "wrong_fact",            # metinle çelişen tutar, süre veya kural
    "outside_knowledge",     # metinde olmayan bilgi (ör. güncel ceza tutarı, kanal)
    "wrong_citation",        # yanlış madde gösterildi
    "missing_citation",      # doğru cevap ama gerekli madde atıfı yok
    "assumed_ambiguity",     # belirsiz soruda tek bir varsayımla cevap (S25 gibi)
    "conflict_not_shown",    # iki metnin çeliştiği yerde yalnızca biri verildi (S15)
    "false_refusal",         # cevaplanabilir soruya "kapsam dışı" dedi
    "oos_fabricated",        # kapsam dışı soruda rakam/kanal/atıf uydurdu
    "oos_not_refused",       # kapsam dışı soruyu kapsam içi gibi cevapladı
    "format_error",          # JSON parse edilemedi / cevap kesildi
    "judge_below_threshold", # hakem < 0.7, gerekçede eksik bilgi ifadesi yok
    "judge_error",           # hakem çağrısı başarısız, puan yok (yeniden çalıştırılmalı)
    "scope_flag_mismatch",   # cevap metni "kapsam dışı" diyor ama in_scope bayrağı true
    "oos_cited_related",     # kapsam dışı soruda doğru ama gereksiz atıf (D28: K02/K09 hariç)
]

DOCS = r"(KTK|KTY|MUAYENE|KURS|SAĞLIK|SAGLIK|SKUTER)"
CIT = re.compile(DOCS + r"\s*(?:m\.|madde|Art\.)?\s*(Ek[- ]?\d+|\d+)(?:/([^\s,;\]\)]+))?", re.I)


def norm_cits(cits):
    """Model atıflarını -> {'KTK 48'} (madde) ve {'KTK 48/5'} (fıkra) kümelerine çevirir."""
    arts, paras = set(), set()
    for c in cits:
        for doc, art, sub in CIT.findall(c):
            doc = doc.upper().replace("SAGLIK", "SAĞLIK")
            art = re.sub(r"(?i)ek[- ]?", "Ek-", art)
            arts.add(f"{doc} {art}")
            if sub:
                paras.add(f"{doc} {art}/{sub}")
    return arts, paras


def _para_key(p):
    """'KTK 48/5', 'SKUTER 5/1-a/4', 'SAĞLIK 9/2(c)(1)' -> ('KTK','48',('5',)) gibi
    gösterimden bağımsız bir anahtar: '/', '(', ')', '-' ayrımı yok sayılır."""
    doc, rest = p.split(" ", 1)
    art, _, sub = rest.partition("/")
    parts = [x for x in re.split(r"[/()\-\s]+", sub.lower()) if x]
    return doc, art, tuple(parts)


def _para_match(a, b):
    """Aynı madde ve biri diğerinin üst/alt birimi ise eşleşir (ör. 9/2-c ile 9/2-c-1, 66/1 ile 66/1-a)."""
    (d1, a1, s1), (d2, a2, s2) = _para_key(a), _para_key(b)
    n = min(len(s1), len(s2))
    return d1 == d2 and a1 == a2 and n > 0 and s1[:n] == s2[:n]


def prf_para(pred, gold):
    if not gold:
        return None, None, None
    p = sum(any(_para_match(x, g) for g in gold) for x in pred) / len(pred) if pred else 0.0
    r = sum(any(_para_match(x, g) for x in pred) for g in gold) / len(gold)
    f = 2 * p * r / (p + r) if p + r else 0.0
    return round(p, 3), round(r, 3), round(f, 3)


def prf(pred, gold):
    if not gold:
        return None, None, None
    tp = len(pred & gold)
    p = tp / len(pred) if pred else 0.0
    r = tp / len(gold)
    f = 2 * p * r / (p + r) if p + r else 0.0
    return round(p, 3), round(r, 3), round(f, 3)


def claude_judge(model_name):
    """DeepEval için Claude hakemi. temperature göndermez (yeni Claude modelleri
    varsayılan dışı temperature'da 400 hatası verir), düşünme bloklarını atlar."""
    import anthropic
    from deepeval.models import DeepEvalBaseLLM

    class ClaudeJudge(DeepEvalBaseLLM):
        def __init__(self):
            self.client = anthropic.Anthropic(max_retries=6)
            self.aclient = anthropic.AsyncAnthropic(max_retries=6)

        def load_model(self):
            return self.client

        @staticmethod
        def _text(r):
            return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")

        REPAIR = ("\n\nÖNEMLİ: Yanıtın yalnızca geçerli bir JSON nesnesi olsun. Metin içindeki çift tırnakları "
                  "\\\" ile kaçır veya tek tırnak kullan; JSON dışında hiçbir şey yazma.")

        @staticmethod
        def _parse(text, schema):
            """Modelin metninden JSON'u çıkarıp DeepEval'in istediği şemaya çevirir."""
            m = re.search(r"\{.*\}", text, re.S)
            if not m:
                raise ValueError("JSON bulunamadı")
            return schema(**json.loads(m.group(0)))

        def generate(self, prompt: str, schema=None):
            last = None
            for attempt in range(3):  # bozuk JSON gelirse en fazla 2 kez daha dener
                r = self.client.messages.create(model=model_name, max_tokens=8000, messages=[
                    {"role": "user", "content": prompt + (self.REPAIR if attempt else "")}])
                text = self._text(r)
                if schema is None:
                    return text
                try:
                    return self._parse(text, schema)
                except Exception as e:
                    last = e
            raise ValueError(f"Hakem 3 denemede geçerli JSON vermedi: {last}")

        async def a_generate(self, prompt: str, schema=None):
            last = None
            for attempt in range(3):
                r = await self.aclient.messages.create(model=model_name, max_tokens=8000, messages=[
                    {"role": "user", "content": prompt + (self.REPAIR if attempt else "")}])
                text = self._text(r)
                if schema is None:
                    return text
                try:
                    return self._parse(text, schema)
                except Exception as e:
                    last = e
            raise ValueError(f"Hakem 3 denemede geçerli JSON vermedi: {last}")

        def get_model_name(self):
            return model_name

    return ClaudeJudge()


def build_judges(model_name):
    from deepeval.metrics import GEval
    try:
        from deepeval.test_case import LLMTestCaseParams as P
    except ImportError:  # yeni DeepEval sürümlerinde ad değişmiş olabilir
        from deepeval.test_case import SingleTurnParams as P
    model = claude_judge(model_name) if model_name.startswith("claude") else model_name
    correctness = GEval(
        name="Dogruluk",
        evaluation_steps=[
            "Beklenen cevaptaki (expected output) kritik hukuki bilgileri listele: şartlar, süreler, tutarlar, istisnalar.",
            "Gerçek cevabın (actual output) bu bilgilerin her birini doğru verip vermediğini kontrol et.",
            "Beklenen cevapla çelişen tutar, süre veya kural varsa ağır cezalandır.",
            "Beklenen cevapta olmayan ama yanlış olmayan ek bilgiyi cezalandırma.",
            "Köşeli parantez içindeki atıf etiketlerini puanlamada yok say.",
            "Metinde yer almayan bir alt konu için kullanıcıyı yetkili kuruma veya bir belgeye yönlendirmek kapsam içi sorularda serbesttir, puan düşürmez (yalnızca kapsam dışı sorularda yasaktır).",
        ],
        evaluation_params=[P.INPUT, P.ACTUAL_OUTPUT, P.EXPECTED_OUTPUT],
        model=model, threshold=0.7,
    )
    oos = GEval(
        name="KapsamDisi",
        evaluation_steps=[
            # D10/D28: kapsam dışı soruda yalnızca "bilmiyorum / metinlerde yok" denmeli; başka hiçbir şey yok.
            "Soru, verilen trafik mevzuatı metinlerinin kapsamı dışındadır. Doğru davranış: yalnızca bu konunun metinlerde yer almadığını ve bilgi veremeyeceğini söylemek, başka hiçbir şey eklememek.",
            "Gerçek cevap sorunun metinlerde düzenlenmediğini açıkça belirtmiyorsa veya soruyu cevaplamaya çalışıyorsa 0 puan ver.",
            "Gerçek cevap rakam, ücret, telefon numarası, web sitesi veya başvuru kanalı uyduruyorsa 0 puan ver.",
            "Gerçek cevap kapsam dışı olduğunu söyleyip ayrıca madde atıfı, 'ilgili hükümler' listesi, ilgili konulara dair bilgi veya tavsiye/yönlendirme (ör. 'yetkili kuruma başvurun', 'ilgili mevzuata bakın') ekliyorsa en fazla 0.5 puan ver. Eklenen bilgi doğru olsa bile bu kural geçerlidir.",
            "Yalnızca kapsam dışı olduğunu söyleyen, atıf ve tavsiye içermeyen kısa bir cevaba 1 puan ver. Expected output içinde 'isteğe bağlı' olarak yazılan yönlendirmeler de beklenmez, puan almaz.",
        ],
        evaluation_params=[P.INPUT, P.ACTUAL_OUTPUT, P.EXPECTED_OUTPUT],
        model=model, threshold=0.7,
    )
    return correctness, oos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", default=str(pathlib.Path(__file__).resolve().parent / "trial_full_20.json"))
    ap.add_argument("--results", default="results.jsonl")
    ap.add_argument("--judge", default="claude-opus-5-5", help="claude-* veya deepeval'in desteklediği OpenAI model adı")
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--out", default="scores.csv")
    ap.add_argument("--only", default=None, help="virgülle ayrılmış soru ID'leri, ör. S01 (hakemi önce tek soruda denemek için)")
    a = ap.parse_args()

    Q = {q["id"]: q for q in json.load(open(a.questions, encoding="utf-8"))}
    R = [json.loads(l) for l in open(a.results, encoding="utf-8")]
    if a.only:
        keep = set(a.only.split(","))
        R = [r for r in R if r["id"] in keep]
    # Kimlik kontrolü: sonuç dosyasındaki her id soru dosyasında olmalı
    unknown = sorted({r["id"] for r in R} - set(Q))
    if unknown:
        raise SystemExit(f"Soru dosyasında olmayan id'ler: {', '.join(unknown)}")
    seen = {r["id"] for r in R}
    print(f"{len(R)} sonuç, {len(seen)} farklı soru. Soru dosyasında olup sonuçta olmayanlar: "
          f"{', '.join(sorted(set(Q) - seen)) or 'yok'}")
    if not a.no_judge and pathlib.Path(a.out).exists():
        raise SystemExit(f"{a.out} zaten var; elle girilen puanların üzerine yazmamak için başka bir --out ver (ör. scores_judge.csv)")
    judges = None if a.no_judge else build_judges(a.judge)

    rows = []
    for r in R:
        q = Q[r["id"]]
        arts, paras = norm_cits(r.get("citations") or [])
        g_arts = set(q["gold_articles"])
        g_paras = {f'{x["doc"]} {p}' for x in q["gold_refs"] for p in x["paras"]}
        row = {"run": r.get("run", 1), "id": r["id"], "scope": q["scope"],
               "type": q["tags"].get("Question Tag"),
               "hop_type": q["tags"].get("Hop Type"), "source_scope": q["tags"].get("Source Scope"),
               "parse_ok": r.get("parse_ok", True), "latency_s": r.get("latency_s"),
               "input_tokens": r.get("input_tokens"), "output_tokens": r.get("output_tokens"),
               "pred_citations": "; ".join(r.get("citations") or [])}
        if q["scope"] == "in":
            row["art_P"], row["art_R"], row["art_F1"] = prf(arts, g_arts)
            row["para_P"], row["para_R"], row["para_F1"] = prf_para(paras, g_paras)
            row["false_refusal"] = r.get("pred_in_scope") is False  # bayrak yoksa (None) ret sayılmaz
        else:
            row["refusal_ok"] = r.get("pred_in_scope") is False
            row["cited_anything"] = bool(r.get("citations"))
            # D28: katı ret = bayrak false VE hiç atıf yok (tavsiye kontrolü hakemde)
            row["refusal_strict"] = row["refusal_ok"] and not row["cited_anything"]
        if judges:
            from deepeval.test_case import LLMTestCase
            metric = judges[0] if q["scope"] == "in" else judges[1]
            tc = LLMTestCase(input=q["question"], actual_output=r["answer"], expected_output=q["gold_answer"])
            try:
                metric.measure(tc)
                row["judge_score"] = round(metric.score, 3)
                row["judge_reason"] = metric.reason
            except Exception as e:  # bir sorunun hatası tüm koşuyu durdurmasın
                print(f"UYARI: {r['id']} hakem hatası, atlandı: {str(e)[:150]}")
                row["judge_score"] = float("nan")
                row["judge_reason"] = f"JUDGE_ERROR: {str(e)[:300]}"
        # D35: elle puan yok. Hata nedeni otomatik: kapsam dışında bayrak ve atıf kontrolü,
        # kapsam içinde hakem puanı 0.7'nin altındaysa hakem gerekçesinden.
        if judges:
            row["judge_pass"] = bool(row["judge_score"] >= 0.7)  # NaN (hakem hatası) -> False
        causes = []
        if q["scope"] == "out":
            if not row["refusal_ok"]:
                causes.append("scope_flag_mismatch")
            if row["cited_anything"]:
                causes.append("oos_cited_related")
        elif judges and str(row.get("judge_reason", "")).startswith("JUDGE_ERROR"):
            causes.append("judge_error")
        elif judges and row["judge_score"] < 0.7:
            reason = (row.get("judge_reason") or "").lower()
            causes.append("missing_key_fact" if any(w in reason for w in ("omit", "missing", "eksik")) else "judge_below_threshold")
        row["failure_cause"] = "; ".join(causes)
        rows.append(row)
        print(row["run"], r["id"], row.get("judge_score"), row.get("art_F1", row.get("refusal_ok")))

    df = pd.DataFrame(rows)
    df.to_csv(a.out, index=False, encoding="utf-8-sig")

    print("\n=== ÖZET ===")
    ins, outs = df[df.scope == "in"], df[df.scope == "out"]
    num = [c for c in ["judge_score", "art_P", "art_R", "art_F1", "para_R"] if c in ins]
    if len(ins): print("In-scope ortalama:\n", ins[num].mean().round(3).to_string())
    if len(ins) and "judge_score" in ins and ins.run.nunique() > 1:
        print("In-scope run bazında std (judge):", round(float(ins.groupby("run")["judge_score"].mean().std()), 3))
    if len(ins): print("Yanlış ret oranı:", round(ins.false_refusal.mean(), 3))
    if len(outs):
        print("Out-of-scope doğru ret oranı (bayrak):", round(outs.refusal_ok.mean(), 3))
        print("Out-of-scope katı ret oranı (bayrak false ve atıf yok, D28):", round(outs.refusal_strict.mean(), 3))
    if "judge_score" in outs:
        print("Out-of-scope judge ort.:", round(outs.judge_score.mean(), 3))
    by_type = ins.groupby("type")[num].mean().round(3)
    by_hop = ins.groupby("hop_type")[num].mean().round(3)
    print("Soru tipi kırılımı:\n", by_type.to_string())
    print("Hop type kırılımı:\n", by_hop.to_string())
    if df.latency_s.notna().any():  # sohbet arayüzünden gelen sonuçlarda bu alanlar boş
        tok = (f"{int(df.input_tokens.mean())} / {int(df.output_tokens.mean())}"
               if df.input_tokens.notna().any() and df.output_tokens.notna().any() else "-")
        print("Ort. gecikme (s):", round(df.latency_s.mean(), 2), "| Ort. token in/out:", tok)

    # Deney kartı (E-card) için özet dosyası
    import importlib.metadata as md
    summary = {
        "results_file": a.results, "judge": None if a.no_judge else a.judge,
        "packages": {p: md.version(p) for p in ["deepeval", "pandas"] if not a.no_judge or p == "pandas"},
        "in_scope_mean": ins[num].mean().round(3).to_dict(),
        "in_scope_run_means_judge": ins.groupby("run")["judge_score"].mean().round(3).to_dict() if "judge_score" in ins else None,
        "false_refusal_rate": round(float(ins.false_refusal.mean()), 3) if len(ins) else None,
        "oos_refusal_rate": round(float(outs.refusal_ok.mean()), 3) if len(outs) else None,
        "oos_strict_refusal_rate": round(float(outs.refusal_strict.mean()), 3) if len(outs) else None,
        "oos_cited_anything_rate": round(float(outs.cited_anything.mean()), 3) if len(outs) else None,
        "oos_judge_mean": round(float(outs.judge_score.mean()), 3) if "judge_score" in outs else None,
        "by_type": by_type.to_dict(orient="index"), "by_hop_type": by_hop.to_dict(orient="index"),
        "latency_s_mean": round(float(df.latency_s.mean()), 2) if df.latency_s.notna().any() else None,
        "failure_causes": FAILURE_CAUSES,
    }
    out_json = a.out.rsplit(".", 1)[0] + "_summary.json"
    json.dump(summary, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Özet:", out_json)
    from collections import Counter
    print("Hata nedenleri:", dict(Counter(x for f in df.failure_cause for x in f.split("; ") if x)))


if __name__ == "__main__":
    main()
