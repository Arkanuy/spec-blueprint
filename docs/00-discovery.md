# 00 — Discovery & Konteks Bisnis

> Tujuan dokumen ini: memastikan masalahnya **nyata**, akar masalahnya **benar**, dan sistem adalah **solusi yang proporsional**. Dokumen ini ditulis sebelum PRD. Kalau bagian ini kosong, PRD akan berisi tebakan.

**Proyek:** {{PROJECT_NAME}}
**Domain bisnis:** {{DOMAIN}}
**Pemilik produk:** {{OWNER}}
**Tanggal:** {{DATE}}

---

## 1. Konteks organisasi

| Item | Isi |
|---|---|
| Nama organisasi / usaha | {{OWNER}} |
| Bidang usaha | {{DOMAIN}} |
| Produk / layanan utama | [isi] |
| Pelanggan utama | [isi] |
| Perkiraan skala operasi | [butuh data: jumlah transaksi/hari, jumlah staf, jumlah pelanggan] |
| Unit yang terlibat | [isi] |
| Sistem yang sudah dipakai sekarang | [isi, tulis "belum ada / manual / spreadsheet / nama aplikasi"] |

<!-- EXAMPLE-START -->
Contoh (isi dan hapus setelah dipakai):

| Item | Isi |
|---|---|
| Nama organisasi / usaha | Toko Berkah |
| Bidang usaha | Retail perlengkapan sekolah |
| Produk / layanan utama | Penjualan barang eceran + grosir |
| Pelanggan utama | Siswa, orang tua, sekolah |
| Perkiraan skala operasi | ±120 transaksi/hari, 4 staf kasir, 1 pemilik |
| Unit yang terlibat | Kasir, gudang, pemilik |
| Sistem yang sudah dipakai sekarang | Buku nota manual + rekap Excel mingguan |
<!-- EXAMPLE-END -->

---

## 2. Stakeholder

Siapa saja yang terlibat atau terpengaruh. Bedakan **stakeholder** (terpengaruh) dari **aktor** (langsung memakai sistem).

| Stakeholder | Peran | Kepentingan utama | Info yang butuh | Info yang dihasilkan | Titik sakit | Aktor sistem? |
|---|---|---|---|---|---|---|
| [nama peran] | [tanggung jawab] | [tujuan] | [data yang harus dia lihat] | [data yang dia masukkan] | [masalah yang dia rasakan] | Ya/Tidak |

Catatan: tidak semua stakeholder jadi aktor. Pemilik usaha sering hanya butuh laporan (stakeholder), bukan pengguna aplikasi.

---

## 3. Kondisi saat ini (AS-IS)

Tulis proses yang berjalan sekarang, apa adanya — termasuk alat manual, WhatsApp, Excel, buku tulis. **Jangan** memasukkan fitur sistem yang belum ada ke bagian ini.

### 3.1 Proses sekarang, langkah per langkah

| # | Aktor | Aktivitas | Input | Output | Alat | Waktu/durasi | Masalah terlihat |
|---|---|---|---|---|---|---|---|
| 1 | [peran] | [langkah] | [data/mask] | [hasil] | [manual/Excel/aplikasi X] | [estimasi] | [apa yang tidak lancar] |

### 3.2 Di mana pekerjaan terasa berat

- [aktivitas yang berulang dan memakan waktu]
- [perlu verifikasi berulang]
- [data yang harus dimasukkan dua kali]
- [informasi yang tersebar di banyak tempat]
- [laporan yang harus dirakit manual]

### 3.3 Bukti pendukung

Kumpulkan bukti, bukan opini:

- [ ] Dokumen yang dipakai sekarang (foto nota, screenshot Excel, template laporan)
- [ ] Jumlah transaksi / volume pekerjaan per periode → sumber: [isi]
- [ ] Keluhan pelanggan atau staf → dikatakan oleh: [isi]
- [ ] Data lama yang bisa dihitung (contoh: rata-rata pesanan salah per bulan) → [isi]

Kalau bukti belum ada, tulis `(Perlu dikonfirmasi)` dan masukkan ke 09-risks.md.

---

## 4. Pohon masalah

### 4.1 Gejala (yang terlihat sehari-hari)

1. [gejala yang bisa diamati, bukan tafsiran]
2. [gejala kedua]

### 4.2 Akar masalah (5 Whys)

Ambil gejala paling penting, turunkan sampai penyebab yang benar-benar bisa diperbaiki:

| Tingkat | Pertanyaan | Jawaban |
|---|---|---|
| 1 | Kenapa [gejala] terjadi? | [jawaban] |
| 2 | Kenapa [jawaban 1] bisa terjadi? | [jawaban] |
| 3 | Kenapa [jawaban 2] terjadi? | [jawaban] |
| 4 | Kenapa [jawaban 3] terjadi? | [jawaban] |
| 5 | Akar masalah | [penyebab dasar yang bisa diperbaiki] |

<!-- EXAMPLE-START -->
Contoh:
1. Kenapa rekap penjualan sering salah? → Karena nota hilang / tulisan tidak terbaca.
2. Kenapa nota bisa hilang? → Karena pencatatan masih di kertas dan tidak ada cadangan.
3. Kenapa masih pakai kertas? → Karena tidak ada tempat menyimpan data yang bisa diakses semua kasir.
4. Kenapa perlu diakses semua kasir? → Karena transaksi terjadi di 2 kasir berbeda pada jam sibuk.
5. **Akar masalah:** tidak ada satu sumber data transaksi yang terpusat dan bisa dipercaya.
<!-- EXAMPLE-END -->

### 4.3 Apakah masalah ini nyata?

| Uji | Jawaban | Bukti |
|---|---|---|
| Terjadi berulang, bukan sekali | [Ya/Tidak] | [bukti] |
| Menimbulkan kerugian terukur (waktu/uang/risiko) | [Ya/Tidak] | [bukti] |
| Ada orang yang bertanggung jawab merasakannya | [nama peran] | [bukti] |
| Tidak bisa diselesaikan hanya dengan kebiasaan baru | [Ya/Tidak] | [alasan] |

Kalau ada jawaban "Tidak" di sini, **jangan lanjut ke PRD**. Perbaiki dulu rumusan masalahnya, karena sistem tidak akan menyelesaikan masalah yang bukan masalah.

---

## 5. Dampak bisnis

| Dimensi | Dampak saat ini | Bagaimana diukur |
|---|---|---|
| Waktu | [contoh: 3 jam/minggu untuk rekap manual] | [metode ukur] |
| Biaya | [contoh: selisih stok menyebabkan modal hilang] | [metode ukur] |
| Pengalaman pelanggan | [isi] | [metode ukur] |
| Beban kerja staf | [isi] | [metode ukur] |
| Kualitas data | [isi] | [metode ukur] |
| Pengambilan keputusan | [isi] | [metode ukur] |
| Risiko / kepatuhan | [isi] | [metode ukur] |

Aturan: **jangan mengarang angka.** Kalau belum ada data, tulis `[butuh data]` dan sebutkan cara mendapatkannya.

---

## 6. Tujuan bisnis

Ubah masalah menjadi tujuan yang menggambarkan hasil, bukan fitur.

| # | Tujuan | Terhubung ke akar masalah | Indikator keberhasilan |
|---|---|---|---|
| G-1 | [tujuan bisnis] | [akar masalah #] | [indikator + target] |

<!-- EXAMPLE-START -->
Contoh:
| G-1 | Tersedianya data penjualan yang konsisten dari semua kasir | Akar masalah #5 | Selisih rekap mingguan turun dari 8% ke <1% |
| G-2 | Pemilik bisa melihat performa harian tanpa menunggu rekap manual | Akar masalah #5 | Laporan tersedia <1 menit setelah toko tutup |
<!-- EXAMPLE-END -->

Tujuan buruk: "Membuat aplikasi kasir." — itu solusi, bukan tujuan.

---

## 7. Evaluasi alternatif solusi

**Jangan langsung memilih sistem.** Bandingkan minimal 3 opsi, termasuk opsi paling murah.

| Alternatif | Cara kerja | Kelebihan | Kekurangan | Perkiraan biaya/effort | Cocok? |
|---|---|---|---|---|---|
| A. Perbaikan proses saja (SOP + form standar) | [isi] | [isi] | [isi] | [rendah] | [Ya/Tidak] |
| B. Perbaikan proses + spreadsheet terstruktur | [isi] | [isi] | [isi] | [rendah-sedang] | [Ya/Tidak] |
| C. Aplikasi sederhana (1 modul inti) | [isi] | [isi] | [isi] | [sedang] | [Ya/Tidak] |
| D. Aplikasi lengkap multi-modul | [isi] | [isi] | [isi] | [tinggi] | [Ya/Tidak] |

### Keputusan

- **Dipilih:** [A/B/C/D]
- **Alasan:** [kenapa opsi ini paling proporsional terhadap masalah]
- **Yang sengaja tidak diambil sekarang:** [dan kenapa]

Aturan: kalau masalah bisa selesai dengan SOP atau spreadsheet, sistem **tidak wajib dibuat** — dan itu keputusan yang sah.

---

## 8. Kelayakan

| Aspek | Penilaian | Catatan |
|---|---|---|
| Teknis | [bisa / perlu kajian] | [stack, kemampuan tim, infrastruktur] |
| Ekonomi | [layak / belum jelas] | [biaya kira-kira vs manfaat] |
| Operasional | [siap / belum] | [kemampuan staf memakai & merawat] |
| Jadwal | [cukup / ketat] | [tenggat, ketersediaan waktu] |
| Organisasi | [didukung / berisiko ditolak] | [siapa yang mendukung, siapa yang menolak] |
| Hukum / kebijakan | [aman / perlu izin] | [data pribadi, aturan internal] |

---

## 9. Ringkasan satu halaman

Tulis ≤10 baris. Ini yang dibaca AI dan orang sibuk.

```
Masalah   : ...
Akar      : ...
Dampak    : ...
Tujuan    : ...
Solusi    : ...
Batasan   : ...
Sukses jika: ...
Gagal jika : ...
```

---

## 10. Yang belum diketahui

Pindahkan semua ketidakpastian ke [09-risks.md](09-risks.md) dengan nomor `Q-xx` agar bisa dilacak.

- Q-01: [pertanyaan yang jawabannya mengubah desain]
- Q-02: [asumsi yang belum diverifikasi]
