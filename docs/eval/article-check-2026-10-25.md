# Article check against the official source

Run on 2026-10-25 with `python src/check_articles.py --seed 502 --n 20` on commit 021f15f (texts in `data/legal/`). Stored text = `data/legal/*.txt`; official = the mevzuat.gov.tr PDFs in `data/legal/pdf/`, extracted with `pdftotext -layout`. Comparison after normalising whitespace, page breaks, line-end hyphenation and footnote markers; any other character difference counts as "differs". Detection verified with a deliberate one-word change (reported as "differs").

Article check — seed 502, 20 articles, 20/20 identical

| # | Text | Article | Chars | Result | First difference (stored \| official) |
|---|---|---|---|---|---|
| 1 | Karayolları Trafik Kanunu (2918) | Madde 11 | 112 | identical |  |
| 2 | Karayolları Trafik Kanunu (2918) | Madde 44 | 431 | identical |  |
| 3 | Karayolları Trafik Kanunu (2918) | Madde 91 | 1801 | identical |  |
| 4 | Karayolları Trafik Kanunu (2918) | Madde 94 | 756 | identical |  |
| 5 | Karayolları Trafik Kanunu (2918) | Madde 110 | 668 | identical |  |
| 6 | Karayolları Trafik Kanunu (2918) | Madde 130 | 347 | identical |  |
| 7 | Karayolları Trafik Yönetmeliği | Madde 20 | 608 | identical |  |
| 8 | Karayolları Trafik Yönetmeliği | Madde 51 | 297 | identical |  |
| 9 | Karayolları Trafik Yönetmeliği | Madde 64 | 772 | identical |  |
| 10 | Karayolları Trafik Yönetmeliği | Madde 82 | 1646 | identical |  |
| 11 | Karayolları Trafik Yönetmeliği | Madde 98 | 5261 | identical |  |
| 12 | Karayolları Trafik Yönetmeliği | Madde 130 | 1261 | identical |  |
| 13 | Karayolları Trafik Yönetmeliği | Madde 167 | 2552 | identical |  |
| 14 | Karayolları Trafik Yönetmeliği | Madde 168 | 1627 | identical |  |
| 15 | MEB Özel Motorlu Taşıt Sürücüleri Kursu Yönetmeliği | Madde 7 | 4914 | identical |  |
| 16 | MEB Özel Motorlu Taşıt Sürücüleri Kursu Yönetmeliği | Madde 50 | 166 | identical |  |
| 17 | Sürücü Adayları ve Sürücülerde Aranacak Sağlık Şartları Yönetmeliği | Madde 11 | 299 | identical |  |
| 18 | Araç Muayene Yönetmeliği | Madde 11 | 2001 | identical |  |
| 19 | Elektrikli Skuter Yönetmeliği | Madde 23 | 351 | identical |  |
| 20 | Elektrikli Skuter Yönetmeliği | Madde 25 | 506 | identical |  |

Articles per text: Karayolları Trafik Kanunu 138, Karayolları Trafik Yönetmeliği 180, MEB Özel Motorlu Taşıt Sürücüleri Kursu Yönetmeliği 51, Sürücü Adayları ve Sürücülerde Aranacak Sağlık Şartları Yönetmeliği 14, Araç Muayene Yönetmeliği 29, Elektrikli Skuter Yönetmeliği 30
