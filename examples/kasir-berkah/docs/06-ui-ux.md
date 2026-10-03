# 06 — UI/UX

> Dokumen ini menjawab: **apa yang dilihat pengguna, apa yang bisa dia lakukan, dan apa yang terjadi saat sesuatu gagal.** Bagian yang paling sering dilupakan di dokumen lain — dan paling sering ditebak salah oleh AI — adalah kondisi kosong, kondisi memuat, dan kondisi error. Di sini wajib ditulis.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

---

## 1. Prinsip desain

Batasi 4–6 prinsip. Prinsip di sini yang dipakai untuk menilai semua keputusan tampilan.

| # | Prinsip | Konsekuensi praktis |
|---|---|---|
| D-1 | Tugas utama selesai dengan langkah paling sedikit | Kasir mencatat penjualan dengan satu perintah `jual`; tidak ada menu bertingkat |
| D-2 | Kesalahan dicegah, bukan hanya diberitahu | Harga diambil sistem (kasir tidak bisa mengetik harga); stok diperiksa sebelum simpan |
| D-3 | Status selalu jelas | Setiap keluaran menyebut status (produk tersimpan, transaksi SELESAI, transaksi DIBATALKAN) |
| D-4 | Bahasa manusia, bukan bahasa teknis | Pesan error Bahasa Indonesia menyebut penyebab + tindakan; kode keluar hanya pelengkap |
| D-5 | Uang dan tanggal selalu format yang sama | Uang `Rp1.234.567`; tanggal `YYYY-MM-DD` |

---

## 2. Konteks pemakaian

| Aspek | Isi | Implikasi desain |
|---|---|---|
| Perangkat utama | Komputer/laptop toko dengan terminal | Teks monospasi, kolom rata, tidak perlu grafis |
| Tempat pemakaian | Meja kasir, kadang dilihat pelanggan | Teks harus bisa dibaca cepat; jangan tampilkan data sensitif |
| Tingkat ketergesaan | Tinggi saat jam sibuk | Perintah pendek; pesan singkat; tidak ada konfirmasi berlebihan |
| Kualitas jaringan | Tidak relevan (sistem lokal, NFR-002) | Tidak ada indikator koneksi |
| Kemampuan pengguna | Rendah (kasir), menengah (pemilik) | Bantuan `--help` jelas; pesan error menuntun langkah berikutnya |

---

## 3. Daftar layar

Untuk proyek CLI, "layar" adalah satu perintah beserta keluarannya.

Perintah yang tersedia (sama persis dengan kontrak di [03-architecture.md](03-architecture.md) bagian 6.1):

```
python -m app produk tambah --sku SKU --nama "Nama" --harga 3500 --stok 40
python -m app produk daftar
python -m app jual --produk SKU:QTY [--produk SKU:QTY ...] --bayar 50000 --kasir "Nadia"
python -m app rekap --tanggal 2026-10-03
python -m app batal --kode TRX-20261003-001 --alasan "salah input"
```

Kode keluar (exit code): `0` berhasil, `1` kesalahan aturan bisnis (pesan jelas ke stderr), `2` salah pemakaian perintah.

| ID | Layar (perintah) | Tujuan | Persona | Data yang ditampilkan | Aksi utama | FR terkait | Prioritas |
|---|---|---|---|---|---|---|---|
| S-01 | `produk daftar` | Melihat produk, harga, dan stok | Kasir | SKU, nama, harga, stok | – | FR-001 | P0 |
| S-02 | `produk tambah` | Menambah produk baru | Kasir | Konfirmasi produk tersimpan | Simpan produk | FR-001, BR-010 | P0 |
| S-03 | `jual` | Mencatat penjualan & menerima bayar | Kasir | Kode transaksi, total, kembalian | Simpan transaksi | FR-002…FR-007 | P0 |
| S-04 | `rekap` | Melihat rekap harian | Pemilik | Jumlah transaksi, total penjualan, total item terjual | – | FR-008, FR-009 | P0 |
| S-05 | `batal` | Membatalkan transaksi salah input | Pemilik | Status DIBATALKAN, stok kembali | Batalkan transaksi | FR-010…FR-012 | P0 |
| S-06 | `--help` | Melihat daftar perintah | Kasir, Pemilik | Daftar perintah & contoh | – | – | P1 |

---

## 4. Detail layar

Ulangi blok berikut untuk setiap layar prioritas. Layar P0 wajib lengkap.

### S-01 — Daftar produk (`python -m app produk daftar`)

**Tujuan:** Kasir melihat SKU, nama, harga, dan stok sebelum mencatat penjualan.
**Masuk dari:** terminal (tidak ada menu sebelumnya).
**Keluar ke:** S-02 (kalau produk belum ada) atau S-03 (mencatat jual).

**Tata letak:**

| Area | Isi | Fungsi |
|---|---|---|
| Judul | `Daftar Produk` | Menandai keluaran |
| Utama | Satu baris per produk: `SKU  Nama  Harga  Stok` | Pilihan untuk perintah `jual` |
| Bawah | `Total: N produk` atau pesan kosong | Ringkasan |

**Elemen interaktif:**

| Elemen | Jenis | Aksi | Validasi | Kondisi aktif/nonaktif |
|---|---|---|---|---|
| `--help` | opsi | Menampilkan cara pakai | – | Selalu |

**Status layar yang WAJIB ditangani:**

| Status | Kapan terjadi | Yang ditampilkan | Ada aksi pemulihan? |
|---|---|---|---|
| Memuat | Saat data dibaca dari SQLite | Tidak ada indikator khusus (operasi lokal, < 1 detik) | – |
| Kosong | Belum ada produk sama sekali | `Belum ada produk. Tambah produk dulu dengan: python -m app produk tambah --sku ... --nama "..." --harga ... --stok ...` | Ya: jalankan `produk tambah` |
| Kosong karena filter | Tidak berlaku (perintah ini tidak punya filter) | – | – |
| Berhasil | Produk ditemukan | Daftar produk + `Total: N produk` | – |
| Gagal validasi | Tidak berlaku (tanpa masukan) | – | – |
| Gagal sistem | Berkas basis data tidak bisa dibuka | `Gagal membaca basis data: <nama berkas>. Periksa apakah berkas ada dan bisa ditulis.` | Ya: periksa path `KASIR_DB` |
| Tidak punya akses | Tidak berlaku (semua peran boleh melihat) | – | – |
| Data besar | Produk > 30 | Daftar tetap dicetak semua; pemilik dapat mempersempit dengan mencari SKU (belum ada di P0) | – |

**Aturan tampilan:**

- Harga selalu `Rp` + titik ribuan (`Rp6.500`), bukan `6500`.
- Stok selalu bilangan bulat tanpa desimal.
- Jangan menampilkan catatan internal/margin laba (tidak ada di sistem ini).

### S-02 — Tambah produk (`python -m app produk tambah ...`)

**Tujuan:** Mendaftarkan produk baru beserta harga dan stok awal.
**Masuk dari:** terminal.
**Keluar ke:** S-01 (verifikasi) atau S-03.

**Tata letak:**

| Area | Isi | Fungsi |
|---|---|---|
| Judul | `Tambah Produk` | Menandai aksi |
| Utama | Konfirmasi: `Produk ditambahkan: <SKU> — <Nama> (Rp<harga>, stok <n>)` | Bukti tersimpan |
| Samping | – | – |

**Elemen interaktif:**

| Elemen | Jenis | Aksi | Validasi | Kondisi aktif/nonaktif |
|---|---|---|---|---|
| `--sku` | argumen | Menentukan kode barang | Wajib; unik (BR-010) | – |
| `--nama` | argumen | Nama barang | Wajib; tidak kosong | – |
| `--harga` | argumen | Harga jual | Bilangan bulat ≥ 0 | – |
| `--stok` | argumen | Stok awal | Bilangan bulat ≥ 0 | – |

**Status layar yang WAJIB ditangani:**

| Status | Kapan terjadi | Yang ditampilkan | Ada aksi pemulihan? |
|---|---|---|---|
| Memuat | Saat menulis ke SQLite | Tidak ada indikator khusus | – |
| Kosong | Tidak berlaku | – | – |
| Kosong karena filter | Tidak berlaku | – | – |
| Berhasil | Produk tersimpan | `Produk ditambahkan: <SKU> — <Nama> (Rp<harga>, stok <n>)` | – |
| Gagal validasi | SKU sudah ada; harga/stok negatif; nama kosong | `Gagal: SKU '<sku>' sudah dipakai. Pakai SKU lain.` / `Gagal: harga harus bilangan bulat ≥ 0.` / `Gagal: nama produk tidak boleh kosong.` (kode keluar 1) | Ya: perbaiki argumen |
| Gagal sistem | Berkas basis data tidak bisa ditulis | `Gagal menyimpan produk: <alasan>. Coba lagi; bila berulang, periksa izin tulis folder.` | Ya: coba lagi |
| Tidak punya akses | SKU diketik saat peran bukan yang diizinkan mengubah master | `Gagal: hanya pemilik/kasir yang boleh menambah produk.` | Ya: minta pemilik |
| Data besar | Tidak berlaku | – | – |

**Aturan tampilan:**

- Pesan gagal menyebut nilai yang bermasalah (mis. SKU yang bentrok), bukan hanya "input salah".
- Konfirmasi berhasil menyebut SKU agar kasir yakin produk yang benar tersimpan.

### S-03 — Jual (`python -m app jual ...`)

**Tujuan:** Mencatat penjualan, menghitung total dan kembalian, mengurangi stok.
**Masuk dari:** S-01.
**Keluar ke:** S-01 (transaksi berikutnya) atau S-04 (pemilik melihat dampaknya).

**Tata letak:**

| Area | Isi | Fungsi |
|---|---|---|
| Judul | `Transaksi` | Menandai keluaran |
| Utama | Rincian per baris: `SKU  Nama  qty × Rp<harga>  = Rp<subtotal>`; lalu `Total`, `Bayar`, `Kembalian`; `Status: SELESAI`; `Kode: TRX-YYYYMMDD-###` | Bukti transaksi |
| Bawah | `Kasir: <nama>` | Jejak siapa memproses |

**Elemen interaktif:**

| Elemen | Jenis | Aksi | Validasi | Kondisi aktif/nonaktif |
|---|---|---|---|---|
| `--produk SKU:QTY` | argumen (bisa diulang) | Menambah baris item | SKU ada; qty bulat > 0; tidak duplikat SKU | – |
| `--bayar` | argumen | Uang diserahkan | Bilangan bulat ≥ total (BR-004) | – |
| `--kasir` | argumen | Nama kasir | Wajib; tidak kosong | – |

**Status layar yang WAJIB ditangani:**

| Status | Kapan terjadi | Yang ditampilkan | Ada aksi pemulihan? |
|---|---|---|---|
| Memuat | Saat menulis transaksi (transaksi SQLite) | Tidak ada indikator khusus; operasi < 1 detik (NFR-005) | – |
| Kosong | Belum ada produk terdaftar | `Belum ada produk. Tambah produk dulu sebelum mencatat penjualan.` | Ya: jalankan `produk tambah` |
| Kosong karena filter | SKU yang diminta tidak ada | `Gagal: produk dengan SKU '<sku>' tidak ditemukan. Jalankan 'produk daftar' untuk melihat SKU yang tersedia.` | Ya: perbaiki SKU |
| Berhasil | Transaksi valid tersimpan | Rincian + `Total` + `Kembalian` + `Status: SELESAI` + `Kode: TRX-...` | – |
| Gagal validasi | qty ≤ 0, qty bukan bulat, qty melebihi stok, bayar < total, SKU duplikat, `--kasir` kosong | `Gagal: qty untuk <SKU> harus bilangan bulat lebih dari 0.` / `Gagal: stok <SKU> tinggal <n>, tidak cukup untuk <qty>.` / `Gagal: uang bayar Rp<x> kurang Rp<y> dari total Rp<z>.` / `Gagal: SKU '<sku>' muncul lebih dari sekali dalam satu transaksi.` (kode keluar 1) | Ya: perbaiki argumen |
| Gagal sistem | Transaksi SQLite gagal di tengah jalan | `Gagal menyimpan transaksi: <alasan>. Transaksi tidak tersimpan, stok tidak berubah. Coba lagi.` | Ya: coba lagi |
| Tidak punya akses | Tidak berlaku (kasir & pemilik boleh menjual) | – | – |
| Data besar | Banyak baris dalam satu transaksi | Semua baris dicetak sebelum total | – |

**Aturan tampilan:**

- Semua nilai uang memakai `Rp1.234.567` (titik ribuan, tanpa desimal).
- Total dan kembalian selalu tampil berdampingan agar mudah diperiksa.
- Saat ditolak, tidak ada satu pun baris yang tersimpan dan stok tidak berubah (semua-atau-tidak-sama-sekali).
- Tombol/aksi tidak minta konfirmasi berlebihan; sistem cukup menolak yang salah dan menerima yang benar.

### S-04 — Rekap (`python -m app rekap --tanggal YYYY-MM-DD`)

**Tujuan:** Pemilik melihat jumlah transaksi, total penjualan, dan total item terjual pada satu tanggal.
**Masuk dari:** terminal.
**Keluar ke:** terminal (pemilik menyalin/mencetak keluarannya).

**Tata letak:**

| Area | Isi | Fungsi |
|---|---|---|
| Judul | `Rekap Harian — <YYYY-MM-DD>` | Menandai tanggal yang diminta |
| Utama | `Jumlah transaksi: N` / `Total penjualan: Rp...` / `Total item terjual: N` | Angka rekap |
| Bawah | `(Hanya transaksi SELESAI yang dihitung)` | Menjelaskan cakupan |

**Elemen interaktif:**

| Elemen | Jenis | Aksi | Validasi | Kondisi aktif/nonaktif |
|---|---|---|---|---|
| `--tanggal` | argumen | Menentukan tanggal | Format `YYYY-MM-DD`; tanggal valid | – |

**Status layar yang WAJIB ditangani:**

| Status | Kapan terjadi | Yang ditampilkan | Ada aksi pemulihan? |
|---|---|---|---|
| Memuat | Saat menjumlah dari SQLite | Tidak ada indikator khusus | – |
| Kosong | Belum ada transaksi sama sekali di sistem | `Belum ada transaksi sama sekali di sistem.` | Ya: catat penjualan dulu |
| Kosong karena filter | Tanggal yang diminta tidak punya transaksi | `Rekap 2026-10-04: tidak ada transaksi pada tanggal ini.` dengan angka nol | Ya: cek tanggal atau ganti tanggal |
| Berhasil | Ada transaksi SELESAI pada tanggal itu | Tiga angka rekap | – |
| Gagal validasi | Format tanggal salah (mis. `03-10-2026`) | `Gagal: format tanggal harus YYYY-MM-DD. Contoh: 2026-10-03.` (kode keluar 1) | Ya: perbaiki format |
| Gagal sistem | Basis data tidak bisa dibaca | `Gagal membaca basis data: <alasan>. Periksa berkas kasir.db.` | Ya: periksa berkas |
| Tidak punya akses | Peran bukan pemilik/kasir | `Gagal: perintah rekap hanya untuk pemilik atau kasir.` | Ya: minta pemilik |
| Data besar | Banyak transaksi | Semua dijumlahkan, bukan ditampilkan per transaksi | – |

**Aturan tampilan:**

- Rekap kosong karena filter **bukan error**; tampilkan angka nol dengan kalimat netral.
- Total penjualan memakai format `Rp1.234.567`.
- Selalu sebutkan bahwa hanya transaksi SELESAI dihitung, agar pemilik tidak bertanya kenapa transaksi yang dibatalkan hilang.

### S-05 — Batal (`python -m app batal --kode TRX-... --alasan "..."`)

**Tujuan:** Membatalkan transaksi salah input, mengembalikan stok, dan mengeluarkannya dari rekap.
**Masuk dari:** terminal.
**Keluar ke:** S-04 (verifikasi rekap turun).

**Tata letak:**

| Area | Isi | Fungsi |
|---|---|---|
| Judul | `Batal Transaksi` | Menandai aksi berisiko |
| Utama | `Transaksi <kode> dibatalkan.` / `Alasan: <alasan>` / `Stok dikembalikan: <SKU> +<qty>, ...` | Bukti pembatalan |
| Bawah | `Status: DIBATALKAN` | Status akhir |

