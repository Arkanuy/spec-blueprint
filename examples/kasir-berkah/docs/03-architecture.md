# 03 — Architecture

> Dokumen ini menjawab: **sistemnya tersusun dari apa, batasnya di mana, dan bagaimana bagian-bagiannya bicara satu sama lain.** Ditulis setelah requirement jelas. Arsitektur mengikuti kebutuhan — bukan kebutuhan yang dipaksa mengikuti arsitektur yang sedang populer.

**Proyek:** Kasir Berkah
**Stack:** Python 3.10+ (stdlib), SQLite
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

---

## 1. Prinsip arsitektur

Tulis 3–6 prinsip yang mengikat semua keputusan teknis. Prinsip ini yang dipakai untuk menolak usulan yang tidak sesuai.

| # | Prinsip | Konsekuensi praktis |
|---|---|---|
| P-1 | Sesederhana yang bisa menyelesaikan masalah | Satu proses Python, satu basis data berkas; tidak ada layanan/infra tambahan |
| P-2 | Satu sumber kebenaran untuk setiap data | Harga master produk disalin ke baris transaksi; tidak ada harga yang hidup di dua tempat saat dipakai |
| P-3 | Validasi ditegakkan di lapisan logika, bukan hanya di CLI | BR-001…BR-010 diperiksa di fungsi layanan sebelum menulis ke SQLite, sehingga tidak bisa dilewati |
| P-4 | Data transaksi tidak pernah dihapus, hanya diberi status | Pembatalan mengubah status dan mencatat alasan; baris transaksi tetap ada untuk jejak audit |
| P-5 | Berjalan di perangkat toko tanpa internet dan tanpa dependensi pihak ketiga | Hanya `sqlite3`, `argparse`, `unittest` dari pustaka standar |

---

## 2. Scope sistem

### 2.1 Yang termasuk sistem ini

- Perintah CLI `produk tambah` dan `produk daftar`.
- Perintah CLI `jual` (catat penjualan, hitung total & kembalian, kurangi stok).
- Perintah CLI `rekap` (rekap harian).
- Perintah CLI `batal` (pembatalan + pengembalian stok).
- Penyimpanan data di berkas SQLite lokal.

### 2.2 Yang di luar sistem ini

| Hal | Kenapa di luar | Ditangani oleh |
|---|---|---|
| Pembelian dari pemasok | Bukan akar masalah saat ini | Pemilik secara manual saat ini |
| Diskon/promo | Aturan harga tambahan di luar BR yang disepakati | Belum ada |
| Cetak struk ke printer | Butuh perangkat & driver | Belum ada |
| Login berbasis password | Satu perangkat, dua aktor saling percaya | Fisik: siapa yang memegang terminal |
| Sinkronisasi online / multi-perangkat | Koneksi toko tidak stabil, satu lokasi | Belum ada |
| Pembayaran non-tunai | Di luar lingkup P0 | Kasir secara manual |
| Akuntansi (jurnal, hutang-piutang) | Produk bukan sistem akuntansi | Pemilik / pembukuan terpisah |

### 2.3 Konteks sistem (siapa bicara dengan sistem)

```
                 ┌──────────────────────────────┐
     Kasir   ──▶ │                              │
                 │        Kasir Berkah          │
     Pemilik ──▶ │   (perintah CLI di terminal) │
                 └──────────────┬───────────────┘
                                │ baca/tulis (sqlite3)
                                ▼
                       ┌──────────────────┐
                       │  kasir.db (SQLite)│
                       └──────────────────┘
```

Sistem tidak berbicara dengan layanan eksternal apa pun. Satu-satunya mitra adalah berkas SQLite lokal.

---

## 3. Daftar komponen

| Komponen | Tanggung jawab | Teknologi | Alasan memilih | Batasan |
|---|---|---|---|---|
| `app/__main__.py` (CLI) | Menerjemahkan perintah baris ke pemanggilan layanan; mencetak hasil/kesalahan; menentukan kode keluar | `argparse` | Pustaka standar; tidak perlu instalasi; perintah bisa dibaca kasir | Wajib dipanggil dengan `python -m app` |
| `app/layanan.py` (logika bisnis) | Menegakkan BR-001…BR-010, menghitung total/kembalian, mengubah stok, menandai batal | Python murni | Menyimpan aturan di satu tempat yang bisa diuji tanpa CLI | Tidak menulis langsung ke berkas; lewat lapisan data |
| `app/data.py` (lapisan data) | Membuka koneksi, menjalankan skema, membaca/menulis `products`, `sales`, `sale_items`; memakai transaksi SQLite | `sqlite3` | Pustaka standar; mendukung transaksi ACID; berkas portabel | Tabel dan indeks dibuat saat pertama dijalankan |
| Skema `schema.sql` | Mendefinisikan 3 tabel dan indeks | SQLite DDL | Sumber tunggal struktur tabel, dijalankan sekali | Perubahan skema harus lewat migrasi sederhana |
| `tests/` | Bukti setiap FR via `unittest` | `unittest` | Pustaka standar; bisa dijalankan siapa saja | Basis data sementara per uji |
| Berkas `kasir.db` | Menyimpan data nyata | SQLite | Tanpa server; tetap ada setelah proses ditutup (NFR-001) | Path dari env `KASIR_DB`, default `kasir.db` |

Aturan: satu komponen, satu tanggung jawab. Lapisan logika dan lapisan data dipisah supaya aturan bisnis bisa diuji tanpa memanggil CLI, dan CLI tetap tipis.

---

## 4. Diagram arsitektur

```
   Kasir / Pemilik
        │  mengetik perintah
        ▼
  ┌─────────────────────┐   python -m app
  │  CLI (argparse)     │   produk | jual | rekap | batal
  │  __main__.py        │   → mencetak hasil, kode keluar 0/1/2
  └──────────┬──────────┘
             │ panggil fungsi (Python)
             ▼
  ┌─────────────────────┐
  │  Logika bisnis      │   BR-001..BR-010, hitung total/kembalian,
  │  layanan.py         │   ubah stok, tanda batal
  └──────────┬──────────┘
             │ baca/tulis
             ▼
  ┌─────────────────────┐
  │  Lapisan data       │   products | sales | sale_items
  │  data.py + schema   │
  └──────────┬──────────┘
             │ sqlite3 (ACID, transaksional)
             ▼
  ┌─────────────────────┐
  │  kasir.db (SQLite)  │   berkas lokal di perangkat toko
  └─────────────────────┘
```

Setiap kotak muncul di tabel komponen. Setiap garis berlabel: CLI→layanan (panggilan fungsi Python), layanan→data (baca/tulis), data→berkas (`sqlite3`).

---

## 5. Alur data

Untuk setiap alur penting, tulis: **siapa** → **apa** → **disimpan di mana** → **siapa yang membaca**.

### 5.1 Alur: Kasir menyimpan penjualan (`jual`)

| Langkah | Dari | Ke | Data | Format | Sifat |
|---|---|---|---|---|---|
| 1 | Kasir | CLI | `--produk SKU:QTY`, `--bayar`, `--kasir` | argumen perintah | sinkron |
| 2 | CLI | Logika bisnis | daftar (SKU, qty), bayar, kasir | objek Python | sinkron |
| 3 | Logika bisnis | Lapisan data | cari produk per SKU; periksa stok; hitung total | fungsi Python | sinkron |
| 4 | Logika bisnis | Lapisan data | tulis 1 `sales` + N `sale_items` + kurangi `products.stok` | transaksi SQLite | **transaksional (semua atau tidak sama sekali)** |
| 5 | Lapisan data | kasir.db | baris baru `sales`, `sale_items`; `products.stok` diperbarui | SQL | transaksional |
| 6 | CLI | Kasir | kode `TRX-YYYYMMDD-###`, total, kembalian | teks di stdout | sinkron |

Sifat transaksi pada langkah 4 penting: kalau satu baris gagal disimpan, seluruh transaksi dibatalkan agar stok tidak berkurang tanpa transaksi tercatat.

### 5.2 Alur: Pemilik melihat rekap (`rekap`)

| Langkah | Dari | Ke | Data | Format | Sifat |
|---|---|---|---|---|---|
| 1 | Pemilik | CLI | `--tanggal YYYY-MM-DD` | argumen | sinkron |
| 2 | CLI | Logika bisnis | tanggal | objek Python | sinkron |
| 3 | Logika bisnis | Lapisan data | jumlah transaksi, total penjualan, total item terjual untuk tanggal & status SELESAI | query SQL (baca saja) | sinkron |
| 4 | CLI | Pemilik | tiga angka rekap | teks di stdout | sinkron |

### 5.3 Alur: Pembatalan transaksi (`batal`)

| Langkah | Dari | Ke | Data | Format | Sifat |
|---|---|---|---|---|---|
| 1 | Pemilik | CLI | `--kode TRX-...`, `--alasan "..."` | argumen | sinkron |
| 2 | CLI | Logika bisnis | kode, alasan | objek Python | sinkron |
| 3 | Logika bisnis | Lapisan data | ambil transaksi; periksa status SELESAI & alasan ≥ 5 karakter | fungsi Python | sinkron |
| 4 | Logika bisnis | Lapisan data | ubah status → DIBATALKAN; isi alasan; kembalikan stok tiap baris | transaksi SQLite | **transaksional** |
| 5 | CLI | Pemilik | konfirmasi status DIBATALKAN dan stok yang dikembalikan | teks di stdout | sinkron |

---

## 6. Boundary & kontrak

### 6.1 Perintah CLI (kontrak antarmuka)

Sistem ini CLI, jadi kontraknya adalah perintah. Setiap perintah harus terhubung ke minimal satu FR.

| Perintah | Tujuan | Masukan | Keluaran | Peran | FR terkait | Kode keluar sukses/gagal |
|---|---|---|---|---|---|---|
| `python -m app produk tambah --sku SKU --nama "Nama" --harga 3500 --stok 40` | Menambah produk | sku, nama, harga, stok | Konfirmasi produk ditambahkan | Kasir | FR-001, BR-010 | 0 / 1 (SKU duplikat, angka tidak valid) |
| `python -m app produk daftar` | Menampilkan daftar produk | – | daftar SKU, nama, harga, stok | Kasir | FR-001 | 0 / 2 |
| `python -m app jual --produk SKU:QTY [--produk SKU:QTY ...] --bayar 50000 --kasir "Nadia"` | Mencatat penjualan | daftar SKU:QTY, bayar, kasir | kode transaksi, total, kembalian | Kasir | FR-002…FR-007 | 0 / 1 (stok kurang, bayar kurang, qty tidak valid, SKU ganda) |
| `python -m app rekap --tanggal 2026-10-03` | Rekap harian | tanggal | jumlah transaksi, total penjualan, total item terjual | Pemilik | FR-008, FR-009 | 0 / 1 (format tanggal salah) |
| `python -m app batal --kode TRX-20261003-001 --alasan "salah input"` | Membatalkan transaksi | kode, alasan | konfirmasi status DIBATALKAN + stok kembali | Pemilik | FR-010…FR-012 | 0 / 1 (alasan < 5, sudah dibatalkan, kode tak ada) |

Kode keluar (exit code): `0` berhasil, `1` kesalahan aturan bisnis (pesan jelas ke stderr), `2` salah pemakaian perintah.

### 6.2 Integrasi pihak ketiga

| Layanan | Untuk apa | Protokol | Kalau mati apa yang terjadi | Data yang dikirim | Risiko |
|---|---|---|---|---|---|
| – (tidak ada) | Sistem berjalan sepenuhnya lokal (NFR-002) | – | – | – | Tidak ada ketergantungan pihak ketiga |

---

## 7. Model otorisasi

| Peran | Bisa melihat | Bisa membuat | Bisa mengubah | Bisa menghapus | Catatan |
|---|---|---|---|---|---|
| Kasir | Daftar produk; rekap harian | Produk baru; transaksi penjualan | Stok (hanya lewat penjualan, tidak bisa minta ubah bebas) | Tidak bisa apa pun | Tidak boleh membatalkan transaksi |
| Pemilik | Semua yang kasir lihat | Produk baru | Membatalkan transaksi (ubah status SELESAI → DIBATALKAN) | Tidak (data transaksi tidak dihapus) | Pemilik ikut menjaga toko, jadi juga bisa memakai semua perintah kasir |

**Keputusan yang diputuskan di sini (menjawab Q-03):** pembatalan transaksi **hanya boleh dilakukan Pemilik**, bukan kasir.

**Alasan:** pembatalan mengembalikan stok dan menghapus nilai transaksi dari rekap. Kalau kasir bisa melakukannya sendiri, ada celah menutupi selisih kas (uang sudah diambil, transaksi lalu dibatalkan). Dengan menaruh hak ini di pemilik, pembatalan yang sah tetap bisa dilakukan (pemilik ada di toko) tetapi tidak bisa dipakai untuk menutupi selisih oleh orang yang memegang kas. Alasannya juga tercatat di [10-decisions.md](10-decisions.md) ADR-004.

Catatan penting: hak akses **ditegakkan di lapisan logika**, bukan hanya dengan menyembunyikan perintah. Perintah `batal` memeriksa peran pemanggil sebelum mengubah status; kalau bukan Pemilik, perintah berhenti dengan kode keluar 1 dan pesan dalam Bahasa Indonesia.

Catatan teknis: karena tidak ada login berbasis password (di luar scope), penegakan peran dilakukan lewat argumen peran pada sesi/terminal yang dikendalikan pemilik. Batas keamanan nyata proyek ini adalah **fisik** (siapa memegang terminal), dan itu dicatat sebagai risiko R-04 di [09-risks.md](09-risks.md).

---

## 8. Struktur folder proyek

```
kasir-berkah/
├── app/
│   ├── __init__.py
│   ├── __main__.py     # CLI: argparse, kode keluar
│   ├── layanan.py      # aturan bisnis BR-001..BR-010
│   ├── data.py         # akses SQLite, transaksi
│   └── schema.sql      # DDL 3 tabel + indeks
├── tests/
│   ├── test_produk.py
│   ├── test_jual.py
│   ├── test_rekap.py
│   └── test_batal.py
├── docs/               # dokumen spec ini
├── README.md
└── kasir.db            # dibuat saat pertama dijalankan (tidak masuk git)
```

Setiap folder punya satu alasan: `app/` kode yang dijalankan, `tests/` bukti, `docs/` spec, `kasir.db` data nyata (di-`gitignore`).

---

## 9. Konfigurasi & rahasia

| Variabel | Kegunaan | Wajib | Nilai contoh (bukan rahasia nyata) | Di mana diisi |
|---|---|---|---|---|
| `KASIR_DB` | Path berkas SQLite | Tidak | `kasir.db` (default di cwd) | Variabel lingkungan saat menjalankan |

Aturan:

- Rahasia **tidak pernah** ditulis di kode atau di dokumen ini.
- Proyek ini tidak menyimpan kredensial apa pun (tidak ada login, tidak ada layanan eksternal).
- `kasir.db` masuk `.gitignore` agar data nyata tidak ikut ke repositori.

---

## 10. Deployment

| Aspek | Isi |
|---|---|
| Lingkungan | Satu lingkungan: perangkat toko (lokal) |
| Cara menjalankan lokal | `python -m app --help` dari akar proyek |
| Cara deploy | Salin folder proyek ke perangkat toko; tidak ada langkah build |
| Di mana di-host | Tidak di-host; dijalankan lokal |
| Migrasi database | Skema dibuat otomatis saat pertama dijalankan; perubahan skema lewat skrip migrasi sederhana |
| Backup | Salin berkas `kasir.db` ke media lain, frekuensi: harian sebelum tutup |
| Rollback | Simpan salinan `kasir.db` sebelum perubahan skema; kembalikan berkas bila gagal |
| Pemantauan | Tidak ada pemantauan otomatis; pesan error ditampilkan ke terminal |

---

## 11. Kebutuhan non-fungsional teknis

| Kebutuhan | Keputusan teknis | Alasan |
|---|---|---|
| Performa (NFR-005) | Operasi tulis kecil dalam satu transaksi SQLite; tanpa jaringan | Perangkat toko sederhana; basis data lokal menghindari latensi jaringan |
| Keandalan (NFR-001) | SQLite ACID; berkas persisten di disk | Data harus tetap ada setelah proses ditutup; tanpa server |
| Kompatibilitas (NFR-002) | Tidak ada panggilan jaringan sama sekali | Koneksi toko tidak stabil |
| Keterpakaian (NFR-003) | Pesan error Bahasa Indonesia menyebut penyebab + tindakan; kode keluar 1 | Kasir bukan orang teknis |
| Auditabilitas (NFR-004) | Nomor `TRX-YYYYMMDD-###` unik berurutan per hari; baris transaksi tidak dihapus | Nota harus bisa dicocokkan saat sengketa |

---

## 12. Keputusan yang sengaja tidak diambil

Teknologi/pendekatan yang sering diusulkan tapi **ditolak** untuk proyek ini. Ini pengaman agar AI tidak menambahkannya seenaknya.

| Ditolak | Kenapa ditolak sekarang | Kapan jadi masuk akal |
|---|---|---|
| Aplikasi web (Flask/Django/React) | Butuh server, browser, dan pemasangan; tidak ada masalah akses dari luar toko | Kalau pemilik butuh melihat dari luar toko dari beberapa lokasi |
| ORM (SQLAlchemy/Django ORM) | 3 tabel; SQL langsung lebih mudah dibaca dan tanpa dependensi (NFR: tanpa pihak ketiga) | Kalau model data tumbuh jauh lebih kompleks |
| Docker / container | Satu proses Python di satu perangkat; container menambah lapisan tanpa manfaat | Kalau ada banyak perangkat dengan lingkungan berbeda |
| Cloud / basis data terpusat | Koneksi toko tidak stabil (NFR-002) dan tidak ada kebutuhan multi-lokasi | Kalau ada multi-cabang dengan data bersama |
| Microservices / message queue | Skala satu toko; tidak ada kebutuhan asinkron | Kalau ada proses berat atau jadwal berjalan terpisah |
| Login berbasis password | Satu perangkat, dua aktor saling percaya; batas keamanan bersifat fisik | Kalau ada kasir tambahan dan data perlu dibatasi per orang |
| Kerangka uji pihak ketiga (pytest) | `unittest` cukup dan sudah di pustaka standar | Kalau kebutuhan uji bertambah melebihi kemampuan `unittest` |
| Pencetakan struk ke printer | Butuh perangkat & driver | Kalau pelanggan menuntut bukti cetak |

---

## 13. Utang teknis & catatan

| # | Catatan | Alasan diambil sekarang | Kapan diperbaiki |
|---|---|---|---|
| 1 | Penegakan peran tanpa login (bertumpu pada batas fisik terminal) | Login di luar scope P0 | Kalau ada kasir tambahan dengan hak berbeda |
| 2 | Migrasi skema masih manual | Skema baru 3 tabel | Sebelum perubahan skema kedua |
| 3 | Belum ada backup otomatis | Tidak ada infrastruktur | Sebelum dipakai produksi penuh |

---

## 14. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |