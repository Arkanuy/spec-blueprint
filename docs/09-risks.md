# 09 — Risks, Asumsi & Pertanyaan Terbuka

> Dokumen ini menjawab: **apa yang bisa menggagalkan proyek, apa yang masih kita anggap benar tanpa bukti, dan apa yang belum kita ketahui.** Menuliskan asumsi di sini lebih murah daripada menemukannya salah setelah kode jadi.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## 1. Risiko

Bedakan dengan jelas:

- **Risiko** — sesuatu yang *mungkin* terjadi dan berdampak buruk
- **Masalah** — sesuatu yang *sudah* terjadi
- **Batasan** — sesuatu yang pasti dan tidak bisa diubah

| ID | Risiko | Kategori | Kemungkinan | Dampak | Skor | Cara mengurangi | Penanggung jawab | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | [risiko] | [teknis/operasional/organisasi/jadwal/data/keamanan] | Rendah/Sedang/Tinggi | Rendah/Sedang/Tinggi | [K×D] | [langkah nyata] | [nama] | Terbuka/Dipantau/Tertutup |

Skor = Kemungkinan × Dampak (Rendah=1, Sedang=2, Tinggi=3). Skor ≥6 wajib punya rencana penanganan sebelum coding dimulai.

### 1.1 Risiko yang paling sering muncul di proyek seperti ini

| Risiko | Tanda-tandanya | Pencegahan |
|---|---|---|
| Requirement berubah di tengah jalan | Fitur bertambah sebelum P0 selesai | Perubahan hanya lewat `10-decisions.md` |
| Pengguna menolak memakai sistem | "Nanti saja, sekarang jalan seperti biasa" | Libatkan pengguna saat uji, mulai dari 1 alur nyata |
| Kualitas data lama buruk | Data lama tidak lengkap/berformat beda | Periksa dan bersihkan sebelum migrasi |
| Scope meledak | "Sekalian tambahkan..." | Semua usulan baru masuk "ide tunda", bukan dikerjakan |
| Ketergantungan pihak ketiga | Layanan eksternal sering gagal | Rancang jalur cadangan |
| Kode hasil AI tidak bisa dirawat | Tidak ada yang paham kodenya | Wajib ada dokumen + uji otomatis |
| Data hilang | Tidak ada backup yang pernah diuji | Uji pemulihan, bukan sekadar menyimpan backup |

---

## 2. Asumsi

| ID | Asumsi | Kenapa dianggap benar | Kalau salah, apa yang berubah | Cara memverifikasi | Status |
|---|---|---|---|---|---|
| A-01 | [asumsi] | [alasan] | [dampak ke desain] | [cara] | Terbuka/Terverifikasi/Dibantah |

Aturan: asumsi yang **berdampak besar** dan **belum diverifikasi** harus diperiksa sebelum fase berikutnya. Kalau tidak bisa diverifikasi, rancang sistem agar mudah diubah.

---

## 3. Pertanyaan terbuka

| ID | Pertanyaan | Menghambat apa | Siapa yang bisa menjawab | Tenggat | Status |
|---|---|---|---|---|---|
| Q-01 | [pertanyaan] | [bagian yang terhenti] | [nama] | [tanggal] | Terbuka/Tertutup |

Aturan: pertanyaan yang menghambat pekerjaan P0 **harus** dijawab sebelum coding bagian itu dimulai. Jangan biarkan AI mengisi kekosongan ini dengan tebakan.

---

## 4. Ketergantungan

| ID | Bergantung pada | Untuk apa | Kalau tidak tersedia | Rencana cadangan |
|---|---|---|---|---|
| D-01 | [orang/layanan/data] | [fungsi] | [dampak] | [alternatif] |

---

## 5. Catatan yang dianggap sudah beres

Hal yang pernah jadi kekhawatiran tapi sudah diselesaikan. Berguna sebagai jejak.

| # | Kekhawatiran | Cara diselesaikan | Tanggal |
|---|---|---|---|

---

## 6. Pemantauan risiko

Risiko yang berubah wajib diperbarui, bukan dibiarkan menua.

| Tanggal | ID | Perubahan | Alasan |
|---|---|---|---|
| {{DATE}} | – | Dokumen dibuat | Awal proyek |

---

## 7. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