**Elemen interaktif:**

| Elemen | Jenis | Aksi | Validasi | Kondisi aktif/nonaktif |
|---|---|---|---|---|
| `--kode` | argumen | Menentukan transaksi | Wajib; harus ada; berformat `TRX-YYYYMMDD-###` | Hanya berlaku untuk transaksi SELESAI |
| `--alasan` | argumen | Alasan pembatalan | Wajib; ≥ 5 karakter (BR-007) | – |

**Status layar yang WAJIB ditangani:**

| Status | Kapan terjadi | Yang ditampilkan | Ada aksi pemulihan? |
|---|---|---|---|
| Memuat | Saat mengubah status & stok | Tidak ada indikator khusus | – |
| Kosong | Tidak berlaku | – | – |
| Kosong karena filter | Kode transaksi tidak ditemukan | `Gagal: transaksi dengan kode '<kode>' tidak ditemukan.` | Ya: cek kode lewat rekap |
| Berhasil | Transaksi SELESAI berhasil dibatalkan | Konfirmasi + daftar stok yang dikembalikan + `Status: DIBATALKAN` | – |
| Gagal validasi | Alasan < 5 karakter | `Gagal: alasan pembatalan minimal 5 karakter. Jelaskan singkat kenapa dibatalkan.` (kode keluar 1) | Ya: tulis alasan lebih panjang |
| Gagal validasi | Transaksi sudah DIBATALKAN | `Gagal: transaksi <kode> sudah dibatalkan pada <tanggal>. Pembatalan hanya boleh sekali.` (kode keluar 1) | Tidak ada (memang dilarang) |
| Gagal sistem | Perubahan status gagal disimpan | `Gagal membatalkan transaksi: <alasan>. Status dan stok tidak berubah.` | Ya: coba lagi |
| Tidak punya akses | Peran bukan pemilik | `Gagal: pembatalan hanya boleh dilakukan pemilik. Minta pemilik menjalankan perintah ini.` (kode keluar 1) | Ya: minta pemilik |
| Data besar | Transaksi dengan banyak baris | Semua baris stok yang dikembalikan dicetak | – |

**Aturan tampilan:**

- Pembatalan adalah tindakan berisiko, jadi keluarannya menyebut **apa** yang berubah (kode, alasan, dan daftar stok yang dikembalikan), bukan sekadar "berhasil".
- Tidak ada tombol "batal" yang bisa diklik dua kali sampai berhasil; percobaan kedua ditolak dengan pesan jelas.

---

## 5. Navigasi

```
python -m app
  ├─ produk
  │    ├─ tambah   (S-02)
  │    └─ daftar   (S-01)
  ├─ jual          (S-03)
  ├─ rekap         (S-04)
  ├─ batal         (S-05)
  └─ --help        (S-06)
```

| Dari | Aksi | Ke | Siapa yang boleh |
|---|---|---|---|
| Terminal | `produk daftar` | S-01 | Kasir, Pemilik |
| Terminal | `produk tambah` | S-02 | Kasir, Pemilik |
| Terminal | `jual` | S-03 | Kasir, Pemilik |
| Terminal | `rekap` | S-04 | Kasir, Pemilik |
| Terminal | `batal` | S-05 | **Pemilik saja** |
| Terminal | `--help` | S-06 | Kasir, Pemilik |

---

## 6. Peran & tampilan

| Peran | Layar yang bisa diakses | Elemen yang disembunyikan | Aksi yang dilarang |
|---|---|---|---|
| Kasir | S-01, S-02, S-03, S-04, S-06 | – (semua perintah terlihat di `--help`) | `batal` (S-05) |
| Pemilik | S-01…S-06 | – | – |

Catatan penting: menyembunyikan elemen di UI **bukan** pengamanan. Penegakan hak akses tetap dilakukan di lapisan logika (lihat `03-architecture.md` bagian 7). Perintah `batal` menolak peran bukan pemilik walaupun perintahnya tetap muncul di bantuan.

---

## 7. Bahasa & penulisan teks

| Aspek | Aturan | Contoh |
|---|---|---|
| Bahasa antarmuka | Indonesia | – |
| Nada pesan | Netral, tidak menyalahkan | `Data belum lengkap` bukan `Input Anda salah` |
| Pesan error | Sebutkan penyebab + cara memperbaiki | `Gagal: stok BRS-5KG tinggal 2, tidak cukup untuk 5. Kurangi qty atau tambah stok.` |
| Label tombol | Kata kerja, spesifik | `Simpan Transaksi`, bukan `OK` |
| Format angka | Titik sebagai pemisah ribuan, tanpa desimal | Rp1.234.567 |
| Format uang | Awalan `Rp` menempel, titik ribuan | Rp6.500 (bukan Rp 6.500, bukan IDR 6500) |
| Format tanggal | `YYYY-MM-DD` di perintah dan keluaran | 2026-10-03 |
| Format nomor transaksi | `TRX-YYYYMMDD-###` | TRX-20261003-001 |

Catatan: uang disimpan sebagai bilangan bulat rupiah penuh (tanpa sen), dan ditampilkan sebagai `Rp1.234.567`. Perhitungan memakai bilangan bulat agar tidak ada pembulatan yang menyimpang.

---

## 8. Umpan balik & keamanan tindakan

| Tindakan | Tingkat risiko | Konfirmasi | Bisa dibatalkan | Pemberitahuan |
|---|---|---|---|---|
| Lihat daftar produk | rendah | tidak | – | Keluaran daftar |
| Simpan transaksi (jual) | sedang | tidak (sistem menolak input salah) | ya, lewat `batal` (satu kali) | Rincian + kode transaksi + kembalian |
| Tambah produk | sedang | tidak | Tidak dihapus; perlu koreksi manual oleh pemilik | Konfirmasi SKU + nama |
| Batalkan transaksi | tinggi | ya — perintah `batal` memerlukan `--kode` + `--alasan`, dan hanya pemilik | tidak (status akhir) | Sebutkan kode, alasan, dan daftar stok yang dikembalikan |
| Menimpa/hapus data | – | Tidak ada perintah semacam ini | – | – |

Catatan: pembatalan adalah satu-satunya tindakan berisiko tinggi. Karena itu ia membutuhkan kode transaksi eksplisit, alasan minimal 5 karakter, dan hanya boleh dijalankan pemilik.

---

## 9. Aksesibilitas & kenyamanan

Hanya tulis yang relevan dengan konteks pemakaian nyata.

| Aspek | Target | Alasan |
|---|---|---|
| Ukuran teks minimum | Ukuran terminal bawaan (jangan paksa mengecil) | Dibaca sekilas di meja kasir |
| Kontras | Kontras bawaan terminal | Cukup untuk ruangan dalam toko |
| Navigasi keyboard | Penuh (semua perintah diketik) | Kasir bekerja dengan papan ketik |
| Label kolom wajib | Header kolom jelas: `SKU  Nama  Harga  Stok` | Mengurangi salah pilih SKU |
| Panjang pesan error | Maksimal 2 baris | Harus terbaca cepat tanpa menggulir |
| Warna | Tidak mengandalkan warna untuk menyampaikan status (pakai kata `SELESAI`/`DIBATALKAN`) | Terminal bisa tanpa warna |

---

## 10. Yang belum didesain

Bagian ini mencegah AI "mengisi sendiri" tampilan yang belum diputuskan.

| Layar/fitur | Kenapa belum didesain | Rencana |
|---|---|---|
| Cetak struk ke printer | Di luar scope P0 | Ditinjau bila pelanggan menuntut struk |
| Pencarian/filter produk | Jumlah SKU masih kecil `[butuh data]` | Ditambah bila daftar produk mulai panjang |
| Ekspor rekap ke berkas | Fitur P1 | Didesain setelah P0 stabil |
| Penyesuaian stok manual | Butuh aturan hak akses | Didesain bersama aturan barunya |
| Tampilan warna/format kaya | Tidak dibutuhkan; teks cukup | Ditinjau bila ada keluhan keterbacaan |

---

## 11. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |