# 09 — Risks, Asumsi & Pertanyaan Terbuka

> Dokumen ini menjawab: **apa yang bisa menggagalkan proyek, apa yang masih kita anggap benar tanpa bukti, dan apa yang belum kita ketahui.** Menuliskan asumsi di sini lebih murah daripada menemukannya salah setelah kode jadi.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

---

## 1. Risiko

Bedakan dengan jelas:

- **Risiko** — sesuatu yang *mungkin* terjadi dan berdampak buruk
- **Masalah** — sesuatu yang *sudah* terjadi
- **Batasan** — sesuatu yang pasti dan tidak bisa diubah

| ID | Risiko | Kategori | Kemungkinan | Dampak | Skor | Cara mengurangi | Penanggung jawab | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Kasir kembali memakai nota kertas karena sistem terasa lebih lambat/membingungkan | operasional | Sedang | Tinggi | 6 | Uji keselamatan di hari pertama; sediakan pendamping; sederhanakan perintah; ukur waktu per transaksi sebelum rilis | Pemilik | Terbuka |
| R-02 | Perangkat toko lambat sehingga simpan transaksi > 1 detik (NFR-005) | teknis | Sedang | Sedang | 4 | Ukur pada perangkat nyata (Q-04); batasi ukuran data; operasi tulis minimal | Developer | Terbuka |
| R-03 | Data hilang karena berkas `kasir.db` rusak atau terhapus tanpa cadangan | data | Sedang | Tinggi | 6 | Wajibkan pencadangan harian (salin berkas) sebelum tutup; uji pemulihan; jangan simpan di folder sementara | Pemilik | Terbuka |
| R-04 | Penyalahgunaan pembatalan untuk menutupi selisih kas | keamanan | Rendah | Tinggi | 3 | Pembatalan hanya pemilik (ADR-004); alasan wajib tertulis; transaksi batal tetap terlihat di data | Pemilik | Terbuka |
| R-05 | Stok sistem tidak cocok dengan rak karena kelalaian di luar sistem | data | Tinggi | Sedang | 6 | Rekap harian dipakai membandingkan; pembatalan mengembalikan stok; siapkan prosedur hitung fisik berkala | Pemilik | Terbuka |
| R-06 | Harga master diubah setelah transaksi lama; transaksi lama ikut berubah | data | Rendah | Tinggi | 3 | Harga disalin ke `sale_items.harga_satuan` saat transaksi dibuat (ADR-003) | Developer | Tertutup (sudah dirancang) |
| R-07 | Requirement bertambah di tengah jalan (mis. minta multi-cabang) | organisasi | Sedang | Sedang | 4 | Perubahan scope hanya lewat `10-decisions.md`; semua usulan baru masuk "ide tunda" | Pemilik | Terbuka |
| R-08 | Kode tidak bisa dirawat karena tidak ada yang paham | teknis | Rendah | Sedang | 2 | Pertahankan 3 tabel & satu lapisan logika; dokumentasi & uji otomatis | Developer | Terbuka |
| R-09 | Salah hitung kembalian tetap terjadi karena kasir mengabaikan keluaran sistem | operasional | Rendah | Sedang | 2 | Kembalian selalu ditampilkan; tampilkan total & kembalian berdampingan; pelatihan | Pemilik | Terbuka |
| R-10 | Angka dasar (volume transaksi, selisih kas/stok) tidak pernah diukur, sehingga keberhasilan tidak bisa dibuktikan | data | Tinggi | Sedang | 6 | Jawab Q-01 & Q-02 sebelum rilis; ukur baseline sebelum sistem dipakai | Pemilik | Terbuka |

Skor = Kemungkinan × Dampak (Rendah=1, Sedang=2, Tinggi=3). Skor ≥6 wajib punya rencana penanganan sebelum coding dimulai.

Risiko berskor ≥ 6 yang wajib ditangani lebih dulu: **R-01, R-03, R-05, R-10**. R-02 (skor 4) dipantau dan diukur di perangkat nyata.

### 1.1 Risiko yang paling sering muncul di proyek seperti ini

| Risiko | Tanda-tandanya | Pencegahan |
|---|---|---|
| Requirement berubah di tengah jalan (R-07) | Fitur bertambah sebelum P0 selesai | Perubahan hanya lewat `10-decisions.md`; fitur baru masuk "ide tunda" |
| Pengguna menolak memakai sistem (R-01) | "Nanti saja, sekarang jalan seperti biasa" | Libatkan kasir saat uji, mulai dari 1 alur nyata; pesan Bahasa Indonesia |
| Kualitas data lama buruk | Data lama tidak lengkap/berformat beda | Di proyek ini tidak ada data lama yang dipindahkan, jadi risiko ini tidak berlaku |
| Scope meledak (R-07) | "Sekalian tambahkan..." | Semua usulan baru masuk "ide tunda", bukan dikerjakan |
| Ketergantungan pihak ketiga | Layanan eksternal sering gagal | Tidak ada pihak ketiga (NFR-002), jadi risiko ini tidak berlaku |
| Kode hasil AI tidak bisa dirawat (R-08) | Tidak ada yang paham kodenya | Wajib ada dokumen + uji otomatis |
| Data hilang (R-03) | Tidak ada backup yang pernah diuji | Uji pemulihan, bukan sekadar menyimpan backup |

---

## 2. Asumsi

| ID | Asumsi | Kenapa dianggap benar | Kalau salah, apa yang berubah | Cara memverifikasi | Status |
|---|---|---|---|---|---|
| A-01 | Kasir menerima memakai terminal untuk setiap transaksi | Pemilik yang meminta; kasir terbiasa dengan ponsel/terminal sederhana | Sistem tidak dipakai; solusi harus dirancang ulang agar secepat nota | Amati 1 hari kerja setelah pelatihan | Terbuka |
| A-02 | Simpan transaksi < 1 detik di perangkat toko (NFR-005) | SQLite lokal & data kecil | Target NFR-005 gagal; perlu optimasi atau perangkat diganti | Ukur waktu `jual` di perangkat nyata (Q-04) | Terbuka |
| A-03 | Satu perangkat dipakai bergantian oleh kasir & pemilik | Toko kecil, satu meja kasir | Butuh aturan data bersama/multi-perangkat yang belum dirancang | Periksa jumlah perangkat (Q-04) | Terbuka |
| A-04 | Pembatalan dilakukan pemilik, bukan kasir | Pemilik ada di toko dan bisa memutuskan | Kalau pemilik sering tak ada, pembatalan macet; perlu aturan peran lain | Sepakati dengan pemilik (Q-03) | Terbuka |
| A-05 | Jumlah SKU masih sedikit (puluhan) sehingga `produk daftar` tanpa pencarian cukup | Toko kelontong kecil | Daftar terlalu panjang; butuh filter/pencarian lebih awal | Hitung jumlah SKU saat isi produk (Q-06) | Terbuka |
| A-06 | Nota kertas lama tidak perlu dipindahkan ke sistem | Tidak ada format terstruktur dan tidak dibutuhkan untuk keputusan harian | Riwayat lama tidak bisa dianalisis; perlu impor manual | Konfirmasi pemilik (Q-07) | Terbuka |

Aturan: asumsi yang **berdampak besar** dan **belum diverifikasi** harus diperiksa sebelum fase berikutnya. Kalau tidak bisa diverifikasi, rancang sistem agar mudah diubah. A-01, A-02, dan A-04 berdampak besar.

---

## 3. Pertanyaan terbuka

| ID | Pertanyaan | Menghambat apa | Siapa yang bisa menjawab | Tenggat | Status |
|---|---|---|---|---|---|
| Q-01 | Berapa jumlah transaksi per hari dan berapa jumlah kasir? | Perkiraan beban & target NFR-005; validasi asumsi operasional | Pemilik | 2026-10-10 | Terbuka |
| Q-02 | Berapa besar selisih kas dan selisih stok per bulan saat ini? | Baseline metrik M-2 dan M-3 | Pemilik | 2026-10-17 | Terbuka |
| Q-03 | Siapa yang boleh membatalkan transaksi — kasir atau hanya pemilik? | Hak akses `batal`; saat ini diputuskan hanya pemilik (ADR-004) | Pemilik | 2026-10-07 | Terbuka |
| Q-04 | Perangkat apa yang dipakai dan berapa spesifikasinya? | Validasi NFR-005 dan A-02 | Pemilik/Kasir | 2026-10-10 | Terbuka |
| Q-05 | Kapan tenggat proyek ini? | Target milestone M1–M3 dan pengurutan prioritas | Pemilik | 2026-10-10 | Terbuka |
| Q-06 | Berapa jumlah SKU yang akan didaftarkan? | Keputusan perlu/tidak pencarian produk di F-01 | Pemilik | 2026-10-17 | Terbuka |
| Q-07 | Apakah ada data nota lama yang wajib dipindahkan (mis. karena pajak)? | Lingkup migrasi data; mengubah `05-data-model.md` bagian 9 | Pemilik | 2026-10-17 | Terbuka |

Aturan: pertanyaan yang menghambat pekerjaan P0 **harus** dijawab sebelum coding bagian itu dimulai. Q-03, Q-04, dan Q-05 menghambat langsung Fase 0–1 dan wajib dijawab lebih dulu. Angka yang belum ada dasarnya ditulis `[butuh data]` di dokumen lain dan dilacak ke Q di sini.

---

## 4. Ketergantungan

| ID | Bergantung pada | Untuk apa | Kalau tidak tersedia | Rencana cadangan |
|---|---|---|---|---|
| D-01 | Perangkat toko (komputer/laptop) dengan Python 3.10+ | Menjalankan seluruh sistem | Sistem tidak bisa dijalankan | Siapkan satu perangkat yang memenuhi syarat sebelum rilis |
| D-02 | Data master produk (SKU, nama, harga, stok awal) dari pemilik | Mengisi `products` agar `jual` bisa dipakai | Tidak ada barang yang bisa dijual | Masukkan sekurangnya produk cepat laku sebagai contoh awal |
| D-03 | Keputusan pemilik atas Q-03 (siapa boleh batal) | Matriks hak akses & FR-010 | Otorisasi tidak final | Sementara diputuskan pemilik saja (ADR-004), ditinjau bila Q-03 berbeda |

---

## 5. Catatan yang dianggap sudah beres

Hal yang pernah jadi kekhawatiran tapi sudah diselesaikan. Berguna sebagai jejak.

| # | Kekhawatiran | Cara diselesaikan | Tanggal |
|---|---|---|---|
| 1 | Harga transaksi lama bisa berubah saat master harga diubah | Harga disalin ke `sale_items.harga_satuan` saat transaksi dibuat (ADR-003) | 2026-10-03 |
| 2 | Transaksi salah bisa dihapus diam-diam | Tidak ada perintah hapus; hanya status DIBATALKAN dengan alasan (ADR-004) | 2026-10-03 |
| 3 | Ketergantungan internet saat toko sibuk | Sistem sepenuhnya lokal, tanpa panggilan jaringan (NFR-002) | 2026-10-03 |

---

## 6. Pemantauan risiko

Risiko yang berubah wajib diperbarui, bukan dibiarkan menua.

| Tanggal | ID | Perubahan | Alasan |
|---|---|---|---|
| 2026-10-03 | – | Dokumen dibuat | Awal proyek |
| 2026-10-03 | R-06 | Status → Tertutup (sudah dirancang) | Harga disalin ke baris transaksi di `05-data-model.md` dan ADR-003 |

---

## 7. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |