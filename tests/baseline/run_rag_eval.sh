#!/bin/bash
# Bir RAG sonuç dosyasını hakemle puanlar ve LLM baseline'ı (E3) ile karşılaştırır.
# Baseline yeniden çalıştırılmaz: E3'ün puanları llm/run1/scores.csv dosyasından okunur.
#
# Kullanım (tests/baseline klasöründe, .venv açık, ANTHROPIC_API_KEY tanımlı):
#   bash run_rag_eval.sh <rag_sonuç_dosyası.jsonl>             -> hakemle puanla + karşılaştır
#   bash run_rag_eval.sh <rag_sonuç_dosyası.jsonl> --no-judge  -> sadece ücretsiz madde metrikleri
# Çıktılar rag/ klasörüne yazılır. Var olan rag/scores_rag.csv üzerine yazılmaz.
set -e
cd "$(dirname "$0")"
RAG="$1"
JUDGE=claude-opus-5-5
[ -n "$RAG" ] && [ -f "$RAG" ] || { echo "Kullanım: bash run_rag_eval.sh <rag_sonuç_dosyası.jsonl> [--no-judge]"; exit 1; }

if [ "$2" = "--no-judge" ]; then
  python eval.py --results "$RAG" --no-judge --out /tmp/scores_rag_nojudge.csv
  exit 0
fi
[ -n "$ANTHROPIC_API_KEY" ] || { echo "ANTHROPIC_API_KEY tanımlı değil"; exit 1; }
mkdir -p rag
if [ -f rag/scores_rag.csv ]; then
  echo "rag/scores_rag.csv zaten var; yeni bir RAG koşusu için önce bu dosyayı başka bir ada taşı"; exit 1
fi
echo "== 1/2 RAG cevapları hakemle puanlanıyor"
python eval.py --results "$RAG" --judge "$JUDGE" --out rag/scores_rag.csv
echo "== 2/2 LLM baseline (E3) ile karşılaştırma"
python compare.py
