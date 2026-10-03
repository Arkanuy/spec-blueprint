# 01 — Product Requirements Document (PRD)

> Dokumen ini menjawab: **apa yang dibangun, untuk siapa, dan sampai mana batasnya.** Diturunkan dari [00-discovery.md](00-discovery.md). Setiap fitur di sini harus punya alasan yang bisa dilacak ke masalah — bukan karena "keren" atau "biasanya aplikasi punya fitur ini".

**Proyek:** Kasir Berkah
**Versi dokumen:** 0.1
**Status:** Draft
**Pemilik produk:** Toko Berkah
**Terakhir diperbarui:** 2026-10-03

---

## 1. Ringkasan produk

**Dalam satu paragraf** — apa produk ini, untuk siapa, dan masalah apa yang diselesaikan.

```
Kasir Berkah adalah aplikasi baris perintah (CLI) yang membantu kasir dan pemilik
toko kelontong mencatat transaksi penjualan pada satu sumber data, sehingga rekap
harian bisa dipercaya tanpa menghitung ulang nota kertas. Sebelumnya penjualan
ditulis di nota kertas dan direkap manual tiap malam, yang menyebabkan rekap lama
(1–2 jam), stok sering tidak cocok, dan salah hitung kembalian. Batas produk ini:
hanya penjualan, perhitungan total/kembalian, pengurangan stok, rekap harian, dan
pembatalan transaksi — belum termasuk pembelian dari pemasok, diskon, atau cetak
struk ke printer.
```

---

## 2. Masalah dan tujuan

Disalin ringkas dari `00-discovery.md` agar AI punya konteks tanpa harus membuka dua file.

| Item | Isi |
|---|---|
| Masalah utama | Rekap penjualan dan stok dirakit manual dari nota kertas; lama, sering salah, dan tidak bisa dipercaya. |
| Akar masalah | Tidak ada sumber data transaksi yang terpusat dan bisa dihitung ulang. |
| Dampak terukur | 1–2 jam kerja pemilik tiap malam `(Perlu dikonfirmasi)`; selisih kas/stok `[butuh data]`. |
| Tujuan bisnis | G-1 (sumber data tunggal), G-2 (rekap & stok tanpa menunggu), G-3 (hilangkan salah hitung). |
| Kondisi sukses | Rekap harian dihasilkan sistem tanpa penjumlahan nota manual; stok di sistem cocok dengan hitungan fisik. |
| Kondisi gagal | Kasir kembali memakai nota kertas karena sistem dianggap lebih lambat atau membingungkan. |

---

## 3. Pengguna & persona

| Persona | Peran dalam bisnis | Tujuan utama saat memakai sistem | Frekuensi pakai | Kemampuan teknis | Perangkat |
|---|---|---|---|---|---|
| Kasir | Melayani transaksi penjualan | Mencatat penjualan cepat dan benar, tahu total dan kembalian | Setiap transaksi (puluhan kali per hari) `[butuh data jumlah pasti]` | Rendah | Komputer/laptop toko dengan terminal |
| Pemilik | Memantau penjualan & stok, memutuskan belanja | Melihat rekap harian dan sisa stok tanpa menunggu rekap manual | 1–2 kali sehari (saat tutup toko) | Menengah | Komputer/laptop toko dengan terminal |

Catatan: jumlah transaksi per hari belum pernah dicatat — lihat Q-01 di [09-risks.md](09-risks.md).

### 3.1 Yang penting bagi tiap persona

- Kasir: cepat, sedikit perintah yang perlu diingat, pesan error jelas saat salah ketik (jangan sampai menahan antrean), dan aman dari salah input qty/harga.
- Pemilik: angka rekap yang bisa dipercaya, bisa melihat sisa stok kapan saja, tidak perlu instalasi apa pun, dan tidak bergantung pada internet.

---

## 4. Alur utama pengguna

Tulis alur normal (happy path) per persona. Detail lengkap (alternatif & error) ada di [04-workflow.md](04-workflow.md).

**Alur 1 — Kasir mencatat penjualan**

1. Kasir menjalankan `python -m app produk daftar` untuk melihat produk.
2. Kasir menjalankan `python -m app jual --produk SKU:QTY ... --bayar ... --kasir "..."`.
3. Sistem menghitung total dari master produk, memeriksa stok dan kecukupan bayar.
4. Sistem menyimpan transaksi berstatus SELESAI, mengurangi stok, dan menampilkan nomor transaksi serta kembalian.

**Kondisi akhir:** Transaksi tersimpan dengan nomor `TRX-YYYYMMDD-###`, stok berkurang sesuai qty, kembalian ditampilkan.
**Titik gagal yang harus ditangani:** qty bukan bilangan bulat > 0, qty melebihi stok, uang bayar kurang dari total, produk tidak ditemukan, SKU duplikat dalam satu transaksi.

**Alur 2 — Pemilik melihat rekap**

1. Pemilik menjalankan `python -m app rekap --tanggal 2026-10-03`.
2. Sistem menghitung rekap dari transaksi berstatus SELESAI saja.
3. Sistem menampilkan jumlah transaksi, total penjualan, dan total item terjual.

**Kondisi akhir:** Pemilik mendapat rekap harian tanpa menghitung nota.
**Titik gagal yang harus ditangani:** tanggal tanpa transaksi (rekap kosong), format tanggal salah.

**Alur 3 — Pembatalan transaksi**

1. Kasir/pemilik menemukan transaksi salah input, lalu menjalankan `python -m app batal --kode TRX-20261003-001 --alasan "salah input"`.
2. Sistem memeriksa status transaksi masih SELESAI dan alasan minimal 5 karakter.
3. Sistem mengubah status menjadi DIBATALKAN dan mengembalikan stok.

**Kondisi akhir:** Transaksi tidak lagi dihitung di rekap; stok kembali seperti sebelum penjualan.
**Titik gagal yang harus ditangani:** alasan kurang dari 5 karakter, transaksi sudah DIBATALKAN, nomor transaksi tidak ditemukan, transaksi belum pernah berstatus SELESAI.

---

## 5. Daftar fitur

Prioritas:

- **P0** — tanpa ini produk tidak berguna. Wajib untuk rilis pertama.
- **P1** — penting, tapi produk masih bisa dipakai tanpanya.
- **P2** — bagus kalau ada, tunda kalau waktu terbatas.
- **X** — di luar scope (sengaja tidak dibuat sekarang).

| ID | Fitur | Prioritas | Persona | User story | Alasan (mengapa fitur ini ada) | FR terkait |
|---|---|---|---|---|---|---|
| F-01 | Catat penjualan (produk + qty → transaksi) | P0 | Kasir | US-001 | Nota kertas hilang/salah tulis, rekap tidak dipercaya | FR-001, FR-002, FR-003 |
| F-02 | Hitung total & kembalian otomatis | P0 | Kasir | US-002 | Salah hitung manual, selisih kas tiap hari | FR-004, FR-005 |
| F-03 | Stok berkurang otomatis saat terjual | P0 | Kasir, Pemilik | US-003 | Stok dicatat terpisah, sering tidak cocok | FR-006, FR-007 |
| F-04 | Rekap harian yang bisa dicetak | P0 | Pemilik | US-004 | Rekap manual butuh 1–2 jam tiap malam | FR-008, FR-009 |
| F-05 | Batal transaksi dengan alasan | P0 | Kasir, Pemilik | US-005 | Salah input tidak bisa dianulir, laporan jadi menggelembung | FR-010, FR-011, FR-012 |
| F-P1 | Ekspor rekap (mis. CSV) | P1 | Pemilik | US-006 | Memudahkan pengolahan lanjutan di luar sistem | – (belum diturunkan ke FR) |

Aturan: **fitur tanpa alasan yang bisa ditelusuri ke masalah harus dihapus.** Kolom "alasan" tidak boleh berisi "standar aplikasi" atau "supaya lengkap".

### 5.1 Penjelasan fitur P0

**F-01 — Catat penjualan**

- **Masalah yang diselesaikan:** Nota kertas hilang atau salah tulis, sehingga rekap tidak dipercaya.
- **Cara kerja singkat:** Kasir menyebut satu atau beberapa `SKU:QTY`, sistem mengambil harga dari master produk, lalu menyimpan transaksi.
- **Input:** SKU, qty, nama kasir.
- **Output:** Transaksi tersimpan dengan nomor `TRX-YYYYMMDD-###`.
- **Aturan yang mengikat:** BR-001 (qty bilangan bulat > 0), BR-002 (harga dari master), BR-009 (satu SKU satu baris), BR-010 (SKU unik).
- **Selesai kalau:** Satu transaksi dengan beberapa baris item bisa disimpan dan muncul di rekap tanpa input manual kedua kali.
- **Bukan bagian dari fitur ini:** diskon, catatan pelanggan, pembayaran non-tunai.

**F-02 — Hitung total & kembalian otomatis**

- **Masalah yang diselesaikan:** Salah hitung manual di kalkulator; selisih kas harian.
- **Cara kerja singkat:** Sistem menjumlahkan (qty × harga satuan) tiap baris, lalu menghitung kembalian = bayar − total.
- **Input:** qty per baris, harga dari master produk, uang bayar.
- **Output:** total transaksi dan kembalian.
- **Aturan yang mengikat:** BR-003 (total = Σ qty × harga), BR-004 (bayar ≥ total; kembalian = bayar − total).
- **Selesai kalau:** Total dan kembalian dihitung sistem dan tidak bisa ditimpa kasir.
- **Bukan bagian dari fitur ini:** pembulatan diskon, biaya layanan, pajak.

**F-03 — Stok berkurang otomatis saat terjual**

- **Masalah yang diselesaikan:** Stok dicatat terpisah dari penjualan dan sering tidak cocok.
- **Cara kerja singkat:** Saat transaksi disimpan, sistem mengurangi stok tiap produk sebesar qty terjual.
- **Input:** qty per baris.
- **Output:** stok terbaru tiap produk.
- **Aturan yang mengikat:** BR-005 (tidak boleh menjual melebihi stok), BR-008 (stok dikembalikan saat batal).
- **Selesai kalau:** Setelah penjualan, `produk daftar` menunjukkan stok berkurang tepat sebesar qty; setelah pembatalan, stok kembali.
- **Bukan bagian dari fitur ini:** pembelian/penambahan stok otomatis dari pemasok, penyesuaian stok manual (opname).

**F-04 — Rekap harian**

- **Masalah yang diselesaikan:** Rekap manual butuh 1–2 jam tiap malam.
- **Cara kerja singkat:** Sistem menghitung jumlah transaksi, total penjualan, dan total item terjual untuk satu tanggal, hanya dari transaksi SELESAI.
- **Input:** tanggal (`YYYY-MM-DD`).
- **Output:** rekap harian.
- **Aturan yang mengikat:** BR-003 (total yang dijumlahkan konsisten), FR-009 (hanya transaksi SELESAI).
- **Selesai kalau:** Rekap keluar segera tanpa penjumlahan manual dan angkanya cocok dengan daftar transaksi hari itu.
- **Bukan bagian dari fitur ini:** laporan bulanan, grafik, perbandingan antar-periode.

**F-05 — Batal transaksi dengan alasan**

- **Masalah yang diselesaikan:** Salah input tidak bisa dianulir, laporan jadi menggelembung.
- **Cara kerja singkat:** Transaksi SELESAI diubah ke DIBATALKAN bila alasan ≥ 5 karakter; stok dikembalikan.
- **Input:** kode transaksi, alasan.
- **Output:** status transaksi DIBATALKAN, stok bertambah kembali.
- **Aturan yang mengikat:** BR-006 (batal maksimal sekali), BR-007 (alasan ≥ 5 karakter), BR-008 (stok dikembalikan).
- **Selesai kalau:** Transaksi batal tidak lagi dihitung di rekap, stok kembali, dan pembatalan kedua ditolak.
- **Bukan bagian dari fitur ini:** pengembalian uang, pembatalan sebagian baris (partial refund).

---

## 6. Scope

### 6.1 Termasuk (IN SCOPE)

- Catat satu transaksi penjualan dengan beberapa baris item (F-01).
- Hitung total transaksi dan kembalian (F-02).
- Kurangi stok otomatis saat transaksi disimpan (F-03).
- Rekap harian: jumlah transaksi, total penjualan, total item terjual (F-04).
- Batalkan transaksi berstatus SELESAI dengan alasan (F-05).
- Lihat daftar produk berisi SKU, nama, harga, stok (pendukung F-01).
- Data tersimpan di SQLite lokal dan berjalan tanpa internet.

### 6.2 Tidak termasuk (OUT OF SCOPE)

| Hal yang dikecualikan | Alasan | Kapan mungkin ditinjau ulang |
|---|---|---|
| Pembelian dari pemasok | Bukan akar masalah saat ini; penambahan stok belum jadi kebutuhan P0 | Setelah penjualan & stok stabil dipakai harian |
| Multi-cabang | Toko baru satu lokasi | Kalau ada cabang kedua |
| Diskon/promo | Menambah aturan harga di luar BR yang sudah disepakati | Kalau promosi jadi kebiasaan tetap |
| Cetak struk ke printer | Butuh perangkat & driver tambahan | Kalau pelanggan menuntut struk |
| Login berbasis password | Aktor hanya kasir & pemilik di perangkat yang sama | Kalau ada beberapa kasir dengan hak berbeda |
| Sinkronisasi online | Koneksi toko tidak stabil (NFR-002) | Kalau ada kebutuhan melihat dari luar toko |
| Laporan bulanan | Belum ada keputusan bisnis yang butuh periode itu | Setelah rekap harian terbukti dipakai |
| Ekspor Excel | Belum dibutuhkan untuk keputusan harian | Kalau pemilik ingin mengolah data sendiri |
| Fitur AI/rekomendasi | Tidak ada keputusan bisnis yang butuh prediksi | Kalau ada data historis cukup dan masalah prediktif nyata |
| Notifikasi WhatsApp | Tidak dipakai untuk proses inti | Kalau ada kebutuhan memberi tahu pemilik saat jauh |

### 6.3 Ide tunda (parking lot)

Ide yang muncul saat diskusi tapi bukan bagian dari masalah saat ini. **Ditulis di sini, bukan langsung dikerjakan.**

| Ide | Kapan menarik | Alasan ditunda |
|---|---|---|
| Ekspor rekap harian ke CSV | Setelah pemilik ingin mengolah data di luar sistem | Belum masuk lima fitur P0 |
| Penyesuaian stok manual (opname) | Setelah ada selisih yang perlu dibetulkan tanpa transaksi | Butuh aturan siapa boleh dan jejak audit |
| Cetak struk ringkas ke file teks | Kalau pelanggan minta bukti | Belum ada permintaan nyata |

---

## 7. Batasan & dependensi

| Jenis | Isi | Dampak kalau tidak dipenuhi |
|---|---|---|
| Teknis | Python 3.10+ dengan pustaka standar (`sqlite3`, `argparse`, `unittest`); tanpa dependensi pihak ketiga | Sistem tidak bisa dijalankan di perangkat toko tanpa pemasangan tambahan |
| Waktu | Belum ada tenggat resmi `[butuh data]` | Prioritas bisa bergeser tanpa acuan |
| Anggaran | Tanpa biaya infrastruktur; hanya waktu pengerjaan | – |
| Data | Belum ada data lama terstruktur; nota kertas tidak dipindahkan ke sistem | Riwayat lama tidak bisa dianalisis sistem (dapat diterima untuk P0) |
| Pihak ketiga | Tidak ada | – |
| Kebijakan | Tidak menyimpan data pribadi pelanggan | – |
| Kemampuan tim | Kode harus bisa dirawat oleh orang non-spesialis, jadi sesederhana mungkin | Kode yang rumit akan terbengkalai setelah rilis |

---

## 8. Metrik keberhasilan

| # | Metrik | Baseline sekarang | Target | Cara mengukur | Kapan diukur |
|---|---|---|---|---|---|
| M-1 | Waktu menyelesaikan rekap harian | 1–2 jam `(Perlu dikonfirmasi)` | Kurang dari 1 menit | Catat jam mulai & selesai rekap sebelum dan sesudah | Minggu ke-2 setelah dipakai |
| M-2 | Kesesuaian stok sistem dengan hitungan fisik | Sering tidak cocok `[butuh data]` | Tidak ada selisih pada barang cepat laku | Hitung fisik sampel harian dan bandingkan | Harian pada minggu pertama |
| M-3 | Kejadian salah kembalian | Ada `[butuh data frekuensi]` | Nol (dihitung sistem) | Catat keluhan/betulan kasir | Setiap hari |
| M-4 | Transaksi tercatat tanpa nota kertas | 0% (semua nota kertas) | 100% transaksi harian di sistem | Bandingkan jumlah transaksi sistem vs pengamatan | Harian |

Metrik buruk: "aplikasi dipakai banyak orang". Metrik baik: "waktu tutup kasir turun dari 30 menit menjadi <5 menit".

---

## 9. Non-goals (produk ini BUKAN apa)

Nyatakan tegas agar AI tidak menambahkan hal yang tidak diminta:

- Produk ini **bukan** sistem akuntansi lengkap (tidak ada jurnal, hutang-piutang, atau laporan keuangan).
- Produk ini **tidak** menggantikan pengelolaan harga dan keputusan belanja pemilik; ia hanya menyediakan angka yang bisa dipercaya.
- Produk ini **tidak** dirancang untuk multi-cabang, multi-pengguna serentak, atau akses dari luar toko.

---

## 10. Definition of Done (tingkat produk)

Rilis pertama dianggap selesai kalau:

- [ ] Semua fitur P0 berfungsi sesuai acceptance criteria di `02-requirements.md`
- [ ] Semua kasus uji P0 lulus
- [ ] Tidak ada bug dengan tingkat keparahan kritis/tinggi yang terbuka
- [ ] Dokumen `03`–`06` sinkron dengan kondisi kode
- [ ] Ada data contoh yang cukup untuk mencoba semua alur
- [ ] Petunjuk pemasangan & penggunaan ditulis di `README.md` proyek

---

## 11. Asumsi

Hal yang dianggap benar tapi belum diverifikasi. Kalau asumsi ini ternyata salah, apa yang berubah?

| # | Asumsi | Risiko kalau salah | Cara verifikasi |
|---|---|---|---|
| A-01 | Kasir bersedia memakai terminal untuk setiap transaksi meskipun lebih lambat dari menulis nota | Sistem tidak dipakai; masalah lama kembali | Amati satu hari kerja setelah pelatihan |
| A-02 | Perangkat toko mampu menjalankan transaksi di bawah 1 detik (NFR-005) | Antrean melambat; kasir menghindari sistem | Ukur waktu simpan pada perangkat nyata |
| A-03 | Pemilik bisa menerima rekap tanpa cetak struk fisik | Perlu fitur cetak lebih awal | Tanyakan sebelum rilis |
| A-04 | Satu perangkat dipakai bergantian oleh kasir dan pemilik | Kalau ada beberapa perangkat, butuh aturan data bersama | Periksa jumlah perangkat di toko |

---

## 12. Pertanyaan terbuka

| # | Pertanyaan | Menghambat apa | Penanggung jawab | Status |
|---|---|---|---|---|
| Q-01 | Berapa jumlah transaksi per hari dan berapa jumlah kasir? | Perkiraan beban & target NFR-005 | Pemilik | Terbuka |
| Q-02 | Berapa besar selisih kas/stok saat ini? | Baseline metrik M-2 dan M-3 | Pemilik | Terbuka |
| Q-03 | Siapa yang boleh membatalkan transaksi, kasir atau hanya pemilik? | Matriks hak akses di `03-architecture.md` | Pemilik | Terbuka |
| Q-04 | Perangkat apa yang dipakai dan spesifikasinya? | Validasi NFR-005 | Pemilik/Kasir | Terbuka |

---

## 13. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan | Oleh |
|---|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek | Toko Berkah |
