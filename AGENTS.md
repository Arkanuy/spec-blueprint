# AGENTS.md — Aturan Kerja Agen AI di Proyek Ini

> File ini adalah **kontrak** antara pemilik proyek dan agen AI (Claude Code, Codex, Cursor, Copilot, Hermes, atau agen lain) yang bekerja di repo ini. Agen wajib membaca file ini dan dokumen di `docs/` sebelum menulis kode.

**Proyek:** {{PROJECT_NAME}}
**Jenis:** {{PROJECT_TYPE}}
**Stack:** {{STACK}}
**Pemilik produk:** {{OWNER}}

---

## 1. Baca dulu sebelum bertindak

Sebelum menulis atau mengubah kode, agen wajib membaca:

| Urutan | File | Untuk apa |
|---|---|---|
| 1 | `docs/01-prd.md` | Tahu apa yang dibangun dan batasnya |
| 2 | `docs/02-requirements.md` | Tahu perilaku yang harus dipenuhi (FR/NFR/BR) |
| 3 | `docs/03-architecture.md` | Tahu susunan komponen dan batas teknis |
| 4 | `docs/05-data-model.md` | Tahu struktur data yang benar |
| 5 | `docs/06-ui-ux.md` | Tahu tampilan dan semua status layar |
| 6 | `docs/09-risks.md` | Tahu asumsi yang belum diverifikasi |

Kalau salah satu file belum diisi (masih berisi placeholder `[isi]` atau `{{...}}`), **jangan menebak**. Tanyakan ke pemilik produk, atau tandai pekerjaan itu sebagai terblokir.

---

## 2. Aturan yang tidak boleh dilanggar

1. **Jangan membuat fitur tanpa ID requirement.** Setiap pekerjaan harus mengacu ke `FR-xxx` yang ada di `docs/02-requirements.md`. Kalau belum ada, minta requirement-nya dibuat dulu.
2. **Jangan mengubah scope.** Ada ide fitur baru? Tulis di `docs/01-prd.md` bagian "Ide tunda" dan `docs/10-decisions.md`. Jangan langsung dikerjakan.
3. **Jangan menebak aturan bisnis.** Kalau aturan tidak jelas (contoh: apakah boleh membatalkan transaksi setelah dibayar), tanyakan. Jangan pilih sendiri.
4. **Jangan menambah ketergantungan baru tanpa persetujuan.** Library, layanan, atau infrastruktur baru harus dicatat dan disetujui lebih dulu.
5. **Jangan menuliskan rahasia ke kode.** Kredensial hanya dari variabel lingkungan. `.env` tidak pernah masuk git.
6. **Validasi ditegakkan di server.** Menyembunyikan tombol di UI bukan pengamanan.
7. **Jangan mengubah perilaku yang sudah disetujui** tanpa mencatatnya di `docs/10-decisions.md`.
8. **Selalu tangani status gagal.** Setiap fitur baru wajib menangani: kosong, memuat, dan error. Tidak ada pengecualian.

---

## 3. Alur kerja per tugas

```
1. BACA     → baca dokumen terkait untuk tugas ini
2. KONFIRMASI → ulangi tugas dalam satu kalimat + sebutkan FR yang jadi acuan
3. RENCANA  → sebutkan file yang akan disentuh dan pendekatannya
4. KERJAKAN → implementasi hanya pada lingkup itu
5. UJI      → jalankan kasus uji terkait (docs/07-test-plan.md)
6. LAPOR    → apa yang berubah, bukti uji, apa yang belum selesai
7. CATAT    → perbarui dokumen kalau ada yang bergeser
```

Aturan: satu tugas, satu lingkup. Jangan mengerjakan dua fitur sekaligus dalam satu perubahan.

---

## 4. Format laporan setelah selesai

Agen wajib melaporkan dengan format ini, bukan ringkasan bebas:

```
Tugas      : [yang dikerjakan]
FR terkait : FR-001, FR-002
File       : [daftar file yang diubah]
Uji        : TC-001 lulus / gagal — [bukti: keluaran perintah, log]
Belum      : [yang sengaja tidak dikerjakan]
Risiko     : [hal yang perlu diperhatikan]
Dokumen    : [dokumen apa yang diperbarui]
```

Kalau tidak ada bukti uji nyata, tulis **"belum diuji"** — jangan menulis "seharusnya jalan".

---

## 5. Standar kode

| Aspek | Aturan |
|---|---|
| Gaya | Ikuti konvensi yang sudah ada di repo. Jangan menyeragamkan gaya file yang tidak disentuh |
| Penamaan | [sesuai bahasa/stack proyek] |
| Ukuran fungsi | Satu fungsi, satu tanggung jawab |
| Komentar | Jelaskan **kenapa**, bukan **apa**. Kode yang butuh penjelasan "apa" berarti penamaannya kurang jelas |
| Penanganan error | Jangan menelan error diam-diam. Tangani atau teruskan dengan konteks |
| Validasi | Di batas sistem (input) dan di lapisan data |
| Logging | Catat kejadian penting, jangan catat data sensitif |
| Bahasa teks UI | [Indonesia/Inggris — sesuai `docs/06-ui-ux.md`] |
| Komentar & dokumen internal | [Indonesia/Inggris] |

---

## 6. Larangan eksplisit

Agen **tidak boleh**:

- Membuat ulang berkas yang sudah ada tanpa membaca isinya lebih dulu
- Menghapus atau menimpa pekerjaan orang lain tanpa dasar
- Menjalankan perintah merusak (`rm -rf`, reset database produksi, force push) tanpa izin eksplisit
- Mengubah skema database tanpa migrasi
- Menonaktifkan uji yang gagal agar terlihat lulus
- Menambah placeholder yang membuat kode terlihat lengkap tapi tidak berfungsi
- Mengklaim sesuatu sudah selesai tanpa menjalankannya

---

## 7. Saat informasi kurang

Format pertanyaan yang benar:

```
Blokir   : [pekerjaan yang terhenti]
Butuh    : [informasi spesifik]
Kenapa   : [kenapa ini mengubah keputusan]
Sementara : [asumsi yang dipakai kalau harus lanjut — tandai jelas]
```

Jangan mengajukan banyak pertanyaan sekaligus. Ajukan hanya yang benar-benar menghambat, dan jelaskan kenapa.

---

## 8. Bahasa

- Bahasa default komunikasi: **Indonesia**
- Istilah teknis tetap dalam bentuk aslinya, dengan penjelasan singkat saat pertama muncul
- Hindari gaya bahasa pemasaran ("solusi inovatif", "canggih", "seamless") dalam dokumen dan komentar kode

---

## 9. Definisi selesai (Definition of Done)

Sebuah tugas dianggap selesai kalau seluruh poin berikut benar:

- [ ] Perilaku sesuai FR dan kriteria penerimaan terkait
- [ ] Aturan bisnis terkait ditegakkan di server
- [ ] Status kosong, memuat, dan error sudah ditangani
- [ ] Pemeriksaan hak akses ada di server
- [ ] Validasi input ada dengan pesan yang bisa dimengerti pengguna
- [ ] Kasus uji terkait dijalankan dan lulus, dengan bukti
- [ ] Tidak ada kesalahan baru di log saat alur itu dijalankan
- [ ] Dokumen di `docs/` diperbarui kalau ada yang bergeser
- [ ] Laporan akhir ditulis sesuai format bagian 4

---

## 10. Jebakan yang sering terjadi di proyek ini

Isi bagian ini dengan pelajaran nyata dari proyek. Contoh isian:

| Jebakan | Cara menghindari |
|---|---|
| [contoh: migrasi DB lupa dijalankan sebelum deploy] | [jalankan `npx prisma migrate deploy` lebih dulu] |
| [contoh: `.env` menimpa nilai default kode] | [periksa variabel lingkungan sebelum menebak penyebab bug] |

Kalau agen menemukan jebakan baru, tulis di sini dan lanjutkan. Jangan biarkan orang berikutnya menemukan hal yang sama.

---

## 11. Ringkasan satu baris untuk agen

> Kerjakan hanya yang punya ID requirement, jangan menebak aturan bisnis, tegakkan validasi di server, tangani status gagal, uji dengan bukti nyata, dan perbarui dokumen saat kenyataan berubah.
