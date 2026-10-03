# Gate 1 — Sebelum Mulai Coding

> Diperiksa setelah dokumen spec selesai, sebelum menulis baris kode pertama. Kalau ada item yang belum tercentang, **jangan mulai coding** — tanyakan dulu ke pemilik produk. Coding dengan spec setengah matang menghasilkan kode yang harus dibongkar.

**Proyek:** {{PROJECT_NAME}}
**Tanggal pemeriksaan:** _______
**Diperiksa oleh:** _______

---

## A. Masalah & tujuan

- [ ] Masalah utamanya tertulis dalam satu kalimat yang jelas
- [ ] Akar masalah sudah diturunkan sampai penyebab yang bisa diperbaiki (bukan gejala)
- [ ] Ada bukti masalahnya nyata dan berulang (bukan keluhan sekali)
- [ ] Dampak bisnisnya terukur atau minimal dijelaskan secara kualitatif
- [ ] Tujuan bisnis ditulis sebagai hasil, bukan sebagai fitur
- [ ] Sudah dipertimbangkan minimal tiga alternatif solusi, termasuk yang tanpa sistem
- [ ] Ada alasan tertulis kenapa opsi yang dipilih paling proporsional
- [ ] Kalau masalahnya bisa selesai dengan SOP/spreadsheet, keputusan tetap membangun sistem sudah punya alasan

## B. Pengguna

- [ ] Semua peran pengguna terdaftar
- [ ] Setiap peran punya tujuan yang jelas saat memakai sistem
- [ ] Diketahui perangkat dan tingkat kemampuan teknis pengguna
- [ ] Diketahui siapa yang paling terdampak dan siapa yang paling mungkin menolak

## C. Fitur & scope

- [ ] Setiap fitur punya ID (`F-xx`) dan prioritas
- [ ] Setiap fitur punya alasan yang bisa dilacak ke masalah nyata (bukan "supaya lengkap")
- [ ] Tidak ada fitur tanpa alasan — yang ada, sudah dihapus
- [ ] Fitur P0 jelas: tanpa ini produk tidak berguna
- [ ] Out of scope ditulis eksplisit, termasuk hal yang biasanya dianggap otomatis ada
- [ ] Ada daftar "ide tunda" untuk mencegah scope meledak

## D. Requirement

- [ ] Setiap fitur P0 punya user story dan FR
- [ ] Setiap FR memakai kata "Sistem harus ..." dan punya perilaku tunggal
- [ ] Setiap FR P0 punya kriteria penerimaan (AC) yang bisa diuji
- [ ] Tidak ada FR dengan kata kabur ("cepat", "mudah", "user-friendly") tanpa ukuran
- [ ] NFR ditulis yang benar-benar dibutuhkan, bukan dikarang demi kelengkapan
- [ ] Aturan bisnis (BR) yang mengikat sudah terdaftar
- [ ] Ada traceability matrix, dan tidak ada FR yang menggantung tanpa fitur
- [ ] Tidak ada data (`DR-`) yang dipakai tanpa pernah dibuat, atau dibuat tanpa pernah dipakai

## E. Proses

- [ ] Kondisi AS-IS tertulis apa adanya (termasuk alat manual yang dipakai sekarang)
- [ ] Setiap masalah di AS-IS punya penyelesaian di TO-BE, atau dinyatakan tidak diselesaikan
- [ ] Alur status (state flow) punya jalur masuk dan jalur keluar
- [ ] Kondisi tidak normal (exception) sudah diidentifikasi bersama penanganannya
- [ ] Diketahui apa yang berubah bagi orang, bukan hanya bagi sistem
- [ ] Sudah dipikirkan bagaimana pengguna dilatih/dibiasakan

## F. Data

- [ ] Setiap entitas punya alasan bisnis dan dipakai minimal satu proses
- [ ] Aturan integritas ditentukan dan tahu di mana ditegakkan
- [ ] Diketahui data mana yang boleh diubah, dikunci, dan diarsipkan
- [ ] Diketahui data sensitif dan siapa yang boleh melihat
- [ ] Ada rencana migrasi data lama (kalau ada data lama)

## G. Arsitektur & teknis

- [ ] Batas sistem jelas: apa yang di dalam, apa yang di luar
- [ ] Komponen punya tanggung jawab tunggal
- [ ] Tidak ada teknologi yang dipilih karena tren — setiap pilihan punya alasan
- [ ] Hak akses dirancang di server, bukan hanya di tampilan
- [ ] Konfigurasi/rahasia dipisahkan dari kode
- [ ] Ada cara menjalankan di lokal dan cara deploy yang jelas
- [ ] Ada cara backup dan cara pemulihan yang sudah dipikirkan
- [ ] Teknologi yang sengaja **tidak** dipakai sudah dicatat beserta alasannya

## H. Antarmuka

- [ ] Setiap layar P0 terdaftar dengan tujuan dan elemennya
- [ ] Setiap layar menangani status: kosong, kosong karena filter, memuat, gagal validasi, gagal sistem
- [ ] Diketahui tindakan mana yang butuh konfirmasi
- [ ] Diketahui data apa yang tidak boleh tampil untuk peran tertentu
- [ ] Bahasa, format angka, dan format tanggal sudah ditentukan

## I. Rencana kerja

- [ ] Ada definisi "selesai" yang bisa diperiksa untuk tiap fitur
- [ ] Fase pengerjaan berurutan dan realistis
- [ ] Fitur P0 dijadwalkan sebelum P1
- [ ] Ada milestone dengan cara memeriksa ketercapaiannya

## J. Risiko

- [ ] Risiko utama terdaftar dengan cara pengurangan dan penanggung jawab
- [ ] Risiko skor tinggi sudah punya rencana penanganan
- [ ] Semua asumsi terdaftar, dan tahu cara memverifikasinya
- [ ] Pertanyaan yang menghambat P0 sudah terjawab
- [ ] Tidak ada placeholder `{{...}}` atau `[isi]` tersisa di dokumen yang dipakai untuk coding

---

## Kesimpulan

| Jumlah item | Tercentang | Belum |
|---|---|---|
| [n] | [n] | [n] |

**Status:** Siap mulai coding / Perlu perbaikan dokumen dulu

**Item yang belum tercentang dan alasannya:**

| Bagian | Item | Kenapa belum | Kapan diselesaikan |
|---|---|---|---|

**Keputusan:** _______

Aturan: bagian **C**, **D**, dan **F** wajib tuntas seluruhnya sebelum coding dimulai. Bagian lain boleh menyusul sambil jalan, tapi harus punya tanggal penyelesaian.
