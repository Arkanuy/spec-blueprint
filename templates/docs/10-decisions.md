# 10 — Decisions & Change Log

> Dokumen ini menjawab: **kenapa sesuatu diputuskan seperti ini, dan apa yang berubah sepanjang proyek.** Tanpa catatan ini, dalam dua minggu tidak ada yang ingat alasan sebuah pilihan — dan pilihan itu akan dibongkar ulang tanpa perlu.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## Format keputusan (ADR ringkas)

Setiap keputusan penting dicatat dengan format ini. "Penting" artinya: sulit dibalik, memengaruhi banyak bagian, atau pernah jadi perdebatan.

```
### ADR-001 — [Judul keputusan]
Tanggal    : [YYYY-MM-DD]
Status     : Diusulkan / Disetujui / Dibatalkan / Digantikan ADR-xxx
Konteks    : [situasi yang memaksa keputusan]
Keputusan  : [apa yang dipilih]
Alasan     : [kenapa ini yang dipilih]
Alternatif : [opsi lain yang dipertimbangkan + kenapa tidak dipilih]
Konsekuensi: [yang jadi lebih mudah + yang jadi lebih sulit]
```

---

## 1. Keputusan yang sudah diambil

### ADR-001 — [Judul keputusan]

- **Tanggal:** {{DATE}}
- **Status:** Diusulkan
- **Konteks:** [situasi]
- **Keputusan:** [pilihan]
- **Alasan:** [alasan]
- **Alternatif yang ditolak:** [opsi + kenapa ditolak]
- **Konsekuensi:** [positif dan negatif]

<!-- EXAMPLE-START -->
Contoh:

### ADR-002 — Tidak memakai microservices untuk rilis pertama

- **Tanggal:** 2026-01-10
- **Status:** Disetujui
- **Konteks:** Aplikasi dikerjakan satu orang, beban pengguna rendah, tenggat 4 minggu.
- **Keputusan:** Satu aplikasi monolit dengan backend dan frontend terpisah.
- **Alasan:** Menambah layanan berarti menambah kompleksitas deploy, pemantauan, dan debugging, tanpa manfaat nyata pada skala ini.
- **Alternatif yang ditolak:** Microservices — ditolak karena tidak ada masalah skalabilitas nyata dan tim hanya satu orang.
- **Konsekuensi:** Lebih cepat dibangun dan dirawat. Kalau nanti butuh skala, pemisahan dilakukan hanya pada bagian yang memang berat.

### ADR-003 — Tidak memakai pembayaran otomatis di rilis pertama

- **Tanggal:** 2026-01-12
- **Status:** Disetujui
- **Konteks:** Pengguna masih mengandalkan transfer manual dan verifikasi oleh staf.
- **Keputusan:** Pembayaran dicatat manual oleh staf dengan unggah bukti transfer.
- **Alasan:** Integrasi payment gateway menambah biaya, ketergantungan pihak ketiga, dan verifikasi webhook yang belum diperlukan.
- **Alternatif yang ditolak:** Payment gateway — ditunda sampai volume transaksi membenarkan biaya integrasinya.
- **Konsekuensi:** Pengguna harus menunggu verifikasi staf. Risiko: kepuasan pengguna di jam sibuk.
<!-- EXAMPLE-END -->

---

## 2. Log perubahan scope

Setiap kali ada fitur ditambah, dikurangi, atau diubah prioritasnya — catat di sini **beserta alasannya**. Ini yang mencegah scope meledak tanpa disadari.

| Tanggal | Perubahan | Jenis | Alasan | Dampak (waktu/kode/dokumen) | Diputuskan oleh | Dokumen yang diperbarui |
|---|---|---|---|---|---|---|
| [tanggal] | [fitur ditambah/dihapus/ditunda] | Tambah/Kurangi/Tunda | [alasan] | [dampak] | [nama] | PRD/requirements/... |

### 2.1 Pertanyaan wajib sebelum menyetujui penambahan scope

Jawab semuanya dengan "ya" sebelum menambah fitur di tengah jalan:

1. Fitur ini menyelesaikan masalah yang sudah tercatat di `00-discovery.md`?
2. Fitur ini lebih penting daripada sisa pekerjaan P0 yang belum selesai?
3. Requirement-nya sudah punya ID di `02-requirements.md`?
4. Ada yang mau mengerjakan dan menguji?
5. Kalau tidak dibuat, apa yang hilang secara nyata?

Kalau ada jawaban "tidak", masukkan ke **ide tunda** di `01-prd.md` — jangan dikerjakan sekarang.

---

## 3. Log perubahan dokumen

| Tanggal | Dokumen | Bagian | Perubahan | Alasan |
|---|---|---|---|---|
| {{DATE}} | semua | – | Dokumen awal dibuat | Awal proyek |

---

## 4. Keputusan yang menunggu

| # | Keputusan yang dibutuhkan | Menghambat apa | Pilihan yang tersedia | Tenggat | Siapa yang memutuskan |
|---|---|---|---|---|---|
| 1 | [keputusan] | [pekerjaan] | [opsi] | [tanggal] | [nama] |

---

## 5. Keputusan yang dibatalkan / digantikan

| ADR | Keputusan lama | Digantikan oleh | Tanggal | Alasan |
|---|---|---|---|---|

---

## 6. Catatan pelajaran (retrospective)

Diisi menjelang akhir fase atau setelah masalah besar. Berguna agar tidak mengulang kesalahan yang sama di proyek berikutnya.

| Tanggal | Apa yang terjadi | Akar penyebab | Yang akan dilakukan berbeda |
|---|---|---|---|

---

## 7. Riwayat perubahan dokumen ini

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
