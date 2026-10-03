# AGENTS.md — Aturan kerja agen AI di proyek ini

> File ini adalah kontrak antara pemilik proyek dan agen AI (Claude Code, Codex, Cursor, Copilot,
> Hermes, atau agen lain). Agen wajib membaca `docs/` sebelum menulis kode.

**Proyek:**
**Stack:**
**Pemilik produk:**

---

## 1. Baca dulu sebelum bertindak

| Urutan | File | Untuk apa |
|---|---|---|
| 1 | `docs/00-masalah.md` | Tahu masalah apa yang diselesaikan dan batasnya |
| 2 | `docs/01-kebutuhan.md` | Tahu perilaku yang harus dipenuhi (FR/NFR/BR) |
| 3 | `docs/02-desain.md` | Tahu susunan komponen dan batas teknis |
| 4 | `docs/04-data.md` | Tahu struktur data yang benar |
| 5 | `docs/05-tampilan.md` | Tahu tampilan dan semua kondisi gagal |
| 6 | `docs/08-risiko.md` | Tahu asumsi yang belum diverifikasi |

Kalau ada bagian yang masih kosong, **jangan menebak**. Tanyakan, atau tandai pekerjaan itu terblokir.

---

## 2. Aturan yang tidak boleh dilanggar

1. **Jangan membuat fitur tanpa ID kebutuhan.** Setiap pekerjaan mengacu ke `FR-xxx` di `docs/01-kebutuhan.md`. Kalau belum ada, minta dibuat dulu.
2. **Jangan mengubah ruang lingkup.** Ide fitur baru masuk `docs/00-masalah.md` bagian "Ide tunda" dulu, jangan langsung dikerjakan.
3. **Jangan menebak aturan bisnis.** Kalau aturannya tidak jelas, tanyakan. Jangan pilih sendiri.
4. **Jangan menambah dependensi baru** tanpa persetujuan; catat alasannya.
5. **Jangan menulis rahasia di kode.** Kredensial hanya dari variabel lingkungan; `.env` tidak masuk git.
6. **Validasi ditegakkan di server.** Menyembunyikan tombol di tampilan bukan pengamanan.
7. **Jangan mengubah perilaku yang sudah disetujui** tanpa mencatatnya di `docs/08-risiko.md`.
8. **Selalu tangani kondisi gagal**: kosong, memuat, dan error.

---

## 3. Alur kerja per tugas

```
1. BACA       → baca dokumen terkait
2. KONFIRMASI → ulangi tugas dalam satu kalimat + sebutkan FR acuannya
3. RENCANA    → sebutkan file yang akan disentuh dan pendekatannya
4. KERJAKAN   → implementasi hanya pada lingkup itu
5. UJI        → jalankan kasus uji terkait (docs/06-uji.md)
6. LAPOR      → apa yang berubah, bukti uji, apa yang belum selesai
7. CATAT      → perbarui dokumen kalau ada yang bergeser
```

Satu tugas, satu ruang lingkup. Jangan mengerjakan dua fitur dalam satu perubahan.

---

## 4. Format laporan

```
Tugas      : [yang dikerjakan]
Kebutuhan  : [ID kebutuhan yang jadi acuan]
File       : [daftar file yang diubah]
Uji        : [ID kasus uji] lulus / gagal — [bukti: keluaran perintah]
Belum      : [yang sengaja tidak dikerjakan]
Risiko     : [hal yang perlu diperhatikan]
Dokumen    : [dokumen yang diperbarui]
```

Kalau tidak ada bukti uji nyata, tulis **"belum diuji"** — jangan menulis "seharusnya jalan".

---

## 5. Standar kode

| Aspek | Aturan |
|---|---|
| Gaya | Ikuti konvensi yang sudah ada di repo |
| Ukuran fungsi | Satu fungsi, satu tanggung jawab |
| Komentar | Jelaskan **kenapa**, bukan **apa** |
| Penanganan error | Jangan menelan error diam-diam; tangani atau teruskan dengan konteks |
| Validasi | Di batas sistem (input) dan di lapisan data |
| Logging | Catat kejadian penting; jangan catat data sensitif |
| Bahasa teks UI | |
| Bahasa komentar | |

---

## 6. Larangan

Agen **tidak boleh**:

- Membuat ulang berkas yang sudah ada tanpa membacanya lebih dulu
- Menghapus atau menimpa pekerjaan orang lain tanpa dasar
- Menjalankan perintah merusak (`rm -rf`, reset database, force push) tanpa izin eksplisit
- Mengubah skema database tanpa migrasi
- Menonaktifkan uji yang gagal agar terlihat lulus
- Menambah placeholder yang membuat kode terlihat lengkap tapi tidak berfungsi
- Mengklaim sesuatu sudah selesai tanpa menjalankannya

---

## 7. Kalau informasi kurang

```
Blokir    : [pekerjaan yang terhenti]
Butuh     : [informasi spesifik]
Kenapa    : [kenapa ini mengubah keputusan]
Sementara : [asumsi yang dipakai kalau harus lanjut — tandai jelas]
```

Ajukan hanya pertanyaan yang benar-benar menghambat.

---

## 8. Bahasa

- Bahasa default: **Indonesia**
- Istilah teknis tetap aslinya, beri penjelasan singkat saat pertama muncul
- Hindari gaya bahasa pemasaran ("solusi inovatif", "canggih", "seamless")

---

## 9. Jebakan yang sudah diketahui

Isi tabel ini dengan pelajaran nyata. Kalau menemukan jebakan baru, tulis di sini.

| Jebakan | Cara menghindari |
|---|---|
| | |
