# Dokumen Proyek — {{PROJECT_NAME}}

Indeks dokumen spec-first untuk proyek ini. Semua dokumen di folder ini adalah sumber kebenaran tunggal (single source of truth). Kalau kode dan dokumen bertentangan, dokumen yang menang — atau dokumen diperbarui dulu, baru kode.

**Proyek:** {{PROJECT_NAME}}
**Jenis:** {{PROJECT_TYPE}}
**Domain:** {{DOMAIN}}
**Stack:** {{STACK}}
**Pemilik produk:** {{OWNER}}
**Tanggal mulai spec:** {{DATE}}

---

## Urutan pengisian (jangan dilompati)

| # | Dokumen | Menjawab pertanyaan | Selesai kalau... |
|---|---|---|---|
| 0 | [00-discovery.md](00-discovery.md) | Apa masalah nyatanya, dan apakah layak dibuat sistem? | Ada 1 masalah utama + akar masalah yang disetujui pemilik produk |
| 1 | [01-prd.md](01-prd.md) | Apa yang dibangun, untuk siapa, sampai mana batasnya | Ada daftar fitur P0 dengan tujuan dan metrik keberhasilan |
| 2 | [02-requirements.md](02-requirements.md) | Syarat detail yang bisa diuji | Setiap fitur P0 punya FR + acceptance criteria ber-ID |
| 3 | [03-architecture.md](03-architecture.md) | Bagaimana sistem disusun | Ada batas sistem, daftar komponen, dan alur integrasi |
| 4 | [04-workflow.md](04-workflow.md) | Bagaimana proses berjalan | Ada AS-IS, TO-BE, dan alur user per peran |
| 5 | [05-data-model.md](05-data-model.md) | Data apa yang disimpan | Ada entitas, relasi, status, aturan validasi |
| 6 | [06-ui-ux.md](06-ui-ux.md) | Bagaimana pengguna melihat & memakai | Ada daftar layar dengan semua state |
| 7 | [07-test-plan.md](07-test-plan.md) | Bagaimana dibuktikan benar | Setiap FR P0 punya minimal 1 kasus uji |
| 8 | [08-roadmap.md](08-roadmap.md) | Dikerjakan berurutan bagaimana | Ada fase 1/2/3 dengan deliverable jelas |
| 9 | [09-risks.md](09-risks.md) | Apa yang bisa gagal | Ada risiko, asumsi, dan pertanyaan terbuka bernomor |
| 10 | [10-decisions.md](10-decisions.md) | Kenapa keputusan diambil | Setiap keputusan besar ada tanggal + alasan + alternatif |

---

## Aturan penulisan dokumen ini

1. **Satu dokumen, satu audiens.** PRD dibaca pemilik produk, architecture dibaca developer, test plan dibaca penguji.
2. **Setiap klaim harus punya sumber.** Tulis `(Fakta)`, `(Asumsi)`, atau `(Perlu dikonfirmasi)` di belakang klaim yang tidak jelas asalnya.
3. **Setiap fitur harus bisa dilacak** ke masalah di `00-discovery.md`.
4. **Setiap requirement punya ID unik.** Format: `FR-001`, `NFR-001`, `BR-001`, `US-001`, `TC-001`.
5. **Angka yang belum ada datanya jangan dikarang.** Tulis `[butuh data]` lalu catat di `09-risks.md`.

---

## Cara memakai bersama AI

```
Konteks untuk AI  =  docs/01-prd.md  +  docs/02-requirements.md
                  +  docs/03-architecture.md  +  docs/05-data-model.md
                  +  docs/06-ui-ux.md  +  AGENTS.md
```

Aturan keras: **AI tidak boleh menulis fitur yang belum punya ID requirement.** Kalau AI menawarkan fitur tambahan, fitur itu masuk ke `01-prd.md` bagian "Di luar scope / ide tunda" dulu — bukan langsung ke kode.

Semua prompt siap pakai ada di folder [`prompts/`](../prompts/).

---

## Cara memeriksa dokumen sudah cukup matang

Jalankan [gate-1-sebelum-coding.md](../checklists/gate-1-sebelum-coding.md). Kalau ada item yang belum tercentang, jangan mulai coding — tanyakan ke pemilik produk dulu.
