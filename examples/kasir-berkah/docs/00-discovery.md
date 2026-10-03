# 00 — Discovery & Konteks Bisnis

> Tujuan dokumen ini: memastikan masalahnya **nyata**, akar masalahnya **benar**, dan sistem adalah **solusi yang proporsional**. Dokumen ini ditulis sebelum PRD. Kalau bagian ini kosong, PRD akan berisi tebakan.

**Proyek:** Kasir Berkah
**Domain bisnis:** retail / toko kelontong
**Pemilik produk:** Toko Berkah
**Tanggal:** 2026-10-03

---

## 1. Konteks organisasi

| Item | Isi |
|---|---|
| Nama organisasi / usaha | Toko Berkah |
| Bidang usaha | retail / toko kelontong |
| Produk / layanan utama | Penjualan kebutuhan harian secara eceran (beras, minyak goreng, gula, sabun, minuman, rokok) |
| Pelanggan utama | Warga di sekitar toko, sebagian langganan tetap |
| Perkiraan skala operasi | [butuh data: jumlah transaksi/hari dan jumlah kasir belum pernah dicatat terpisah dari nota] |
| Unit yang terlibat | Kasir dan pemilik (pemilik ikut menjaga toko) |
| Sistem yang sudah dipakai sekarang | Belum ada aplikasi. Nota kertas karbon untuk penjualan, buku stok tulis tangan untuk persediaan, kalkulator untuk menghitung total dan kembalian. |

---

## 2. Stakeholder

Siapa saja yang terlibat atau terpengaruh. Bedakan **stakeholder** (terpengaruh) dari **aktor** (langsung memakai sistem).

| Stakeholder | Peran | Kepentingan utama | Info yang butuh | Info yang dihasilkan | Titik sakit | Aktor sistem? |
|---|---|---|---|---|---|---|
| Kasir | Melayani penjualan di depan toko | Menyelesaikan transaksi cepat dan benar, tidak salah kembalian | Daftar produk + harga + stok | Data transaksi penjualan dan qty tiap barang | Salah hitung saat ramai, stok di buku tidak cocok | Ya |
| Pemilik | Memutuskan harga, belanja stok, menilai penjualan | Tahu penjualan harian dan sisa stok tanpa menunggu rekap | Rekap harian (jumlah transaksi, total penjualan, item terjual), sisa stok | Daftar produk dan harga | Rekap baru selesai malam, keputusan belanja sering telat | Ya |
| Pemasok | Memasok barang | Pesanan jelas dan jumlahnya benar | Daftar barang yang perlu dibeli ulang | Barang dagangan | Pemilik tidak yakin jumlah stok, pesanan kadang lebih/kurang | Tidak |
| Pelanggan | Membeli barang | Harga benar, kembalian benar, dilayani cepat | Total belanja dan kembalian | Uang bayar | Antre saat kasir menghitung manual; pernah salah kembalian | Tidak |

Catatan: Pemasok dan pelanggan tidak memakai sistem. Pemilik memakai sistem hanya untuk perintah rekap; kasir memakai seluruh perintah lain.

---

## 3. Kondisi saat ini (AS-IS)

Tulis proses yang berjalan sekarang, apa adanya — termasuk alat manual, WhatsApp, Excel, buku tulis. **Jangan** memasukkan fitur sistem yang belum ada ke bagian ini.

### 3.1 Proses sekarang, langkah per langkah

| # | Aktor | Aktivitas | Input | Output | Alat | Waktu/durasi | Masalah terlihat |
|---|---|---|---|---|---|---|---|
| 1 | Kasir | Menerima pesanan pelanggan | Permintaan lisan pelanggan | Tumpukan barang di meja | – | detik | – |
| 2 | Kasir | Menghitung total belanja | Harga tiap barang | Angka total di kalkulator | Kalkulator | puluhan detik | Salah tekan saat ramai; harga kadang lupa |
| 3 | Kasir | Menghitung kembalian | Uang bayar − total | Angka kembalian | Kalkulator | puluhan detik | Kembalian sering dibulatkan spontan, selisih menumpuk |
| 4 | Kasir | Menulis nota | Nama barang + qty + total | Nota kertas karbon 2 lembar | Nota kertas + pulpen | puluhan detik per nota | Tulisan tidak terbaca, lembar arsip hilang |
| 5 | Kasir | Mencatat stok terpakai | Ingatan atas barang yang terjual | Coretan di buku stok | Buku stok tulis tangan | saat luang | Sering lupa mencatat, terutama saat ramai |
| 6 | Pemilik | Merekap penjualan harian | Tumpukan nota | Total penjualan + jumlah transaksi | Kalkulator + buku | 1–2 jam tiap malam | Menghabiskan waktu istirahat; angka tidak bisa dicek ulang |
| 7 | Pemilik | Memutuskan belanja stok | Sisa stok di buku + pengamatan rak | Daftar belanja ke pemasok | Pengamatan + buku stok | beberapa menit | Keputusan berdasarkan angka yang sering tidak cocok |

### 3.2 Di mana pekerjaan terasa berat

- Menjumlahkan seluruh nota secara manual setiap malam (1–2 jam) — sumber utama waktu terbuang.
- Menghitung total dan kembalian di kalkulator sambil melayani antrean.
- Mencatat stok di buku terpisah dari penjualan, lalu mencocokkan keduanya di kepala.
- Informasi harga dan stok tersebar: sebagian di rak, sebagian di buku, sebagian hanya diingat.
- Rekap harus dirakit ulang dari tumpukan kertas, jadi tidak bisa dilihat kapan saja.

### 3.3 Bukti pendukung

Kumpulkan bukti, bukan opini:

- [ ] Dokumen yang dipakai sekarang (foto nota, screenshot Excel, template laporan) → **belum dikumpulkan** `(Perlu dikonfirmasi)` — dikumpulkan pada Q-01
- [ ] Jumlah transaksi / volume pekerjaan per periode → sumber: belum ada catatan terpisah; `[butuh data]`, lihat Q-01
- [ ] Keluhan pelanggan atau staf → dikatakan oleh: pemilik dan kasir secara lisan `(Perlu dikonfirmasi)`
- [ ] Data lama yang bisa dihitung (contoh: rata-rata pesanan salah per bulan) → belum pernah dihitung, `[butuh data]`, lihat Q-02

Kalau bukti belum ada, tulis `(Perlu dikonfirmasi)` dan masukkan ke 09-risks.md.

---

## 4. Pohon masalah

### 4.1 Gejala (yang terlihat sehari-hari)

1. Rekap penjualan baru selesai 1–2 jam setelah toko tutup, dan hasilnya sering dipersoalkan ulang.
2. Stok di buku tidak cocok dengan barang di rak; selisih ketahuan saat barang mau dijual habis.
3. Kembalian pernah salah; pelanggan mengeluh atau uang kas selisih tanpa ketahuan.

### 4.2 Akar masalah (5 Whys)

Ambil gejala paling penting, turunkan sampai penyebab yang benar-benar bisa diperbaiki:

| Tingkat | Pertanyaan | Jawaban |
|---|---|---|
| 1 | Kenapa rekap penjualan sering salah dan lama? | Karena semua nota dijumlah ulang dengan kalkulator setiap malam. |
| 2 | Kenapa harus dijumlah ulang? | Karena nota yang tersimpan di kertas tidak bisa dihitung otomatis dan sering tidak lengkap. |
| 3 | Kenapa tidak lengkap? | Karena nota ditulis tangan sambil melayani antrean, jadi ada yang terlewat atau tidak terbaca. |
| 4 | Kenapa masih ditulis tangan? | Karena tidak ada satu tempat data transaksi yang tersimpan dan bisa dipakai ulang untuk menghitung. |
| 5 | Akar masalah | Tidak ada sumber data transaksi yang terpusat dan bisa dipercaya; angka penjualan dan stok harus dirakit ulang dari kertas setiap kali dibutuhkan. |

### 4.3 Apakah masalah ini nyata?

| Uji | Jawaban | Bukti |
|---|---|---|
| Terjadi berulang, bukan sekali | Ya | Rekap manual dilakukan setiap malam, bukan kejadian tunggal `(Fakta dari kebiasaan toko)` |
| Menimbulkan kerugian terukur (waktu/uang/risiko) | Ya | Waktu 1–2 jam tiap malam `(Perlu dikonfirmasi)`; selisih kas dan selisih stok `[butuh data angkanya]` |
| Ada orang yang bertanggung jawab merasakannya | Pemilik dan kasir | Pemilik kehilangan waktu istirahat; kasir dipersoalkan saat rekap tidak cocok `(Perlu dikonfirmasi)` |
| Tidak bisa diselesaikan hanya dengan kebiasaan baru | Ya | Masalahnya adalah ketiadaan data yang bisa dihitung ulang, bukan sekadar disiplin mencatat. Menyuruh kasir menulis lebih rapi tidak menghilangkan kerja penjumlahan dan pencocokan. |

Kalau ada jawaban "Tidak" di sini, **jangan lanjut ke PRD**. Perbaiki dulu rumusan masalahnya, karena sistem tidak akan menyelesaikan masalah yang bukan masalah.

---

## 5. Dampak bisnis

| Dimensi | Dampak saat ini | Bagaimana diukur |
|---|---|---|
| Waktu | Pemilik kehilangan 1–2 jam tiap malam untuk merekap `(Perlu dikonfirmasi)` | Catat jam mulai dan selesai rekap selama beberapa hari |
| Biaya | Selisih kas dan selisih stok menggerus margin tanpa terdeteksi | Bandingkan nilai stok buku vs hitung fisik akhir bulan `[butuh data]` |
| Pengalaman pelanggan | Antre lebih lama saat kasir menghitung manual; pernah salah kembalian | Keluhan pelanggan + lamanya antre (belum dicatat) |
| Beban kerja staf | Kasir harus mengerjakan pekerjaan rangkap: melayani, menghitung, mencatat stok | Amati jumlah aktivitas per transaksi |
| Kualitas data | Angka penjualan dan stok dirakit ulang tiap hari dari kertas; tidak ada rujukan tunggal | Bandingkan hasil rekap dua kali atas nota yang sama `[butuh data]` |
| Pengambilan keputusan | Pemilik memutuskan belanja dari pengamatan rak, bukan angka pasti | Catat berapa kali barang kehabisan atau kebanyakan |
| Risiko / kepatuhan | Tidak ada jejak audit; nota hilang berarti transaksi tidak bisa dibuktikan | Hitung frekuensi nota hilang/tidak terbaca `[butuh data]` |

Aturan: **jangan mengarang angka.** Kalau belum ada data, tulis `[butuh data]` dan sebutkan cara mendapatkannya.

Cara mendapatkan angka yang masih kosong dicatat sebagai Q-01 dan Q-02 di [09-risks.md](09-risks.md).

---

## 6. Tujuan bisnis

Ubah masalah menjadi tujuan yang menggambarkan hasil, bukan fitur.

| # | Tujuan | Terhubung ke akar masalah | Indikator keberhasilan |
|---|---|---|---|
| G-1 | Tersedia satu sumber data transaksi yang bisa dihitung ulang dan dipercaya | Akar masalah tingkat 5 | Rekap harian dihasilkan dari sistem tanpa menjumlah nota manual; selisih rekap turun `[butuh data baseline]` |
| G-2 | Pemilik tahu penjualan harian dan sisa stok tanpa menunggu rekap manual | Akar masalah tingkat 5 | Rekap dan sisa stok tersedia segera setelah transaksi terakhir disimpan |
| G-3 | Mengurangi salah hitung total dan kembalian | Akar masalah tingkat 1 dan 3 | Total dan kembalian dihitung sistem; tidak ada lagi hitung manual di kalkulator |

Tujuan buruk: "Membuat aplikasi kasir." — itu solusi, bukan tujuan.

---

## 7. Evaluasi alternatif solusi

**Jangan langsung memilih sistem.** Bandingkan minimal 3 opsi, termasuk opsi paling murah.

| Alternatif | Cara kerja | Kelebihan | Kekurangan | Perkiraan biaya/effort | Cocok? |
|---|---|---|---|---|---|
| A. Perbaikan proses saja (SOP + form nota standar) | Bikin format nota baku, kasir wajib menulis rapi, pemilik merekap dengan cara yang sama | Tidak perlu teknologi; bisa jalan besok | Kerja menjumlah dan mencocokkan stok tetap manual; salah hitung dan nota hilang tidak hilang | Rendah | Tidak — tidak menyentuh akar masalah |
| B. Perbaikan proses + spreadsheet terstruktur | Nota tetap ditulis, lalu tiap malam kasir memasukkan ke lembar Excel yang otomatis menjumlah | Rekap lebih cepat; rumus mengurangi salah hitung | Masih input ganda (nota → Excel); stok tidak otomatis; butuh laptop + disiplin harian; rawan salah ketik | Rendah–sedang | Tidak — mengurangi sebagian masalah tapi menambah pekerjaan input |
| C. Aplikasi sederhana 1 modul inti (nota digital + rekap) | Kasir mencatat transaksi di aplikasi; total, kembalian, dan rekap dihitung sistem | Menghilangkan nota kertas, menghitung otomatis, rekap instan, stok berkurang sendiri | Perlu waktu membuat dan melatih kasir; bergantung pada satu perangkat | Sedang | Ya |
| D. Aplikasi lengkap multi-modul (POS + akuntansi + pembelian + multi-cabang) | Sistem besar dengan pembelian, hutang, laporan keuangan, banyak cabang | Menjawab hampir semua kebutuhan masa depan | Jauh melebihi masalah saat ini; lama dibuat; sulit dirawat tanpa tenaga IT | Tinggi | Tidak — tidak proporsional sekarang |

