# 05 — Data Model

> Dokumen ini menjawab: **data apa yang disimpan, bagaimana hubungannya, dan aturan apa yang menjaganya tetap benar.** Setiap entitas harus punya alasan bisnis. Entitas tanpa proses yang memakainya harus dihapus.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

---

## 1. Klasifikasi data

| Jenis | Contoh di proyek ini | Sifat |
|---|---|---|
| Data induk (master) | `products` (SKU, nama, harga, stok) | Berubah jarang (tambah produk, stok berubah karena penjualan), dipakai berulang |
| Data transaksi | `sales` (kepala transaksi), `sale_items` (baris transaksi) | Terus bertambah, tidak boleh diubah sembarangan, tidak dihapus |
| Data referensi | Nilai status transaksi `DRAFT` / `SELESAI` / `DIBATALKAN` | Daftar tetap di dalam kode, bukan pilihan pengguna |
| Dokumen / keluaran | Teks rekap harian yang dicetak ke terminal | Dihasilkan dari data lain; tidak disimpan sebagai tabel |

---

## 2. Daftar entitas

| Entitas | Jenis | Deskripsi satu baris | Pemilik data | Dipakai oleh proses | Perkiraan volume |
|---|---|---|---|---|---|
| `products` | master | Barang yang dijual beserta harga dan stok terkini | Pemilik | PS-01 (catat penjualan), PS-03 (kurangi stok), PS-04 (rekap sisa stok) | Kecil (puluhan–ratusan SKU) `[butuh data jumlah pasti]` |
| `sales` | transaksi | Satu kejadian penjualan: nomor, tanggal, kasir, status, total, bayar, kembalian | Kasir (dibuat), Pemilik (batal) | PS-01, PS-02 (batal), PS-04 (rekap) | Sedang (bertambah tiap transaksi) |
| `sale_items` | transaksi | Baris rincian barang di dalam satu transaksi | Kasir | PS-01 (hitung total & stok), PS-04 (item terjual) | Sedang (1–N per transaksi) |

Ketiga entitas dipakai proses nyata. Tidak ada entitas tambahan: `kategori`, `pemasok`, `pelanggan`, dan `pembayaran` sengaja tidak dibuat karena tidak ada proses P0 yang memakainya.

---

## 3. Detail entitas

Untuk setiap entitas, isi blok berikut. Ulangi sesuai jumlah entitas.

### Entitas: products

**Tujuan bisnis:** Menjadi daftar barang beserta harga tetap dan sisa stok, supaya kasir tidak mengetik harga dan stok selalu bisa diperiksa.
**Dibuat oleh:** Kasir/pemilik lewat `produk tambah`.
**Diubah oleh:** Sistem saat penjualan/batal (mengubah `stok`). Nama dan harga boleh diubah pemilik, tetapi `sku` tidak boleh diubah setelah dipakai transaksi (BR-010).
**Dihapus/diarsipkan:** Tidak dihapus selama masih ada baris transaksi yang memakainya; produk yang tidak dijual lagi cukup dibiarkan dengan stok 0.

| Field | Tipe | Wajib | Unik | Default | Aturan validasi | Keterangan |
|---|---|---|---|---|---|---|
| id | INTEGER | Ya | Ya | auto (rowid) | – | Kunci utama |
| sku | TEXT | Ya | Ya | – | Tidak boleh kosong; tidak boleh diubah setelah dipakai transaksi | Kode barang yang dipakai kasir (`BRS-5KG`) |
| nama | TEXT | Ya | Tidak | – | Tidak boleh kosong | Nama tampilan barang |
| harga | INTEGER | Ya | Tidak | – | Bilangan bulat rupiah ≥ 0 | Harga jual satuan (BR-002) |
| stok | INTEGER | Ya | Tidak | 0 | Bilangan bulat ≥ 0 | Sisa barang; berkurang saat jual, bertambah saat batal (BR-005, BR-008) |
| dibuat_pada | TEXT | Ya | Tidak | waktu sekarang | Format `YYYY-MM-DD HH:MM:SS` | Waktu produk pertama dibuat |

