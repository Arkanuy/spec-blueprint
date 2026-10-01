# Gate 3 — Sebelum Rilis

> Pemeriksaan terakhir sebelum sistem dipakai orang lain. Bukan hanya soal "apakah kodenya jalan" — tapi apakah produk ini benar-benar siap dipakai, dipahami, dan dipulihkan kalau bermasalah.

**Proyek:** {{PROJECT_NAME}}
**Versi yang akan dirilis:** _______
**Tanggal:** _______
**Diperiksa oleh:** _______

---

## A. Fungsi & kebutuhan

- [ ] Semua fitur P0 berfungsi sesuai kriteria penerimaan
- [ ] Semua kasus uji P0 lulus, dengan bukti yang tersimpan
- [ ] Alur utama bisa diselesaikan dari awal sampai akhir tanpa bantuan manual
- [ ] Metrik keberhasilan di PRD sudah bisa diukur (alat ukurnya ada)
- [ ] Kalau ada requirement yang tidak jadi dibuat: sudah dicatat di `10-decisions.md` dengan alasan

## B. Cacat

- [ ] Tidak ada bug keparahan **Kritis** yang terbuka
- [ ] Tidak ada bug keparahan **Tinggi** yang terbuka — kalau ada, sudah ada izin tertulis untuk dirilis
- [ ] Bug Sedang/Rendah yang terbuka sudah terdaftar dengan rencana perbaikan
- [ ] Semua bug sudah dicoba reproduksi ulang setelah diperbaiki (diverifikasi, bukan diasumsikan)

## C. Keamanan

- [ ] Tidak ada kredensial/kunci di kode atau di riwayat git
- [ ] `.env` tidak ikut masuk repositori (sudah diperiksa, bukan diasumsikan)
- [ ] Setiap endpoint memeriksa hak akses di server
- [ ] Kata sandi disimpan dalam bentuk ter-hash
- [ ] Input pengguna divalidasi di batas sistem
- [ ] Data sensitif tidak ditampilkan ke peran yang tidak berhak
- [ ] Pesan error produksi tidak menampilkan detail teknis
- [ ] Akses database produksi dibatasi (bukan kredensial default)

## D. Data & pemulihan

- [ ] Migrasi database sudah dijalankan di lingkungan sasaran
- [ ] Data awal yang wajib (admin, referensi) sudah terisi
- [ ] Backup otomatis sudah menyala
- [ ] **Pemulihan sudah pernah dicoba** — bukan sekadar ada backup
- [ ] Diketahui berapa lama data bisa hilang kalau terjadi kejadian terburuk
- [ ] Data uji/coba-coba sudah dibersihkan atau ditandai jelas

## E. Kesiapan operasional

- [ ] Ada cara memantau sistem berjalan (log/health check)
- [ ] Diketahui cara melihat error kalau ada masalah di produksi
- [ ] Ada cara rollback ke versi sebelumnya, dan sudah dipahami caranya
- [ ] Waktu operasional sistem tercatat dan dipenuhi
- [ ] Performa sudah diperiksa pada kondisi data nyata (bukan hanya data kosong)
- [ ] Diketahui siapa yang dihubungi kalau sistem bermasalah

## F. Dokumentasi & dukungan

- [ ] `README.md` cukup untuk membuat orang lain menjalankan proyek ini
- [ ] Ada panduan singkat untuk pengguna akhir (langkah per tugas nyata)
- [ ] Dokumen `02`–`06` sudah selaras dengan kode (sudah menjalankan prompt `04-sync-docs.md`)
- [ ] Ada catatan perubahan versi (apa yang baru di rilis ini)
- [ ] Diketahui siapa yang bertanggung jawab merawat sistem setelah rilis

## G. Kesiapan pengguna

- [ ] Pengguna sudah mencoba sendiri alur utama (uji penerimaan)
- [ ] Hal yang paling membingungkan bagi pengguna sudah diketahui
- [ ] Panduan/bantuan singkat tersedia di tempat yang mudah dilihat
- [ ] Diketahui cara menampung keluhan dan perbaikan sesudah rilis
- [ ] Perubahan cara kerja sudah dikomunikasikan ke orang yang terdampak

## H. Kebersihan teknis

- [ ] Tidak ada kode debug yang tertinggal (cetak log berlebihan, perintah uji manual)
- [ ] Tidak ada fitur setengah jadi yang terlihat aktif
- [ ] Tidak ada komentar berisi rencana yang tidak akan dikerjakan
- [ ] Tidak ada dependensi yang tidak dipakai
- [ ] Konfigurasi lingkungan sasaran sudah benar (bukan masih menunjuk ke lokal)

## I. Kelengkapan dokumen

- [ ] Tidak ada placeholder `{{...}}` atau `[isi]` di dokumen yang sudah dipakai
- [ ] `10-decisions.md` memuat semua keputusan besar dan perubahan scope
- [ ] `09-risks.md` sudah diperbarui statusnya
- [ ] `08-roadmap.md` mencatat apa yang ditunda beserta syarat pengerjaannya nanti

---

## Hasil

| Bagian | Tercentang | Belum |
|---|---|---|
| A. Fungsi | | |
| B. Cacat | | |
| C. Keamanan | | |
| D. Data | | |
| E. Operasional | | |
| F. Dokumentasi | | |
| G. Pengguna | | |
| H. Kebersihan | | |
| I. Dokumen | | |

**Keputusan:** Rilis / Tunda / Rilis terbatas

**Alasan keputusan:** _______

**Yang harus dibereskan dalam 7 hari setelah rilis:**

| # | Hal | Penanggung jawab | Tenggat |
|---|---|---|---|
| 1 | | | |

Aturan: bagian **B** (tidak ada bug kritis) dan **C** (rahasia tidak bocor) bersifat mutlak. Selain itu boleh ada pengecualian tertulis, asal ada penanggung jawab dan tenggat.

---

## Setelah rilis

Lakukan ini dalam minggu pertama:

- [ ] Periksa log setiap hari selama 3 hari pertama
- [ ] Tanyakan ke pengguna: apa yang paling menyusahkan?
- [ ] Catat masalah nyata yang tidak terpikirkan sebelumnya ke `09-risks.md`
- [ ] Tulis pelajaran di `10-decisions.md` bagian catatan pelajaran
