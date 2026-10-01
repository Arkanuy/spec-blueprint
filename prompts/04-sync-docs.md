# Prompt 04 — Menyelaraskan Dokumen dengan Kode

> Dipakai di akhir fase, setelah beberapa fitur selesai. Tanpa langkah ini, dokumen akan perlahan berbeda dari kenyataan — dan dokumen yang salah lebih berbahaya daripada tidak ada dokumen, karena orang mempercayainya.

---

## Kapan dijalankan

- Setelah satu fase selesai (misal: semua P0 tuntas)
- Sebelum rilis
- Setelah bug besar diperbaiki
- Setiap kali kamu merasa "dokumennya sudah tidak sesuai lagi"

---

## Prompt

```
Kamu bertindak sebagai analis dokumen. Tugasmu: bandingkan dokumen spec dengan kode nyata
di repo ini, lalu laporkan setiap ketidaksesuaian.

DOKUMEN YANG DIPERIKSA
- docs/02-requirements.md
- docs/03-architecture.md
- docs/04-workflow.md
- docs/05-data-model.md
- docs/06-ui-ux.md
- docs/07-test-plan.md
- docs/08-roadmap.md

KODE YANG MENJADI KENYATAAN
- Baca struktur kode nyata: [sebutkan folder/file utama]

ATURAN
1. JANGAN mengubah kode apa pun. Tugasmu hanya membandingkan dan melaporkan.
2. Untuk setiap ketidaksesuaian, tentukan mana yang benar:
   - Kalau kode benar dan dokumen ketinggalan → dokumen harus diperbarui
   - Kalau dokumen benar dan kode menyimpang → ini BUG, harus diperbaiki di kode
   - Kalau keduanya meragukan → tandai sebagai "perlu keputusan pemilik produk"
   Jangan memutuskan sendiri hal yang mengubah perilaku produk.
3. Jangan menambah requirement baru. Kalau kamu menemukan fitur yang ada di kode tapi tidak
   ada di dokumen, laporkan sebagai "tidak terdaftar" — jangan otomatis dibuatkan requirement.

CARA MEMERIKSA (per dokumen)

A. docs/02-requirements.md
   - Setiap FR: apakah ada kode yang mengimplementasikannya? (cari dan sebutkan lokasinya)
   - Ada FR yang tidak ditemukan implementasinya? (ini kegagalan, bukan kelalaian dokumen)
   - Ada perilaku di kode yang tidak punya FR? (fitur tidak terdaftar)

B. docs/03-architecture.md
   - Apakah daftar komponen masih sesuai kenyataan?
   - Apakah ada dependensi/paket baru yang tidak tercatat?
   - Apakah endpoint yang ada masih sama dengan yang didokumentasikan?
   - Apakah struktur folder masih sesuai?

C. docs/04-workflow.md
   - Apakah alur status (state flow) yang ada di kode masih sama dengan yang didokumentasikan?
   - Apakah ada alur alternatif/pengecualian yang ditangani di kode tapi tidak ada di dokumen?

D. docs/05-data-model.md
   - Apakah setiap entitas dan field di dokumen benar-benar ada di database?
   - Apakah ada field/entitas di database yang tidak ada di dokumen?
   - Apakah aturan integritas yang tertulis benar-benar ditegakkan?

E. docs/06-ui-ux.md
   - Apakah setiap layar yang ada di kode sudah terdaftar?
   - Apakah status kosong/memuat/error benar-benar ada di kode?
   - Apakah ada layar yang didokumentasikan tapi tidak ada di kode?

F. docs/07-test-plan.md
   - Apakah setiap FR P0 punya TC?
   - Kasus uji mana yang belum pernah dijalankan (tidak ada bukti)?

FORMAT LAPORAN

RINGKASAN
- FR terdokumentasi : [n]
- FR ditemukan di kode : [n]
- Selisih : [n]

KETIDAKSESUAIAN
| # | Dokumen | Isi dokumen | Kenyataan di kode | Siapa yang benar | Tindakan |
|---|---|---|---|---|---|

FITUR TIDAK TERDAFTAR (ada di kode, tidak ada di dokumen)
| # | Perilaku | Lokasi kode | Perlu requirement baru? | Catatan |
|---|---|---|---|---|

REQUIREMENT BELUM TERIMPLEMENTASI
| # | FR | Status | Perlu diperbaiki atau dihapus dari scope? |
|---|---|---|---|

PERLU KEPUTUSAN PEMILIK PRODUK
| # | Hal | Pilihan | Dampak masing-masing |
|---|---|---|---|

TINDAKAN YANG SAYA USULKAN (urutan prioritas)
1. [dokumen mana diperbarui, bagian mana]
2. [kode mana diperbaiki, kenapa]
3. [requirement yang perlu dibuat/dihapus]

Kalau semuanya sudah selaras, katakan jelas "semua dokumen sudah sesuai" — jangan mengarang
temuan agar laporan terlihat berisi.
```

---

## Setelah menjalankan prompt ini

Lakukan tiga hal ini secara berurutan:

1. **Perbarui dokumen yang ketinggalan.** Jangan menunda — kalau ditunda, akan lupa.
2. **Buat requirement untuk fitur tidak terdaftar** yang memang mau dipertahankan. Fitur yang tidak mau dipertahankan: hapus kodenya, atau tandai sebagai kode mati untuk dibersihkan.
3. **Catat perubahan scope** di `docs/10-decisions.md`. Termasuk yang tidak direncanakan.

---

## Pemeriksaan akhir sebelum menyatakan selaras

- [ ] Setiap FR punya implementasi di kode
- [ ] Setiap entitas di dokumen ada di database, dan sebaliknya
- [ ] Setiap layar di dokumen ada di kode, dan sebaliknya
- [ ] Setiap layar sudah menangani status kosong, memuat, dan error
- [ ] Setiap FR P0 punya kasus uji dengan bukti
- [ ] Dokumen `10-decisions.md` mencatat semua perubahan scope
- [ ] Tidak ada dokumen yang masih berisi placeholder `[isi]` atau `{{...}}`
