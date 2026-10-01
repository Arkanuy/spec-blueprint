# 01 — Product Requirements Document (PRD)

> Dokumen ini menjawab: **apa yang dibangun, untuk siapa, dan sampai mana batasnya.** Diturunkan dari [00-discovery.md](00-discovery.md). Setiap fitur di sini harus punya alasan yang bisa dilacak ke masalah — bukan karena "keren" atau "biasanya aplikasi punya fitur ini".

**Proyek:** {{PROJECT_NAME}}
**Versi dokumen:** 0.1
**Status:** Draft / Direview / Disetujui
**Pemilik produk:** {{OWNER}}
**Terakhir diperbarui:** {{DATE}}

---

## 1. Ringkasan produk

**Dalam satu paragraf** — apa produk ini, untuk siapa, dan masalah apa yang diselesaikan.

```
{{PROJECT_NAME}} adalah [jenis aplikasi] yang membantu [pengguna utama] untuk
[aktivitas utama], sehingga [hasil yang diinginkan]. Sebelumnya [kondisi lama],
yang menyebabkan [masalah]. Batas produk ini adalah [batas singkat].
```

<!-- EXAMPLE-START -->
Contoh: Toko Berkah POS adalah aplikasi kasir berbasis web yang membantu kasir dan pemilik toko mencatat transaksi penjualan secara terpusat, sehingga rekap harian bisa dipercaya tanpa menghitung ulang nota kertas. Sebelumnya pencatatan dilakukan di kertas dan direkap manual setiap minggu, yang menyebabkan selisih stok dan laporan terlambat. Batas produk ini: hanya penjualan dan stok keluar, belum termasuk pembelian dari supplier.
<!-- EXAMPLE-END -->

---

## 2. Masalah dan tujuan

Disalin ringkas dari `00-discovery.md` agar AI punya konteks tanpa harus membuka dua file.

| Item | Isi |
|---|---|
| Masalah utama | [satu kalimat] |
| Akar masalah | [satu kalimat] |
| Dampak terukur | [dengan satuan] |
| Tujuan bisnis | [G-1, G-2 dari discovery] |
| Kondisi sukses | [kondisi yang bisa diamati] |
| Kondisi gagal | [kondisi yang menandakan produk tidak berguna] |

---

## 3. Pengguna & persona

| Persona | Peran dalam bisnis | Tujuan utama saat memakai sistem | Frekuensi pakai | Kemampuan teknis | Perangkat |
|---|---|---|---|---|---|
| [nama persona] | [jabatan/fungsi] | [yang ingin dicapai] | [harian/mingguan] | [rendah/menengah/tinggi] | [HP/laptop/tablet] |

<!-- EXAMPLE-START -->
Contoh:
| Kasir | Menjalankan transaksi penjualan | Menyelesaikan pembayaran dengan cepat dan benar | 100+ kali/hari | Rendah | Desktop kasir |
| Pemilik toko | Memantau & memutuskan | Mengetahui penjualan dan stok tanpa menunggu laporan | 1–3 kali/hari | Menengah | HP |
<!-- EXAMPLE-END -->

### 3.1 Yang penting bagi tiap persona

- [persona A]: cepat, sedikit klik, tahan salah input
- [persona B]: bisa dilihat dari HP, angka bisa dipercaya, tidak perlu instalasi

---

## 4. Alur utama pengguna

Tulis alur normal (happy path) per persona. Detail lengkap (alternatif & error) ada di [04-workflow.md](04-workflow.md).

**Alur 1 — [nama alur]**

1. Pengguna [aksi]
2. Sistem [respons]
3. Pengguna [aksi]
4. Sistem [hasil]

**Kondisi akhir:** [apa yang tercapai]
**Titik gagal yang harus ditangani:** [kondisi error yang mungkin]

---

## 5. Daftar fitur

Prioritas:

- **P0** — tanpa ini produk tidak berguna. Wajib untuk rilis pertama.
- **P1** — penting, tapi produk masih bisa dipakai tanpanya.
- **P2** — bagus kalau ada, tunda kalau waktu terbatas.
- **X** — di luar scope (sengaja tidak dibuat sekarang).

| ID | Fitur | Prioritas | Persona | User story | Alasan (mengapa fitur ini ada) | FR terkait |
|---|---|---|---|---|---|---|
| F-01 | [nama fitur] | P0 | [persona] | US-01 | [masalah/akar masalah yang diselesaikan] | FR-001 |
| F-02 | [nama fitur] | P0 | [persona] | US-02 | [alasan] | FR-002..004 |
| F-03 | [nama fitur] | P1 | [persona] | US-05 | [alasan] | FR-005 |
| F-04 | [nama fitur] | X | – | – | [kenapa sengaja tidak dibuat] | – |

Aturan: **fitur tanpa alasan yang bisa ditelusuri ke masalah harus dihapus.** Kolom "alasan" tidak boleh berisi "standar aplikasi" atau "supaya lengkap".

### 5.1 Penjelasan fitur P0

Untuk setiap fitur P0, tulis satu blok seperti ini:

**F-01 — [Nama fitur]**

- **Masalah yang diselesaikan:** [...]
- **Cara kerja singkat:** [...]
- **Input:** [...]
- **Output:** [...]
- **Aturan yang mengikat:** [BR-xx]
- **Selesai kalau:** [...kriteria yang bisa diuji...]
- **Bukan bagian dari fitur ini:** [...agar AI tidak melebar...]

---

## 6. Scope

### 6.1 Termasuk (IN SCOPE)

- [kapabilitas 1]
- [kapabilitas 2]

### 6.2 Tidak termasuk (OUT OF SCOPE)

| Hal yang dikecualikan | Alasan | Kapan mungkin ditinjau ulang |
|---|---|---|
| [fitur/proses] | [alasan] | [kondisi pemicu] |

Contoh pengecualian yang sering perlu dinyatakan eksplisit: integrasi pembayaran online, aplikasi mobile native, multi-cabang, multi-bahasa, AI/rekomendasi, notifikasi WhatsApp, ekspor akuntansi.

### 6.3 Ide tunda (parking lot)

Ide yang muncul saat diskusi tapi bukan bagian dari masalah saat ini. **Ditulis di sini, bukan langsung dikerjakan.**

| Ide | Kapan menarik | Alasan ditunda |
|---|---|---|

---

## 7. Batasan & dependensi

| Jenis | Isi | Dampak kalau tidak dipenuhi |
|---|---|---|
| Teknis | [stack yang sudah ditentukan, perangkat minimum] | [isi] |
| Waktu | [tenggat] | [isi] |
| Anggaran | [batas biaya operasional] | [isi] |
| Data | [data lama yang harus dipakai] | [isi] |
| Pihak ketiga | [layanan eksternal yang dipakai] | [isi] |
| Kebijakan | [aturan organisasi/regulasi] | [isi] |
| Kemampuan tim | [yang tim bisa rawat] | [isi] |

---

## 8. Metrik keberhasilan

| # | Metrik | Baseline sekarang | Target | Cara mengukur | Kapan diukur |
|---|---|---|---|---|---|
| M-1 | [metrik] | [kondisi awal] | [target] | [metode] | [waktu] |

Metrik buruk: "aplikasi dipakai banyak orang". Metrik baik: "waktu tutup kasir turun dari 30 menit menjadi <5 menit".

---

## 9. Non-goals (produk ini BUKAN apa)

Nyatakan tegas agar AI tidak menambahkan hal yang tidak diminta:

- Produk ini **bukan** [sistem akuntansi lengkap].
- Produk ini **tidak** menggantikan [proses/produk lain].
- Produk ini **tidak** dirancang untuk [skenario di luar cakupan].

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
| A-01 | [asumsi] | [dampak] | [cara] |

---

## 12. Pertanyaan terbuka

| # | Pertanyaan | Menghambat apa | Penanggung jawab | Status |
|---|---|---|---|---|
| Q-01 | [pertanyaan] | [bagian yang tidak bisa dilanjut] | [nama] | Terbuka/Tertutup |

---

## 13. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan | Oleh |
|---|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek | {{OWNER}} |