**Aturan pada entitas ini:**

- BR-010: `sku` unik dan tidak boleh diubah setelah dipakai di transaksi.
- BR-005: `stok` tidak boleh negatif; penjualan melebihi stok ditolak sebelum penyimpanan.

**Indeks yang dibutuhkan:**

| Field | Alasan (query yang sering) |
|---|---|
| sku (UNIQUE) | Pencarian produk saat `jual` berdasarkan SKU; sekaligus menegakkan SKU unik |

**Relasi:**

| Ke entitas | Jenis | Aturan | Kalau induk dihapus |
|---|---|---|---|
| sale_items | 1-N | Satu produk bisa muncul di banyak baris transaksi | RESTRICT (produk tidak boleh dihapus bila ada baris transaksi) |

### Entitas: sales

**Tujuan bisnis:** Mencatat setiap kejadian penjualan sebagai satu kesatuan yang bisa dipercaya, bernomor, dan bisa dibatalkan dengan jejak.
**Dibuat oleh:** Sistem saat perintah `jual` disimpan.
**Diubah oleh:** Sistem (mengubah `status`, `alasan_batal`, `dibatalkan_pada` saat `batal`). Pemilik yang memicu pembatalan. `total`, `bayar`, `kembalian`, `kode`, `kasir` terkunci setelah status SELESAI.
**Dihapus/diarsipkan:** Tidak pernah dihapus. Transaksi yang dibatalkan tetap ada dengan status DIBATALKAN.

| Field | Tipe | Wajib | Unik | Default | Aturan validasi | Keterangan |
|---|---|---|---|---|---|---|
| id | INTEGER | Ya | Ya | auto (rowid) | – | Kunci utama |
| kode | TEXT | Ya | Ya | – | Format `TRX-YYYYMMDD-###`, urut per hari (FR-003, NFR-004) | Nomor yang dicocokkan saat sengketa |
| dibuat_pada | TEXT | Ya | Tidak | waktu sekarang | Format `YYYY-MM-DD HH:MM:SS` | Waktu transaksi disimpan |
| status | TEXT | Ya | Tidak | `DRAFT` | Salah satu dari `DRAFT`, `SELESAI`, `DIBATALKAN` | Posisi transaksi di state machine |
| total | INTEGER | Ya | Tidak | – | Bilangan bulat rupiah = Σ subtotal baris (BR-003) | Total belanja |
| bayar | INTEGER | Ya | Tidak | – | Bilangan bulat rupiah ≥ total (BR-004) | Uang yang diserahkan |
| kembalian | INTEGER | Ya | Tidak | – | = bayar − total (BR-004) | Uang kembali |
| kasir | TEXT | Ya | Tidak | – | Tidak boleh kosong | Nama kasir pemroses |
| alasan_batal | TEXT | Tidak | Tidak | NULL | Bila diisi, minimal 5 karakter (BR-007) | Alasan transaksi dibatalkan |
| dibatalkan_pada | TEXT | Tidak | Tidak | NULL | Diisi bersamaan dengan status → DIBATALKAN | Waktu pembatalan |

**Aturan pada entitas ini:**

- BR-004: bayar ≥ total; kembalian = bayar − total.
- BR-006: SELESAI hanya bisa dibatalkan satu kali; DIBATALKAN adalah status akhir.
- BR-007: pembatalan wajib menyertakan alasan minimal 5 karakter.

**Indeks yang dibutuhkan:**

| Field | Alasan (query yang sering) |
|---|---|
| kode (UNIQUE) | Pencarian transaksi saat `batal` dan penomoran urut |
| dibuat_pada / tanggal | Query rekap harian (`rekap --tanggal`) |
| status | Query rekap memfilter status = SELESAI |

**Relasi:**

| Ke entitas | Jenis | Aturan | Kalau induk dihapus |
|---|---|---|---|
| sale_items | 1-N | Satu transaksi punya satu atau lebih baris item | CASCADE hanya bila status masih DRAFT (praktiknya transaksi tidak dihapus) |

### Entitas: sale_items

**Tujuan bisnis:** Menyimpan rincian barang yang terjual di tiap transaksi, beserta harga saat itu, untuk menghitung total dan jumlah item terjual secara konsisten.
**Dibuat oleh:** Sistem saat `jual` disimpan.
**Diubah oleh:** Tidak diubah setelah transaksi tersimpan (harga dan qty terkunci).
**Dihapus/diarsipkan:** Tidak dihapus selama `sales.status` bukan DRAFT, agar riwayat utuh.

| Field | Tipe | Wajib | Unik | Default | Aturan validasi | Keterangan |
|---|---|---|---|---|---|---|
| id | INTEGER | Ya | Ya | auto (rowid) | – | Kunci utama |
| sale_id | INTEGER | Ya | Tidak | – | Harus merujuk `sales.id` yang ada | Transaksi induk |
| product_id | INTEGER | Ya | Tidak | – | Harus merujuk `products.id` yang ada | Produk yang dijual |
| qty | INTEGER | Ya | Tidak | – | Bilangan bulat > 0 (BR-001) | Jumlah terjual |
| harga_satuan | INTEGER | Ya | Tidak | – | Bilangan bulat rupiah; disalin dari `products.harga` saat transaksi dibuat (BR-002) | Riwayat harga terkunci |
| subtotal | INTEGER | Ya | Tidak | – | = qty × harga_satuan (BR-003) | Nilai baris |

**Aturan pada entitas ini:**

- BR-001: qty bilangan bulat > 0.
- BR-002: harga_satuan disalin dari master saat transaksi dibuat, bukan diketik kasir.
- BR-003: subtotal = qty × harga_satuan.
- BR-009: satu transaksi tidak boleh punya dua baris dengan `product_id` yang sama.

**Indeks yang dibutuhkan:**

| Field | Alasan (query yang sering) |
|---|---|
| sale_id | Mengambil seluruh baris milik satu transaksi (rekap & pembatalan) |
| product_id | Mengembalikan stok saat pembatalan dan mengecek riwayat produk |

**Relasi:**

| Ke entitas | Jenis | Aturan | Kalau induk dihapus |
|---|---|---|---|
| sales | N-1 | Setiap baris milik tepat satu transaksi | CASCADE (mengikuti transaksi induk) |
| products | N-1 | Setiap baris merujuk satu produk | RESTRICT (produk yang dipakai tidak boleh dihapus) |

---

## 4. Diagram relasi (ERD)

```
  products ──1:N──▶ sale_items ◀──N:1── sales
      │                                     │
      │                    sales ──1:N──▶ sale_items
      │
      └──(harga disalin ke sale_items.harga_satuan agar riwayat harga tetap)
```

Bentuk yang lebih jelas:

```
  ┌────────────┐            ┌──────────────┐            ┌────────────┐
  │  products  │ 1        N │  sale_items  │ N        1 │   sales    │
  │            │────────────│              │────────────│            │
  │ id (PK)    │            │ id (PK)      │            │ id (PK)    │
  │ sku (UQ)   │            │ sale_id (FK) │            │ kode (UQ)  │
  │ nama       │            │ product_id(FK)            │ status     │
  │ harga      │            │ qty          │            │ total      │
  │ stok       │            │ harga_satuan │            │ bayar      │
  └────────────┘            │ subtotal     │            │ kembalian  │
                            └──────────────┘            └────────────┘
```

Aturan:

- Kardinalitas ditandai jelas: `products 1:N sale_items` dan `sales 1:N sale_items`.
- Tidak ada relasi N:N di proyek ini, jadi tidak ada tabel penghubung tambahan.
- Setiap garis: "satu produk bisa muncul di banyak baris transaksi" dan "satu transaksi punya banyak baris item".