### Keputusan

- **Dipilih:** C — aplikasi CLI sederhana, satu modul inti (catat penjualan, hitung total/kembalian, kurangi stok, rekap harian, batal transaksi).
- **Alasan:** Opsi A tidak menyentuh akar masalah (data tetap di kertas dan harus dihitung ulang). Opsi B masih menyimpan nota kertas dan menambah pekerjaan input ganda, sedangkan stok tetap tidak otomatis. Opsi D jauh lebih besar dari masalah yang ada dan tidak ada tenaga untuk merawatnya. Opsi C menghapus langsung akar masalahnya: satu sumber data transaksi yang bisa dihitung ulang, dengan stok yang ikut berkurang saat terjual. Bentuk CLI dipilih karena bisa dijalankan di perangkat toko yang sudah ada tanpa server dan tanpa instalasi tambahan.
- **Yang sengaja tidak diambil sekarang:** pembelian dari pemasok, multi-cabang, diskon/promo, cetak struk ke printer, login berbasis password, sinkronisasi online, laporan bulanan, ekspor Excel. Semua masuk "di luar scope" (lihat [01-prd.md](01-prd.md)).

Aturan: kalau masalah bisa selesai dengan SOP atau spreadsheet, sistem **tidak wajib dibuat** — dan itu keputusan yang sah.

---

## 8. Kelayakan

| Aspek | Penilaian | Catatan |
|---|---|---|
| Teknis | Bisa | Python 3.10+ dengan pustaka standar (`sqlite3`, `argparse`, `unittest`). Tanpa server, tanpa dependensi pihak ketiga. Perangkat toko cukup untuk menjalankannya. |
| Ekonomi | Layak | Tidak ada biaya langganan atau infrastruktur; hanya waktu pengerjaan. Manfaat terbesar berupa waktu pemilik dan pengurangan selisih. |
| Operasional | Siap dengan pelatihan singkat | Kasir tidak teknis, jadi teks perintah dan pesan error harus berbahasa Indonesia dan jelas (NFR-003). Perlu pendampingan hari pertama. |
| Jadwal | Cukup | Lingkupnya lima fitur P0; bisa dikerjakan bertahap. |
| Organisasi | Didukung | Pemilik yang meminta perbaikan rekap dan bersedia mengubah cara kerja. |
| Hukum / kebijakan | Aman | Tidak menyimpan data pribadi pelanggan; hanya transaksi dan produk. |

---

## 9. Ringkasan satu halaman

Tulis ≤10 baris. Ini yang dibaca AI dan orang sibuk.

```
Masalah   : Rekap penjualan dan stok dirakit manual dari nota kertas; lama, sering salah, dan tidak bisa dipercaya.
Akar      : Tidak ada sumber data transaksi yang terpusat dan bisa dihitung ulang.
Dampak    : 1–2 jam kerja pemilik tiap malam; selisih kas dan selisih stok tidak terdeteksi.
Tujuan    : Satu sumber data transaksi yang bisa dihitung ulang, rekap instan, stok ikut berkurang saat terjual.
Solusi    : Aplikasi CLI sederhana (Python + SQLite) untuk catat penjualan, hitung total/kembalian, kurangi stok, rekap harian, dan batal transaksi.
Batasan   : Tanpa internet, tanpa server, tanpa dependensi pihak ketiga; hanya lima fitur P0.
Sukses jika: Rekap harian keluar dari sistem tanpa menjumlah nota manual, dan stok sistem cocok dengan hitungan fisik.
Gagal jika : Kasir kembali ke nota kertas karena sistem lebih lambat atau membingungkan.
```

---

## 10. Yang belum diketahui

Pindahkan semua ketidakpastian ke [09-risks.md](09-risks.md) dengan nomor `Q-xx` agar bisa dilacak.

- Q-01: Berapa jumlah transaksi per hari dan berapa jumlah kasir? Belum pernah dicatat terpisah dari nota. Jawabannya menentukan perkiraan beban dan target NFR-005. Tenggat: 2026-10-10.
- Q-02: Berapa besar selisih kas dan selisih stok per bulan saat ini? Belum ada angka dasar untuk mengukur perbaikan. Tenggat: 2026-10-17.
- Q-03: Apakah kasir mengizinkan pembatalan transaksi, atau hanya pemilik? Keputusan ini memengaruhi matriks hak akses di [03-architecture.md](03-architecture.md). Tenggat: 2026-10-07.
- Q-04: Di perangkat apa aplikasi dijalankan (laptop toko atau komputer kasir) dan berapa spesifikasinya? Menentukan apakah NFR-005 terpenuhi. Tenggat: 2026-10-10.
