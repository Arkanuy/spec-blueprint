# 04 — Workflow & Proses Bisnis

> Dokumen ini menjawab: **bagaimana pekerjaan berjalan sekarang, bagaimana seharusnya berjalan, dan bagaimana pengguna bergerak di dalam sistem.** Bagian AS-IS menjelaskan kondisi nyata; bagian TO-BE menjelaskan rencana. Jangan mencampur keduanya.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## 1. Daftar proses utama

| # | Proses | Pemicu | Pelaku utama | Frekuensi | Dampak kalau gagal | Prioritas |
|---|---|---|---|---|---|---|
| PS-01 | [nama proses] | [apa yang memulai] | [peran] | [harian/mingguan] | [dampak] | P0 |

---

## 2. Proses AS-IS (kondisi sekarang)

> Aturan: tulis apa adanya. Jangan memasukkan fitur sistem yang belum ada. Kalau sekarang pakai WhatsApp, tulis WhatsApp.

### PS-01 — [Nama proses]

| Langkah | Pelaku | Aktivitas | Masukan | Keluaran | Alat | Waktu | Masalah |
|---|---|---|---|---|---|---|---|
| 1 | [peran] | [aktivitas] | [data] | [hasil] | [manual/kertas/Excel] | [estimasi] | [kendala] |

**Titik masalah pada proses ini:**

| # | Masalah | Jenis | Dampak |
|---|---|---|---|
| 1 | [masalah] | [penundaan / input ganda / verifikasi berulang / informasi tersebar / handoff tidak jelas / tidak ada kontrol] | [dampak] |

Jenis masalah yang biasa ditemukan: pekerjaan manual berulang, data dimasukkan dua kali, verifikasi berulang, serah terima antar orang yang tidak jelas, informasi tersebar, keterlambatan, kesalahan input, data tidak konsisten, sulit dipantau, tidak ada jejak audit, tindak lanjut terlewat.

---

## 3. Proses TO-BE (kondisi yang diusulkan)

### PS-01 — [Nama proses] (setelah perbaikan)

| Langkah | Pelaku | Aktivitas | Masukan | Keluaran | Sistem/alat | Perubahan dari AS-IS | FR terkait |
|---|---|---|---|---|---|---|---|
| 1 | [peran] | [aktivitas] | [data] | [hasil] | [{{PROJECT_NAME}}] | [apa yang berbeda] | FR-00x |

**Perbaikan yang dicapai:**

| Masalah AS-IS | Diselesaikan oleh | Bagaimana |
|---|---|---|
| [masalah #1] | [fitur/FR] | [mekanisme] |

Aturan verifikasi: **setiap masalah di AS-IS harus punya penyelesaian di TO-BE.** Kalau ada masalah tanpa penyelesaian, tulis eksplisit "tidak diselesaikan sekarang — alasan: ..." — jangan dihapus diam-diam.

---

## 4. Diagram alur proses

Gambarkan proses utama. Bisa pakai BPMN, activity diagram, atau flowchart sederhana. Yang penting: setiap aktivitas bisa dipetakan ke aktor, masukan, dan keluaran.

```
Contoh alur sederhana:

[Mulai] ─▶ [Aktor: aktivitas] ─▶ <Keputusan?>
                                    │        │
                                  Ya         Tidak
                                    ▼          ▼
                            [Aksi A]      [Aksi B]
                                    │          │
                                    └────┬─────┘
                                         ▼
                                      [Selesai]
```

### 4.1 Aturan pembuatan diagram

- Nama aktivitas pakai **kata kerja + objek** (contoh: "Periksa stok", bukan "Stok").
- Setiap cabang keputusan harus punya kondisi yang tertulis di garis.
- Jangan menggambar komponen teknis (database, API) sebagai aktor manusia.
- Kalau ada proses paralel, tandai jelas mana yang bisa berjalan bersamaan.

---

## 5. Alur pengguna di sistem (user flow)

Alur ini menjelaskan langkah di dalam aplikasi, berbeda dari proses bisnis di atas.

### UF-01 — [Nama alur] — [persona]

| Langkah | Aksi pengguna | Respons sistem | Layar/URL | Kondisi |
|---|---|---|---|---|
| 1 | [aksi] | [respons] | [halaman] | [syarat] |

**Kondisi awal:** [apa yang harus benar sebelum alur dimulai]
**Kondisi akhir:** [apa yang berubah setelah alur selesai]
**Alur alternatif:** [variasi yang sah]
**Alur error:** [kondisi gagal + apa yang ditampilkan]

---

## 6. Alur status (state flow)

Untuk setiap entitas yang punya siklus hidup (pesanan, pengajuan, pembayaran, tiket).

### Entitas: [nama entitas]

| Dari | Ke | Pemicu | Syarat | Peran yang boleh | Efek samping |
|---|---|---|---|---|---|
| [status] | [status] | [aksi/event] | [syarat] | [peran] | [notifikasi/update data lain] |

```
[Draft] ──submit──▶ [Menunggu] ──setuju──▶ [Disetujui]
                        │
                     tolak
                        ▼
                    [Ditolak]
```

Aturan: setiap status harus punya jalur masuk dan jalur keluar. Status yang tidak punya jalur keluar biasanya tanda desain proses belum matang.

---

## 7. Alur data (dari sisi proses)

| Langkah proses | Data dibuat | Data diubah | Data dibaca | Data dihapus/diarsipkan |
|---|---|---|---|---|
| [langkah] | [entitas.field] | [entitas.field] | [entitas.field] | [entitas] |

Berguna untuk memastikan: setiap data yang dibuat benar-benar dipakai, dan setiap data yang dibaca benar-benar pernah dibuat.

---

## 8. Aturan dan pengecualian

### 8.1 Aturan yang mengikat proses

| # | Aturan | Berlaku untuk | Kalau dilanggar |
|---|---|---|---|
| 1 | [BR-00x] | [proses/langkah] | [penanganan] |

### 8.2 Pengecualian (exception)

Kondisi tidak normal yang harus tetap punya jalur penyelesaian. Bukan "di luar tanggung jawab".

| # | Kondisi tidak normal | Bagaimana ditangani | Siapa yang menangani | FR terkait |
|---|---|---|---|---|
| EX-01 | [contoh: pelanggan membatalkan setelah bayar] | [prosedur] | [peran] | FR-00x |

Contoh pengecualian yang sering terlupakan: data tidak lengkap, pengguna tidak punya hak akses, koneksi terputus saat menyimpan, data ganda, pembatalan di tengah proses, tenggat terlewat, pihak ketiga tidak merespons, perangkat/print gagal.

---

## 9. Perbandingan AS-IS vs TO-BE

| Aspek | AS-IS | TO-BE | Perbaikan |
|---|---|---|---|
| Jumlah langkah | [n] | [n] | [berkurang/bertambah + alasan] |
| Waktu proses | [estimasi] | [target] | [selisih] |
| Input ganda | [ada/tidak] | [ada/tidak] | [perbaikan] |
| Titik verifikasi | [n] | [n] | [perbaikan] |
| Ketersediaan informasi | [kondisi] | [kondisi] | [perbaikan] |
| Jejak audit | [ada/tidak] | [ada/tidak] | [perbaikan] |

Catatan: TO-BE yang **menambah** langkah bukan otomatis buruk — kadang menambah kontrol memang perlu. Tapi harus dijelaskan alasannya.

---

## 10. Perubahan pada manusia & organisasi

Perubahan sistem mengubah cara kerja orang. Bagian ini mencegah sistem bagus tapi tidak dipakai.

| Peran | Yang berubah | Pelatihan/kebiasaan baru yang dibutuhkan | Risiko penolakan | Cara mengatasinya |
|---|---|---|---|---|
| [peran] | [perubahan tugas] | [yang harus dipelajari] | [rendah/sedang/tinggi] | [langkah] |

---

## 11. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
