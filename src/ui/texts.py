"""Chunky arayüzü — tüm Türkçe metinler tek yerde (CHUNKY-166: dil ve ton kontrolü).

Kural: app.py'de tırnak içinde Türkçe cümle olmaz; her metin buradan T["anahtar"] ile gelir.
Yer tutucular Python format alanıdır: T["x"].format(n=3). Markdown serbesttir.
"""

T = {
    # --- sayfa / başlık
    "page_title": "Chunky · Trafik Mevzuatı Asistanı",
    "title": "🚦 Chunky — Trafik Mevzuatı Asistanı",
    "subtitle": "Karayolları Trafik Kanunu ve ilgili beş yönetmelik hakkında sorular. "
                "Cevaplar yalnızca bu metinlere dayanır; hukuki tavsiye değildir.",
    "ai_disclaimer": "Chunky bir yapay zekâ asistanıdır ve hata yapabilir.",
    "heading_icon": "🚦",
    "ask_heading": "Trafik mevzuatı hakkında bir soru sorun",
    "ai_notice": "Chunky bir yapay zekâ asistanıdır ve hata yapabilir. Cevapları mevzuatın güncel metninden doğrulayın; para cezası tutarları her yıl yeniden değerleme oranında güncellenir.",
    "input_placeholder": "Örn. Seyir halinde cep telefonu kullanmanın cezası nedir?",
    "input_too_long": "Soru çok uzun ({n} karakter). En fazla {max} karakter yazabilirsiniz.",

    # --- örnek sorular (butonlar)
    "examples": [
        "Kırmızı ışıkta geçmenin cezası ne kadar?",
        "Araçların ilk muayenesi ne zaman yapılır?",
        "Elektrikli skuter hangi yollarda kullanılamaz?",
        "Alkollü araç kullanmanın cezası nedir?",
    ],

    # --- kenar çubuğu
    "sidebar_title": "🚦 Chunky",
    "sidebar_caption": "Trafik kuralları ve cezaları asistanı — RAG prototipi",
    "mode_api": "Bağlantı: **retriever servisi** ({url})",
    "mode_local": "Bağlantı: **yerel pipeline** (arama bu bilgisayarda, cevap Google Cloud'daki modelde)",
    "settings_local": "Ayarlar `config/rag.yaml` dosyasından okunur:  \nCevap modeli `{model}`  \nPrompt `{prompt}` · top_k={k} · hybrid ağırlığı {sw}",
    "health_ok": "Servis hazır · korpus {corpus}",
    "health_fail": "Servise ulaşılamadı: {err}",
    "settings_header": "Ayarlar",
    "advanced_expander": "Gelişmiş ayarlar",
    "opt_model": "Cevap modeli",
    "opt_prompt": "Sistem komutu (prompt)",
    "opt_rerank": "Yeniden sıralama (reranker)",
    "opt_k": "Aday parça sayısı (k)",
    "opt_top": "Modele verilen parça sayısı",
    "opt_show_text": "Parça metinlerini göster",
    "new_chat": "Yeni Sohbet",
    "avatar_user": "🧑",
    "avatar_assistant": "🚦",
    "corpus_line": "**Korpus:** {n_chunks} parça · 6 belge",
    "models_line": "**Embedding:** `{embedding}`  \n**Reranker:** `{reranker}`",
    "models_line_local": "**Embedding:** `{embedding}`",
    "disclaimer": "Cevaplar yalnızca yüklü mevzuat metinlerine dayanır; hukuki tavsiye değildir. "
                  "Para cezası tutarları her yıl yeniden değerleme oranında güncellenir.",

    # --- cevap akışı
    "spinner_retrieving": "Mevzuat aranıyor…",
    "spinner_loading": "Arama modeli yükleniyor… (ilk açılışta bir dakika kadar sürebilir)",
    "spinner_answering": "Mevzuat aranıyor ve cevap hazırlanıyor…",
    "spinner_waiting_api": "Cevap hazırlanıyor… (bu işlem birkaç dakika sürebilir)",
    "writing": "_cevap yazılıyor…_",
    "cursor": " ▌",
    "empty_answer": "Cevap boş geldi. Lütfen soruyu yeniden sorun; sorun sürerse soru numarasını bildirin.",
    "interpreted_as": "Soru şu şekilde yorumlandı: _{q}_",

    # --- ret sebepleri (refusal_reason → kullanıcıya gösterilen açıklama)
    "refusal": {
        "out_of_scope": "Bu soru trafik mevzuatının kapsamı dışında görünüyor. Asistan yalnızca Karayolları Trafik Kanunu ve ilgili yönetmelikler hakkında cevap verir.",
        "injection": "Bu girdi bir soru olarak işlenemedi.",
        "empty_or_invalid": "Lütfen trafik mevzuatıyla ilgili bir soru yazın.",
        "not_in_corpus": "Elimdeki mevzuat metinlerinde bu sorunun cevabı yok.",
        "default": "Bu soruya cevap verilemedi.",
    },

    # --- kaynaklar
    "sources_label": "Kullanılan parçalar · toplam {total:.1f} sn",
    "sources_label_detail": " (arama {retr:.1f} sn, ilk kelime {ttft:.1f} sn)",
    "sources_label_detail_no_ttft": " (arama {retr:.1f} sn)",
    "source_line": "**{header}** — puan {score:.3f}",
    "source_line_noscore": "**{header}**",
    "source_version": " · sürüm {date}",
    "source_pages": " · s. {pages}",
    "unknown_citations": "Dikkat: cevap, aranan maddeler arasında olmayan şu atıfları içeriyor: {ids}. Bu atıfları kaynak olarak kabul etmeyin.",
    "request_line": "istek {request_id}",
    "tokens_line": "Token: soru+bağlam {prompt} · cevap {completion}",
    "config_line": "Model `{model}` · prompt `{prompt}` · k={k} · top={top} · reranker {rerank} · istek {request_id}",
    "config_line_local": "Model `{model}` · prompt `{prompt}` · top_k={k} · hybrid ağırlığı {sw} · istek {request_id}",
    "rerank_on": "açık",
    "rerank_off": "kapalı",

    # --- hatalar
    "err_bad_request": "Soru gönderilemedi (geçersiz istek). Lütfen soruyu kontrol edip tekrar deneyin.",
    "err_model_unavailable": "Cevap modeli şu anda kullanılamıyor. Lütfen biraz sonra tekrar deneyin.",
    "err_auth": "Google Cloud girişi bulunamadı. Terminalde `gcloud auth application-default login` komutunu çalıştırıp sayfayı yenileyin.",
    "err_permission": "Google Cloud'daki cevap modeline erişim izni yok (kod {code}). Hesabınızın `{project}` projesine erişimi olduğundan emin olun.",
    "err_index_missing": "Arama dizini bulunamadı. Proje klasöründe `python -m chunky.index` komutunu çalıştırıp sayfayı yenileyin.",
    "err_timeout": "Cevap süresi aşıldı. Lütfen soruyu kısaltıp tekrar deneyin.",
    "err_connection": "Servise bağlanılamadı ({url}). Servisin çalıştığından emin olun.",
    "err_generic": "Beklenmeyen bir hata oluştu (kod {code}). Lütfen tekrar deneyin.",
    "err_local": "Yerel pipeline hatası: {err}",
}

# Belge kısaltmaları → tam ad (kaynak satırlarında ve raporlarda)
DOC_NAMES = {  # kısaltmalar data/chunks/chunks.jsonl içindeki doc_code alanıyla aynı
    "KTK": "Karayolları Trafik Kanunu (2918 sayılı)",
    "KTY": "Karayolları Trafik Yönetmeliği",
    "KURS": "MEB Özel Motorlu Taşıt Sürücüleri Kursu Yönetmeliği",
    "SAĞLIK": "Sürücü Adayları ve Sürücülerde Aranacak Sağlık Şartları Yönetmeliği",
    "MUAYENE": "Araç Muayene Yönetmeliği",
    "SKUTER": "Elektrikli Skuter Yönetmeliği",
}