---

## 5. Siklus hidup data

Untuk entitas transaksi, jelaskan perjalanan datanya.

### sales (transaksi)

| Tahap | Apa yang terjadi | Siapa yang bisa melakukan | Data yang berubah |
|---|---|---|---|
| Dibuat (DRAFT) | Baris transaksi dan item disusun, total dihitung | Kasir | `sales.kode`, `dibuat_pada`, `kasir`, `total`, baris `sale_items` |
| Diselesaikan (SELESAI) | Stok dikurangi, transaksi terkunci | Kasir | `sales.status` → SELESAI, `sales.bayar`, `sales.kembalian`, `products.stok` turun |
| Dikunci | Setelah SELESAI, `total`, `bayar`, `kembalian`, `kode`, `kasir`, dan semua `sale_items` tidak bisa diubah | – | Field terkait tidak bisa diubah |
| Dibatalkan (DIBATALKAN) | Status diubah, alasan dicatat, stok dikembalikan | Pemilik | `sales.status` → DIBATALKAN, `alasan_batal`, `dibatalkan_pada`, `products.stok` naik |
| Diarsipkan | Tidak ada arsip terpisah; transaksi lama tetap di tabel yang sama dan difilter per tanggal | – | – |
| Dihapus | Tidak pernah dihapus | – | – |

Aturan umum yang aman: untuk data transaksi, **arsipkan, jangan hapus**. Di proyek ini transaksi dibatalkan tetap disimpan dengan status DIBATALKAN, bukan dihapus, agar jejak audit tetap ada.

### products (stok)

| Tahap | Apa yang terjadi | Siapa yang bisa melakukan | Data yang berubah |
|---|---|---|---|
| Dibuat | Produk baru dengan harga & stok awal | Kasir/pemilik | seluruh field `products` |
| Diubah | `stok` berubah karena penjualan/batal; `nama`/`harga` boleh diubah pemilik | Sistem / Pemilik | `stok`, `nama`, `harga` |
| Dikunci | `sku` terkunci setelah dipakai di transaksi (BR-010) | – | `sku` |
| Diarsipkan | Stok 0 dibiarkan, tidak dihapus | – | – |
| Dihapus | Tidak dihapus selama ada baris transaksi | – | – |

---

## 6. Aturan integritas

| # | Aturan | Ditegakkan di mana | Kalau dilanggar |
|---|---|---|---|
| 1 | Total transaksi = Σ subtotal seluruh barisnya (BR-003) | Aplikasi (dihitung sekali saat `jual`) + transaksi DB | Transaksi tidak disimpan |
| 2 | Stok tidak boleh negatif; jual > stok ditolak (BR-005) | Aplikasi (periksa sebelum tulis) + transaksi DB | Perintah `jual` gagal, kode keluar 1, stok tidak berubah |
| 3 | SKU produk unik (BR-010) | Database `UNIQUE(sku)` | `produk tambah` ditolak dengan pesan SKU sudah dipakai |
| 4 | Kode transaksi unik (FR-003, NFR-004) | Database `UNIQUE(kode)` | Transaksi tidak disimpan; urutan digenerate ulang |
| 5 | Uang bayar ≥ total; kembalian = bayar − total (BR-004) | Aplikasi sebelum menyimpan | `jual` ditolak, kode keluar 1 |
| 6 | Baris transaksi tidak boleh duplikat SKU dalam satu transaksi (BR-009) | Aplikasi sebelum menyimpan | `jual` ditolak, kode keluar 1 |
| 7 | Harga satuan tersalin saat transaksi dibuat, tidak berubah setelahnya (BR-002) | Aplikasi (nilai disalin) | Riwayat harga berubah bila master diubah — dicegah karena salinan |
| 8 | Baris transaksi tidak dihapus setelah status bukan DRAFT | Aplikasi (tidak ada perintah hapus) | Tidak mungkin; tidak ada perintah untuk itu |

Aturan penting: **integritas ditegakkan di database/aplikasi, bukan hanya di tampilan.**

---

## 7. Aturan transisi status

### sales — status

| Status | Arti | Boleh berubah ke | Aktor | Efek samping |
|---|---|---|---|---|
| DRAFT | Transaksi sedang disusun, item ditambahkan | SELESAI | Kasir | Stok belum berubah |
| SELESAI | Transaksi tersimpan; stok sudah dikurangi | DIBATALKAN | Pemilik | Nilai transaksi masuk rekap |
| DIBATALKAN | Transaksi dibatalkan, alasan tercatat | (tidak ada — status akhir) | – | Nilai keluar dari rekap; stok kembali |

Transisi terlarang: `DIBATALKAN → apa pun`, `SELESAI → SELESAI`, `DRAFT → DIBATALKAN`.

### Nilai status (referensi)

| Status | Kode tersimpan | Dipakai di |
|---|---|---|
| DRAFT | `DRAFT` | Perintah `jual` sebelum konfirmasi tersimpan |
| SELESAI | `SELESAI` | Rekap harian (FR-009) |
| DIBATALKAN | `DIBATALKAN` | Rekap harian (dikecualikan) dan perintah `batal` |

---

## 8. Referensi data

| Kode | Nilai | Dipakai di | Bisa ditambah pengguna? |
|---|---|---|---|
| status transaksi | `DRAFT`, `SELESAI`, `DIBATALKAN` | `jual`, `batal`, `rekap` | Tidak (tetap di kode) |
| kode transaksi | `TRX-YYYYMMDD-###` | `jual`, `batal`, `rekap` | Tidak (dibuat sistem) |

---

## 9. Migrasi & data awal

| Hal | Isi |
|---|---|
| Data awal yang wajib ada saat sistem pertama jalan | Tidak ada akun/kategori bawaan. Tabel dibuat kosong; produk pertama diisi lewat `produk tambah`. |
| Data lama yang harus dipindahkan | Tidak ada data lama terstruktur. Nota kertas tidak dipindahkan (lihat [01-prd.md](01-prd.md) batasan Data). |
| Cara memindahkan | Tidak ada. |
| Data lama yang dibuang | Nota & buku stok lama: dibuang sebagai sumber data utama, boleh disimpan fisik sebagai arsip. |
| Cara memeriksa migrasi berhasil | Jalankan `produk daftar`; jumlah produk harus sama dengan yang dimasukkan. `[butuh data jumlah produk awal]` |

---

## 10. Retensi & privasi

| Data | Sensitif? | Berapa lama disimpan | Siapa boleh melihat | Cara menghapus |
|---|---|---|---|---|
| produk, transaksi, baris transaksi | Tidak | Selama toko memakai sistem (tidak dihapus) | Kasir (tanpa batal), Pemilik | Tidak ada penghapusan; pembatalan mengubah status |
| Nama kasir (`sales.kasir`) | Tidak (tidak ada data pribadi di luar nama pemroses) | Sama seperti transaksi | Kasir, Pemilik | Tidak dihapus |
| Data pelanggan | Tidak disimpan | – | – | – |

Data yang biasanya sensitif (identitas pelanggan, nomor telepon, alamat, data pembayaran, kredensial) **tidak dikumpulkan** oleh sistem ini karena di luar scope.

---

## 11. Konsistensi dengan dokumen lain

- [x] Setiap `DR-xx` di `02-requirements.md` ada di sini (DR-001…DR-005)
- [x] Setiap entitas dipakai minimal satu proses di `04-workflow.md` (products→PS-03, sales→PS-02/PS-04, sale_items→PS-01)
- [x] Setiap aturan `BR-xx` yang menyangkut data punya tempat penegakan
- [x] Setiap layar di `06-ui-ux.md` mengambil data dari entitas yang ada di sini

---

## 12. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |