# 10 — Decisions & Change Log

> Dokumen ini menjawab: **kenapa sesuatu diputuskan seperti ini, dan apa yang berubah sepanjang proyek.** Tanpa catatan ini, dalam dua minggu tidak ada yang ingat alasan sebuah pilihan — dan pilihan itu akan dibongkar ulang tanpa perlu.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

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

### ADR-001 — Memakai Python 3.10+ pustaka standar tanpa dependensi pihak ketiga

- **Tanggal:** 2026-10-03
- **Status:** Disetujui
- **Konteks:** Toko tidak punya infrastruktur dan tidak ada tenaga IT untuk merawat pemasangan tambahan. Sistem harus bisa dijalankan apa adanya di perangkat toko.
- **Keputusan:** Seluruh sistem dibangun dengan pustaka standar Python: `sqlite3`, `argparse`, `unittest`. Tidak ada `pip install` untuk menjalankannya.
- **Alasan:** Menghapus seluruh risiko pemasangan (versi paket, konflik dependensi, akses internet ke paket). Kode lebih mudah dibaca orang yang merawat toko.
- **Alternatif yang ditolak:** Framework web (Flask/Django/Next.js) — butuh server dan dependensi. ORM (SQLAlchemy) — tidak perlu untuk 3 tabel dan menambah lapisan yang harus dipelajari. Pustaka uji pihak ketiga (pytest) — `unittest` sudah cukup dan ikut bawaan.
- **Konsekuensi:** Pemasangan cukup menyalin folder. Yang jadi lebih sulit: beberapa kemudahan framework (mis. validasi otomatis, templating) harus ditulis sendiri.

### ADR-002 — Antarmuka CLI, bukan aplikasi web

- **Tanggal:** 2026-10-03
- **Status:** Disetujui
- **Konteks:** Masalahnya adalah rekap manual dan stok yang tidak akurat. Aktor bekerja di satu meja kasir; tidak ada kebutuhan diakses dari luar toko.
- **Keputusan:** Antarmuka berupa perintah baris: `python -m app produk|jual|rekap|batal`.
- **Alasan:** Menghilangkan kebutuhan server, browser, dan pemasangan; bisa dijalankan di perangkat toko apa pun yang punya Python. Kasir dapat melayani antrean tanpa membuka aplikasi berat.
- **Alternatif yang ditolak:** Aplikasi web (Flask + template) — menambah server lokal, browser, dan risiko yang tidak dibutuhkan. Aplikasi mobile (Android) — butuh pemasangan dan distribusi; perangkat tidak pasti. Aplikasi desktop berbasis GUI — menambah ketergantungan grafis tanpa manfaat untuk alur yang hanya memasukkan SKU:QTY.
- **Konsekuensi:** Ringan, cepat, dan mudah diuji otomatis. Yang jadi lebih sulit: kasir harus mengetik perintah dan tidak ada tombol; pelatihan singkat wajib (lihat `04-workflow.md` bagian 10).

### ADR-003 — Harga satuan disalin ke baris transaksi

- **Tanggal:** 2026-10-03
- **Status:** Disetujui
- **Konteks:** Harga master produk bisa berubah dari waktu ke waktu. Transaksi lama harus tetap bisa dipertanggungjawabkan dengan harga saat barang terjual.
- **Keputusan:** `sale_items.harga_satuan` menyimpan salinan `products.harga` pada saat transaksi dibuat (BR-002). Harga tidak diambil ulang dari master saat membaca riwayat.
- **Alasan:** Menjaga riwayat harga tidak berubah kalau master produk diedit. Total transaksi lama tetap konsisten dan dapat diaudit.
- **Alternatif yang ditolak:** Hanya menyimpan `product_id` dan selalu membaca harga master — transaksi lama ikut berubah saat harga naik, sehingga rekap dan sengketa harga menjadi tidak dapat dipercaya. Menyimpan harga di luar basis data (mis. di nota) — mengembalikan masalah asal.
- **Konsekuensi:** Riwayat harga utuh dan rekap historis bisa dipercaya. Yang jadi lebih sulit: penyimpanan sedikit lebih besar dan setiap baris harus dijaga agar tidak diubah setelah tersimpan.

### ADR-004 — Pembatalan maksimal sekali, wewenang Pemilik (tanpa penegakan teknis)

- **Tanggal:** 2026-10-03
- **Status:** Disetujui
- **Konteks:** Transaksi salah input harus bisa dianulir, tetapi pembatalan juga bisa disalahgunakan untuk menutupi selisih kas (uang sudah diambil, transaksi lalu dibatalkan). Kasir yang memegang kas tidak boleh bisa membatalkan transaksinya sendiri.
- **Keputusan:** Transaksi berstatus SELESAI boleh dibatalkan maksimal satu kali (BR-006), dengan alasan minimal 5 karakter (BR-007). Pembatalan mengembalikan stok (BR-008) dan mengeluarkan transaksi dari rekap (FR-009). Wewenang pembatalan ada di Pemilik. **Penegakan wewenang itu bersifat organisasi, bukan teknis**: kode hanya memeriksa status dan alasan, tidak memeriksa peran.
- **Alasan:** Yang bisa ditegakkan sistem tanpa autentikasi adalah batas frekuensi dan syarat alasan — dan itu sudah ditegakkan. Menambah pemeriksaan peran tanpa autentikasi tidak menambah keamanan apa pun: argumen peran bisa diketik siapa saja yang memegang terminal. Menuliskan ini apa adanya lebih berguna daripada mengklaim kontrol yang tidak ada.
- **Alternatif yang ditolak:** (a) Boleh dibatalkan siapa saja berkali-kali — membuka celah selisih kas dan laporan yang bisa diubah berulang tanpa jejak. (b) Pembatalan tanpa alasan — tidak ada jejak audit. (c) Menghapus transaksi salah — menghilangkan jejak dan stok tidak bisa dipulihkan dengan pasti. (d) Menambahkan argumen `--peran pemilik` — pengamanan palsu, sama jenisnya dengan menyembunyikan tombol di tampilan.
- **Konsekuensi:** Selisih kas lebih sulit disembunyikan dan laporan lebih dipercaya. Yang jadi lebih sulit: pembatalan sah harus menunggu pemilik, tidak ada koreksi sebagian (partial refund), dan **tidak ada jaminan teknis** selama autentikasi belum dibuat. Pemicu perubahan: begitu ada kasir tambahan atau lebih dari satu terminal, autentikasi menjadi prasyarat (Q-03).


### ADR-005 — SQLite sebagai basis data

- **Tanggal:** 2026-10-03
- **Status:** Disetujui
- **Konteks:** Data harus tetap ada setelah proses ditutup (NFR-001), sistem berjalan tanpa internet (NFR-002), dan tidak ada server. Basis data harus kuat terhadap mati listrik di tengah transaksi.
- **Keputusan:** Basis data berkas SQLite lokal; path dari env `KASIR_DB` (default `kasir.db` di cwd). Semua penulisan transaksi dibungkus dalam satu transaksi SQLite.
- **Alasan:** Pustaka standar (tanpa pemasangan), transaksional (ACID), satu berkas yang mudah dicadangkan dengan menyalin, tidak butuh server.
- **Alternatif yang ditolak:** PostgreSQL/MySQL — butuh server dan perawatan. Basis data cloud — dilarang oleh NFR-002 dan menambah ketergantungan pihak ketiga. Menyimpan ke berkas teks/CSV — tidak ada jaminan integritas dan rawan korup saat penulisan terputus.
- **Konsekuensi:** Sederhana, cepat, dan mudah dicadangkan. Yang jadi lebih sulit: tidak ada akses serentak dari beberapa perangkat (memang tidak dibutuhkan sekarang) dan migrasi skema harus ditangani sendiri (utang teknis #2 di `03-architecture.md`).

---

## 2. Log perubahan scope

Setiap kali ada fitur ditambah, dikurangi, atau diubah prioritasnya — catat di sini **beserta alasannya**. Ini yang mencegah scope meledak tanpa disadari.

| Tanggal | Perubahan | Jenis | Alasan | Dampak (waktu/kode/dokumen) | Diputuskan oleh | Dokumen yang diperbarui |
|---|---|---|---|---|---|---|
| 2026-10-03 | Lima fitur P0 (F-01…F-05) ditetapkan sebagai lingkup rilis pertama | Tambah | Semua terlacak ke akar masalah di `00-discovery.md` | Menentukan seluruh FR dan TC | Pemilik | 00-discovery, 01-prd, 02-requirements |
| 2026-10-03 | Ekspor rekap diturunkan ke P1 (parking lot) | Tunda | Bukan bagian dari masalah saat ini | Mengurangi lingkup rilis | Pemilik | 01-prd (ide tunda) |
| 2026-10-03 | Pembelian dari pemasok, multi-cabang, diskon, cetak struk, login, sinkronisasi, laporan bulanan, ekspor Excel dinyatakan OUT OF SCOPE | Kurangi | Tidak proporsional; tidak ada proses P0 yang memakainya | Tidak ada FR tambahan | Pemilik | 01-prd, 02-requirements |

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
| 2026-10-03 | semua | – | Dokumen awal dibuat | Awal proyek |

---

## 4. Keputusan yang menunggu

| # | Keputusan yang dibutuhkan | Menghambat apa | Pilihan yang tersedia | Tenggat | Siapa yang memutuskan |
|---|---|---|---|---|---|
| 1 | Siapa boleh membatalkan transaksi (Q-03) | Peran yang berwenang | Kasir saja / Pemilik saja / keduanya | 2026-10-07 | Pemilik (penegakan organisasi, bukan teknis — lihat ADR-004) |
| 2 | Tenggat proyek & target milestone (Q-05) | Target M1–M3 di `08-roadmap.md` | Berbagai tanggal | 2026-10-10 | Pemilik |
| 3 | Perangkat target & spesifikasi (Q-04) | Validasi NFR-005 | Perangkat yang ada / perangkat baru | 2026-10-10 | Pemilik |

---

## 5. Keputusan yang dibatalkan / digantikan

| ADR | Keputusan lama | Digantikan oleh | Tanggal | Alasan |
|---|---|---|---|---|
| – | Belum ada keputusan yang dibatalkan | – | – | – |

---

## 6. Catatan pelajaran (retrospective)

Diisi menjelang akhir fase atau setelah masalah besar. Berguna agar tidak mengulang kesalahan yang sama di proyek berikutnya.

| Tanggal | Apa yang terjadi | Akar penyebab | Yang akan dilakukan berbeda |
|---|---|---|---|
| – | Belum ada fase yang selesai; diisi setelah Fase 1 | – | – |

---

## 7. Riwayat perubahan dokumen ini

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |
| 0.2 | 2026-10-03 | ADR-004 diperbaiki: klaim "penegakan peran di lapisan logika" dihapus, diganti penjelasan bahwa wewenang Pemilik bersifat organisasi dan tidak ditegakkan kode | Kode tidak memeriksa peran sama sekali (tidak ada autentikasi). Dokumen sebelumnya mengklaim kontrol yang tidak ada — persis kesalahan yang dokumen ini seharusnya cegah |