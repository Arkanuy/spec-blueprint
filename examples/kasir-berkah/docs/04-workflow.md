# 04 — Workflow & Proses Bisnis

> Dokumen ini menjawab: **bagaimana pekerjaan berjalan sekarang, bagaimana seharusnya berjalan, dan bagaimana pengguna bergerak di dalam sistem.** Bagian AS-IS menjelaskan kondisi nyata; bagian TO-BE menjelaskan rencana. Jangan mencampur keduanya.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

---

## 1. Daftar proses utama

| # | Proses | Pemicu | Pelaku utama | Frekuensi | Dampak kalau gagal | Prioritas |
|---|---|---|---|---|---|---|
| PS-01 | Catat penjualan & terima pembayaran | Pelanggan membeli barang | Kasir | Tiap transaksi (puluhan per hari `[butuh data]`) | Penjualan tidak tercatat; stok tidak akurat | P0 |
| PS-02 | Batalkan transaksi salah input | Ditemukan salah input / pelanggan batal | Pemilik | Jarang | Laporan menggelembung; stok tidak sesuai | P0 |
| PS-03 | Perbarui stok (kurang saat jual, kembali saat batal) | Selama PS-01 dan PS-02 | Sistem | Tiap transaksi | Stok salah; barang kehabisan atau menumpuk | P0 |
| PS-04 | Rekap penjualan harian | Toko tutup | Pemilik | Harian | Pemilik tidak tahu penjualan & stok | P0 |

---

## 2. Proses AS-IS (kondisi sekarang)

> Aturan: tulis apa adanya. Jangan memasukkan fitur sistem yang belum ada. Kalau sekarang pakai WhatsApp, tulis WhatsApp.

### PS-01 — Catat penjualan & terima pembayaran (AS-IS)

| Langkah | Pelaku | Aktivitas | Masukan | Keluaran | Alat | Waktu | Masalah |
|---|---|---|---|---|---|---|---|
| 1 | Kasir | Menerima permintaan pelanggan | Permintaan lisan | Barang di meja | – | detik | – |
| 2 | Kasir | Menghitung total belanja | Harga tiap barang (ingatan/rak) | Angka total | Kalkulator | puluhan detik | Harga kadang lupa; salah tekan saat ramai |
| 3 | Kasir | Menghitung kembalian | Uang bayar − total | Angka kembalian | Kalkulator | puluhan detik | Pembulatan spontan; selisih menumpuk |
| 4 | Kasir | Menulis nota kertas | Nama barang + qty + total | Nota karbon 2 lembar | Nota + pulpen | puluhan detik | Tulisan tidak terbaca; lembar arsip hilang |
| 5 | Kasir | Mencatat stok terpakai | Ingatan barang terjual | Coretan di buku stok | Buku stok | saat luang | Sering lupa mencatat saat ramai |

**Titik masalah pada proses ini:**

| # | Masalah | Jenis | Dampak |
|---|---|---|---|
| 1 | Total & kembalian dihitung manual dengan kalkulator | kesalahan input | Salah kembalian; selisih kas |
| 2 | Nota ditulis tangan sambil melayani | kesalahan input | Tulisan tidak terbaca; data hilang |
| 3 | Nota disimpan di kertas, tidak ada cadangan | tidak ada kontrol | Lembar hilang; transaksi tidak bisa dibuktikan |
| 4 | Stok dicatat terpisah dari penjualan | input ganda | Stok tidak cocok dengan rak |
| 5 | Harga diandalkan dari ingatan/rak | informasi tersebar | Harga salah disebut |

### PS-04 — Rekap penjualan harian (AS-IS)

| Langkah | Pelaku | Aktivitas | Masukan | Keluaran | Alat | Waktu | Masalah |
|---|---|---|---|---|---|---|---|
| 1 | Pemilik | Mengumpulkan nota hari itu | Tumpukan nota | Tumpukan nota | – | menit | Ada nota yang tidak ketemu |
| 2 | Pemilik | Menjumlah total tiap nota | Angka di nota | Subtotal | Kalkulator | puluhan menit | Nota tidak terbaca; salah tekan |
| 3 | Pemilik | Menghitung jumlah transaksi & item | Tumpukan nota | Angka rekap | Kalkulator + buku | puluhan menit | Sulit dicek ulang |
| 4 | Pemilik | Mencocokkan dengan buku stok | Buku stok + hitungan fisik | Dugaan selisih | Pengamatan | menit | Tidak ketahuan barang mana yang selisih |

**Titik masalah pada proses ini:**

| # | Masalah | Jenis | Dampak |
|---|---|---|---|
| 1 | Penjumlahan nota manual 1–2 jam | pekerjaan manual berulang | Waktu istirahat pemilik habis `(Perlu dikonfirmasi)` |
| 2 | Angka rekap tidak bisa dicek ulang | tidak ada kontrol | Rekap tidak dipercaya |
| 3 | Rekap baru ada malam, bukan kapan saja | keterlambatan | Keputusan belanja telat |
| 4 | Tidak ada data item terjual | informasi tersebar | Sulit tahu barang laku |

---

## 3. Proses TO-BE (kondisi yang diusulkan)

### PS-01 — Catat penjualan & terima pembayaran (TO-BE)

| Langkah | Pelaku | Aktivitas | Masukan | Keluaran | Sistem/alat | Perubahan dari AS-IS | FR terkait |
|---|---|---|---|---|---|---|---|
| 1 | Kasir | Melihat produk & harga | Perintah `produk daftar` | Daftar SKU, nama, harga, stok | Kasir Berkah | Harga tidak lagi dari ingatan | FR-001 |
| 2 | Kasir | Memasukkan penjualan | `jual --produk SKU:QTY ... --bayar ... --kasir ...` | Total & kembalian dihitung sistem | Kasir Berkah | Tidak ada kalkulator; tidak ada hitung manual | FR-002, FR-004, FR-005 |
| 3 | Sistem | Memeriksa stok & bayar | data baris + bayar | Terima/tolak | Kasir Berkah | Pencegahan salah, bukan hanya pemberitahuan | FR-007, BR-004 |
| 4 | Sistem | Menyimpan transaksi, memberi nomor, mengurangi stok | Transaksi valid | `TRX-YYYYMMDD-###`; stok turun | Kasir Berkah | Satu sumber data; stok otomatis | FR-003, FR-006 |
| 5 | Kasir | Menyerahkan kembalian & barang | Kembalian dari sistem | Transaksi selesai | Kasir Berkah | Kembalian pasti | FR-005 |

**Perbaikan yang dicapai:**

| Masalah AS-IS | Diselesaikan oleh | Bagaimana |
|---|---|---|
| Total & kembalian manual (PS-01 #1) | FR-004, FR-005 | Sistem menjumlah baris dan menghitung kembalian |
| Nota tidak terbaca/hilang (PS-01 #2, #3) | FR-002, FR-003 | Transaksi tersimpan di basis data dengan nomor unik |
| Stok dicatat terpisah (PS-01 #4) | FR-006 | Stok berkurang otomatis saat transaksi disimpan |
| Harga dari ingatan (PS-01 #5) | FR-001, BR-002 | Harga diambil dari master produk |

### PS-04 — Rekap penjualan harian (TO-BE)

| Langkah | Pelaku | Aktivitas | Masukan | Keluaran | Sistem/alat | Perubahan dari AS-IS | FR terkait |
|---|---|---|---|---|---|---|---|
| 1 | Pemilik | Menjalankan rekap | `rekap --tanggal YYYY-MM-DD` | Rekap harian | Kasir Berkah | Tidak ada penjumlahan nota | FR-008 |
| 2 | Sistem | Menghitung dari transaksi SELESAI | tanggal | Jumlah transaksi, total penjualan, total item terjual | Kasir Berkah | Angka bisa dicek ulang kapan saja | FR-008, FR-009 |
| 3 | Pemilik | Mencetak/menyalin rekap | keluaran terminal | Catatan rekap | Kasir Berkah | Rekap instan, bukan setelah 1–2 jam | FR-008 |

**Perbaikan yang dicapai:**

| Masalah AS-IS | Diselesaikan oleh | Bagaimana |
|---|---|---|
| Rekap manual 1–2 jam (PS-04 #1) | FR-008, FR-009 | Rekap dihitung sistem dari data tersimpan |
| Angka rekap tidak bisa dicek (PS-04 #2) | FR-009 | Rekap konsisten dari transaksi SELESAI yang sama |
| Rekap hanya malam (PS-04 #3) | FR-008 | Rekap tersedia kapan saja untuk tanggal yang ada |
| Tidak ada data item terjual (PS-04 #4) | FR-008 | Rekap menampilkan total item terjual dari `sale_items` |

### PS-02 — Batalkan transaksi salah input (TO-BE)

| Langkah | Pelaku | Aktivitas | Masukan | Keluaran | Sistem/alat | Perubahan dari AS-IS | FR terkait |
|---|---|---|---|---|---|---|---|
| 1 | Pemilik | Menemukan transaksi salah & menjalankan batal | `batal --kode TRX-... --alasan "..."` | Status DIBATALKAN | Kasir Berkah | Sebelumnya tidak ada cara menganulir | FR-010 |
| 2 | Sistem | Memeriksa status & alasan | kode + alasan | Terima/tolak | Kasir Berkah | Pembatalan kedua & alasan pendek ditolak | FR-012, BR-006, BR-007 |
| 3 | Sistem | Mengembalikan stok | baris transaksi | Stok naik kembali | Kasir Berkah | Sebelumnya stok manual, sering lupa | FR-011 |

**Perbaikan yang dicapai:**

| Masalah AS-IS | Diselesaikan oleh | Bagaimana |
|---|---|---|
| Salah input tidak bisa dianulir | FR-010, FR-012 | Transaksi SELESAI bisa dibatalkan sekali dengan alasan |
| Stok tidak kembali saat barang dikembalikan | FR-011 | Stok dikembalikan sebesar qty baris |
| Laporan menggelembung | FR-009 | Transaksi DIBATALKAN tidak dihitung di rekap |

Aturan verifikasi: setiap masalah di AS-IS sudah punya penyelesaian di TO-BE. Tidak ada masalah yang dibiarkan tanpa penyelesaian di lingkup P0.

---

## 4. Diagram alur proses

Gambarkan proses utama. Bisa pakai BPMN, activity diagram, atau flowchart sederhana. Yang penting: setiap aktivitas bisa dipetakan ke aktor, masukan, dan keluaran.

```
Alur PS-01 (TO-BE): Kasir mencatat penjualan

[Mulai]
   │
   ▼
[Kasir: lihat produk (produk daftar)]
   │
   ▼
[Kasir: masukkan SKU:QTY + bayar]
   │
   ▼
<Sistem: qty > 0, tidak duplikat SKU, stok cukup?>
   │ salah                       │ benar
   ▼                             ▼
[Sistem: tolak, kode 1]   <Bayar ≥ total?>
   │                             │ tidak          │ ya
   ▼                             ▼                ▼
[Selesai]              [Sistem: tolak]   [Sistem: simpan, beri nomor,
                                         kurangi stok, hitung kembalian]
                                                  │
                                                  ▼
                                         [Kasir: serahkan kembalian]
                                                  │
                                                  ▼
                                             [Selesai]
```

```
Alur PS-04 & PS-02 (TO-BE): Rekap dan pembatalan

[Pemilik: rekap --tanggal T] ──▶ [Sistem: ambil transaksi SELESAI di T]
                                        │
                                        ▼
                              [Tampilkan 3 angka rekap] ──▶ [Selesai]

[Pemilik: batal --kode K --alasan A] ──▶ <Status SELESAI & alasan ≥5?>
                                             │ tidak        │ ya
                                             ▼              ▼
                                   [Tolak, kode 1]   [Ubah DIBATALKAN,
                                    ──▶ [Selesai]     kembalikan stok]
                                                            │
                                                            ▼
                                                     [Konfirmasi + stok]
                                                            │
                                                            ▼
                                                        [Selesai]
```

### 4.1 Aturan pembuatan diagram

- Nama aktivitas pakai **kata kerja + objek** (contoh: "Simpan transaksi", bukan "Transaksi").
- Setiap cabang keputusan punya kondisi tertulis di garis ("qty > 0", "bayar ≥ total").
- Komponen teknis (basis data) tidak digambar sebagai aktor manusia.
- Tidak ada proses paralel di lingkup P0.

---

## 5. Alur pengguna di sistem (user flow)

Alur ini menjelaskan langkah di dalam aplikasi, berbeda dari proses bisnis di atas.

### UF-01 — Catat penjualan — Kasir

| Langkah | Aksi pengguna | Respons sistem | Layar/Perintah | Kondisi |
|---|---|---|---|---|
| 1 | Mengetik `produk daftar` | Menampilkan daftar produk + stok | Terminal | Ada produk terdaftar |
| 2 | Mengetik `jual --produk BRS-5KG:2 --bayar 150000 --kasir "Nadia"` | Menghitung total, memeriksa stok & bayar | Terminal | Produk ada, stok cukup |
| 3 | Membaca kembalian | Menampilkan kode transaksi, total, kembalian | Terminal | Transaksi tersimpan |
| 4 | Menyerahkan barang & kembalian | – | – | – |

**Kondisi awal:** Ada minimal satu produk terdaftar; perangkat menyala.
**Kondisi akhir:** Transaksi tersimpan berstatus SELESAI; stok berkurang.
**Alur alternatif:** Beberapa baris barang dalam satu perintah (`--produk` berulang).
**Alur error:** SKU tidak ada → pesan + kode 1; qty ≤ 0 → pesan + kode 1; stok kurang → pesan menyebut stok tersedia + kode 1; bayar kurang → pesan menyebut selisih + kode 1; SKU duplikat dalam satu perintah → pesan + kode 1.

### UF-02 — Rekap harian — Pemilik

| Langkah | Aksi pengguna | Respons sistem | Layar/Perintah | Kondisi |
|---|---|---|---|---|
| 1 | Mengetik `rekap --tanggal 2026-10-03` | Menghitung dari transaksi SELESAI | Terminal | Format tanggal benar |
| 2 | Membaca jumlah transaksi, total penjualan, total item | Menampilkan tiga angka | Terminal | – |

**Kondisi awal:** Setidaknya sudah pernah ada transaksi pada tanggal itu (kalau tidak, rekap kosong).
**Kondisi akhir:** Pemilik memiliki angka rekap yang bisa dipertanggungjawabkan.
**Alur alternatif:** Tanggal dengan transaksi yang sebagian dibatalkan → hanya SELESAI dihitung.
**Alur error:** Format tanggal salah → pesan + kode 1; tanggal tanpa transaksi → menampilkan rekap nol (bukan error).

### UF-03 — Batal transaksi — Pemilik

| Langkah | Aksi pengguna | Respons sistem | Layar/Perintah | Kondisi |
|---|---|---|---|---|
| 1 | Mengetik `batal --kode TRX-20261003-001 --alasan "salah input"` | Memeriksa status & alasan | Terminal | Transaksi SELESAI |
| 2 | Membaca konfirmasi | Menampilkan status DIBATALKAN + stok yang dikembalikan | Terminal | Transaksi berhasil dibatalkan |

**Kondisi awal:** Transaksi berstatus SELESAI dan belum pernah dibatalkan.
**Kondisi akhir:** Status DIBATALKAN; stok kembali; transaksi keluar dari rekap.
**Alur alternatif:** Alasan lebih panjang dari 5 karakter tetap diterima.
**Alur error:** Alasan < 5 karakter → pesan + kode 1; sudah DIBATALKAN → pesan + kode 1; kode tidak ditemukan → pesan + kode 1.

---

## 6. Alur status (state flow)

Untuk setiap entitas yang punya siklus hidup (pesanan, pengajuan, pembayaran, tiket).

### Entitas: sales (transaksi)

| Dari | Ke | Pemicu | Syarat | Peran yang boleh | Efek samping |
|---|---|---|---|---|---|
| DRAFT | SELESAI | Perintah `jual` disimpan | Semua baris valid (BR-001, BR-009), stok cukup (BR-005), bayar ≥ total (BR-004) | Kasir | Stok tiap produk turun sebesar qty; kode transaksi dibuat; masuk rekap |
| SELESAI | DIBATALKAN | Perintah `batal` | Alasan ≥ 5 karakter (BR-007); belum pernah dibatalkan (BR-006) | Pemilik | Status berubah; `alasan_batal` & `dibatalkan_pada` diisi; stok tiap produk naik kembali; keluar dari rekap |
| DIBATALKAN | – | Tidak ada | – | – | Status akhir; tidak boleh berubah lagi |

**Status boleh masuk / boleh keluar:**

| Status | Boleh masuk dari | Boleh keluar ke | Syarat masuk |
|---|---|---|---|
| DRAFT | – (status awal transaksi) | SELESAI | Transaksi dibuat, item ditambahkan |
| SELESAI | DRAFT | DIBATALKAN | Stok tersedia, bayar ≥ total, tersimpan |
| DIBATALKAN | SELESAI | (akhir) | Alasan ≥ 5 karakter, stok dikembalikan |

Transisi terlarang: `DIBATALKAN → apa pun`, `SELESAI → SELESAI`, `DRAFT → DIBATALKAN`.

```
        jual (valid)                 batal (alasan ≥5, sekali)
[DRAFT] ───────────▶ [SELESAI] ─────────────────────▶ [DIBATALKAN]
   │                     │                                   │
   │                     │ (tidak bisa SELESAI lagi)          │ status akhir
   ▼                     ▼                                   ▼
 gagal              tidak boleh balik                  (tidak berubah)
```

Aturan: setiap status punya jalur masuk dan jalur keluar, kecuali status akhir (DIBATALKAN) yang memang tidak punya jalur keluar.

---

## 7. Alur data (dari sisi proses)

| Langkah proses | Data dibuat | Data diubah | Data dibaca | Data dihapus/diarsipkan |
|---|---|---|---|---|
| produk tambah | products.* | – | – | – |
| jual (PS-01) | sales.*, sale_items.* | products.stok | products.harga, products.stok | – |
| rekap (PS-04) | – (keluaran tidak disimpan) | – | sales.status, sales.total, sale_items.qty | – |
| batal (PS-02) | – | sales.status, sales.alasan_batal, sales.dibatalkan_pada, products.stok | sales.status, sale_items.qty, sale_items.product_id | – (tidak ada penghapusan) |

Berguna untuk memastikan: setiap data yang dibuat benar-benar dipakai, dan setiap data yang dibaca benar-benar pernah dibuat.

---

## 8. Aturan dan pengecualian

### 8.1 Aturan yang mengikat proses

| # | Aturan | Berlaku untuk | Kalau dilanggar |
|---|---|---|---|
| 1 | BR-001 (qty bilangan bulat > 0) | PS-01 langkah 2 | Transaksi ditolak, kode keluar 1 |
| 2 | BR-002 (harga dari master) | PS-01 langkah 2 | Kasir tidak bisa mengetik harga; sistem memakai master |
| 3 | BR-004 (bayar ≥ total) | PS-01 langkah 3 | Transaksi ditolak, selisih disebut |
| 4 | BR-005 (tidak jual melebihi stok) | PS-01 langkah 3 & 4 | Transaksi ditolak, stok tersedia disebut |
| 5 | BR-006 (batal sekali) | PS-02 langkah 2 | Pembatalan kedua ditolak |
| 6 | BR-007 (alasan ≥ 5 karakter) | PS-02 langkah 2 | Pembatalan ditolak |
| 7 | BR-009 (satu SKU satu baris) | PS-01 langkah 2 | Transaksi ditolak |
| 8 | BR-010 (SKU unik) | produk tambah | Produk baru ditolak |

### 8.2 Pengecualian (exception)

Kondisi tidak normal yang harus tetap punya jalur penyelesaian. Bukan "di luar tanggung jawab".

| # | Kondisi tidak normal | Bagaimana ditangani | Siapa yang menangani | FR terkait |
|---|---|---|---|---|
| EX-01 | Pelanggan membatalkan setelah bayar | Pemilik membatalkan transaksi dengan alasan; stok dikembalikan; transaksi keluar dari rekap | Pemilik | FR-010, FR-011 |
| EX-02 | Salah input qty/harga pada transaksi tersimpan | Batal lalu input ulang transaksi baru | Pemilik | FR-010 |
| EX-03 | Stok di sistem tidak cocok dengan rak | Ditemukan lewat rekap; ditangani di luar sistem sekarang (penyesuaian manual belum ada) | Pemilik | – (dicatat di 09-risks.md R-05) |
| EX-04 | Perangkat mati saat menyimpan | SQLite transaksional: transaksi tersimpan utuh atau tidak sama sekali; kasir mengulang | Kasir | FR-002, FR-006 |
| EX-05 | Pembatalan kedua atas transaksi yang sama | Ditolak dengan pesan jelas, kode keluar 1 | Pemilik | FR-012 |
| EX-06 | Alasan pembatalan terlalu pendek | Ditolak sebelum menyimpan | Pemilik | FR-010, BR-007 |
| EX-07 | Produk belum ada saat mau dijual | Kasir menambah produk dulu via `produk tambah` | Kasir | FR-001 |
| EX-08 | Tanggal rekap tanpa transaksi | Menampilkan rekap nol, bukan error | Pemilik | FR-008 |

Aturan: setiap pengecualian punya jalur penyelesaian yang bisa dijalankan orang di toko, atau dicatat eksplisit sebagai risiko bila belum bisa ditangani sekarang (EX-03).

---

## 9. Perbandingan AS-IS vs TO-BE

| Aspek | AS-IS | TO-BE | Perbaikan |
|---|---|---|---|
| Jumlah langkah | 5 langkah (hitung, hitung, tulis nota, catat stok) | 4 langkah (lihat produk, input jual, sistem simpan, serahkan) | Berkurang; hitung manual hilang |
| Waktu proses | puluhan detik hitung + tulis nota per transaksi; 1–2 jam rekap malam | detik per transaksi; rekap < 1 menit | Jauh lebih cepat untuk rekap |
| Input ganda | Ada (nota + buku stok) | Tidak (satu input, stok otomatis) | Perbaikan |
| Titik verifikasi | 1 (pemilik mencocokkan nota malam) | 2 (sistem tolak input salah + pemilik bisa cek rekap kapan saja) | Perbaikan |
| Ketersediaan informasi | Hanya saat nota dibawa | Kapan saja untuk tanggal yang ada | Perbaikan |
| Jejak audit | Tidak ada (nota bisa hilang) | Ada (transaksi tersimpan + alasan batal) | Perbaikan |

Catatan: TO-BE tidak menambah langkah bagi kasir; justru mengurangi (tidak ada tulis nota dan catat stok manual).

---

## 10. Perubahan pada manusia & organisasi

Perubahan sistem mengubah cara kerja orang. Bagian ini mencegah sistem bagus tapi tidak dipakai.

| Peran | Yang berubah | Pelatihan/kebiasaan baru yang dibutuhkan | Risiko penolakan | Cara mengatasinya |
|---|---|---|---|---|
| Kasir | Tidak lagi menulis nota atau mengingat harga; mengetik perintah `jual` dan membaca kembalian dari layar | Cara mengetik SKU:QTY, membaca pesan error, kembali ke prosedur bila sistem menolak | Sedang (takut salah ketik, terutama saat ramai) | Pelatihan singkat 1 jam dengan 5 transaksi contoh; pesan error Bahasa Indonesia; sistem mencegah salah, bukan menghukum |
| Pemilik | Rekap dijalankan sendiri, bukan dihitung manual malam; memegang hak pembatalan | Menjalankan `rekap`, memutuskan kapan `batal`, mencadangkan `kasir.db` harian | Rendah (pemilik yang meminta perbaikan) | Tunjukkan rekap instan dibanding waktu rekap manual; sederhanakan backup jadi menyalin satu berkas |
| Kasir | Kehilangan kebebasan mencatat stok di buku | Memahami stok kini otomatis dari penjualan | Rendah–sedang | Tegaskan stok tidak perlu dihitung lagi; sediakan cara melapor bila rak tidak cocok |
| Pemasok | Menerima pesanan yang didasari angka stok, bukan pengamatan | Tidak ada (di luar sistem) | Rendah | – |

Aturan: kalau kasir merasa sistem lebih lambat dari menulis nota, sistem akan ditinggalkan (dicatat sebagai R-01 di [09-risks.md](09-risks.md)).

---

## 11. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |