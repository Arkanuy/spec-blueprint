# 05 — Data Model

> Dokumen ini menjawab: **data apa yang disimpan, bagaimana hubungannya, dan aturan apa yang menjaganya tetap benar.** Setiap entitas harus punya alasan bisnis. Entitas tanpa proses yang memakainya harus dihapus.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## 1. Klasifikasi data

| Jenis | Contoh di proyek ini | Sifat |
|---|---|---|
| Data induk (master) | [contoh: produk, pelanggan, pengguna] | Berubah jarang, dipakai berulang |
| Data transaksi | [contoh: penjualan, pembayaran] | Terus bertambah, tidak boleh diubah sembarangan |
| Data referensi | [contoh: status, kategori, metode bayar] | Daftar tetap, jadi pilihan |
| Dokumen / keluaran | [contoh: struk, invoice, laporan] | Dihasilkan dari data lain |

---

## 2. Daftar entitas

| Entitas | Jenis | Deskripsi satu baris | Pemilik data | Dipakai oleh proses | Perkiraan volume |
|---|---|---|---|---|---|
| [nama] | master/transaksi/referensi | [fungsi] | [peran] | [PS-0x / F-0x] | [kecil/sedang/besar] |

Uji: kalau sebuah entitas tidak dipakai oleh proses mana pun, **hapus atau jelaskan kenapa tetap ada**.

---

## 3. Detail entitas

Untuk setiap entitas, isi blok berikut. Ulangi sesuai jumlah entitas.

### Entitas: [NamaEntitas]

**Tujuan bisnis:** [kenapa data ini ada]
**Dibuat oleh:** [siapa/apa]
**Diubah oleh:** [siapa boleh mengubah]
**Dihapus/diarsipkan:** [kapan dan bagaimana]

| Field | Tipe | Wajib | Unik | Default | Aturan validasi | Keterangan |
|---|---|---|---|---|---|---|
| id | UUID/int | Ya | Ya | auto | – | Kunci utama |
| [field] | [tipe] | Ya/Tidak | Ya/Tidak | [nilai] | [aturan] | [fungsi bisnis field ini] |

**Aturan pada entitas ini:**

- BR-xxx: [aturan]

**Indeks yang dibutuhkan:**

| Field | Alasan (query yang sering) |
|---|---|
| [field] | [alasan] |

**Relasi:**

| Ke entitas | Jenis | Aturan | Kalau induk dihapus |
|---|---|---|---|
| [entitas] | 1-N / N-N / 1-1 | [penjelasan] | [cascade / restrict / set null] |

---

## 4. Diagram relasi (ERD)

```
[Ganti dengan ERD proyek ini]

Contoh bentuk:

  PELANGGAN ──1:N──▶ PENJUALAN ──1:N──▶ ITEM_PENJUALAN
                          │                    │
                          │                    └──N:1──▶ PRODUK
                          └──N:1──▶ PENGGUNA
```

Aturan:

- Tandai kardinalitas dengan jelas (1:1, 1:N, N:N).
- N:N harus dipecah jadi dua 1:N lewat tabel penghubung.
- Setiap garis harus bisa dijelaskan dalam satu kalimat bisnis.

---

## 5. Siklus hidup data

Untuk entitas transaksi, jelaskan perjalanan datanya.

| Tahap | Apa yang terjadi | Siapa yang bisa melakukan | Data yang berubah |
|---|---|---|---|
| Dibuat | [kondisi] | [peran] | [field] |
| Diubah | [kondisi + batas waktu] | [peran] | [field] |
| Dikunci | [kondisi, contoh: setelah dibayar] | – | Field tertentu tidak bisa diubah |
| Diarsipkan | [kondisi] | [peran/sistem] | Pindah ke arsip, tetap bisa dibaca |
| Dihapus | [kondisi, atau "tidak pernah dihapus"] | [peran] | [dampak] |

Aturan umum yang aman: untuk data transaksi, **arsipkan, jangan hapus**. Kalau harus dihapus, gunakan penghapusan lunak (`deleted_at`) agar jejak audit tetap ada.

---

## 6. Aturan integritas

| # | Aturan | Ditegakkan di mana | Kalau dilanggar |
|---|---|---|---|
| 1 | [contoh: total transaksi = jumlah semua item dikurangi diskon] | [aplikasi/database] | [penanganan] |
| 2 | [contoh: stok tidak boleh negatif] | [aplikasi + transaksi DB] | [penanganan] |
| 3 | [contoh: satu email hanya boleh dipakai satu pengguna] | [database unique constraint] | [pesan error] |

Aturan penting: **integritas ditegakkan di database/aplikasi, bukan hanya di tampilan.**

---

## 7. Aturan transisi status

### [Entitas] — status

| Status | Arti | Boleh berubah ke | Aktor | Efek samping |
|---|---|---|---|---|
| [status] | [arti] | [status berikutnya] | [peran] | [dampak ke data lain] |

---

## 8. Referensi data

| Kode | Nilai | Dipakai di | Bisa ditambah pengguna? |
|---|---|---|---|
| [kategori] | [daftar nilai tetap] | [fitur] | [Ya/Tidak] |

---

## 9. Migrasi & data awal

| Hal | Isi |
|---|---|
| Data awal yang wajib ada saat sistem pertama jalan | [daftar, contoh: akun admin, kategori dasar] |
| Data lama yang harus dipindahkan | [sumber, format, jumlah perkiraan] |
| Cara memindahkan | [skrip manual/impor] |
| Data lama yang dibuang | [daftar + alasan] |
| Cara memeriksa migrasi berhasil | [perbandingan jumlah/angka kunci] |

---

## 10. Retensi & privasi

| Data | Sensitif? | Berapa lama disimpan | Siapa boleh melihat | Cara menghapus |
|---|---|---|---|---|
| [data] | Ya/Tidak | [durasi] | [peran] | [cara] |

Data yang biasanya sensitif: identitas pelanggan, nomor telepon, alamat, data pembayaran, kredensial.

---

## 11. Konsistensi dengan dokumen lain

- [ ] Setiap `DR-xx` di `02-requirements.md` ada di sini
- [ ] Setiap entitas dipakai minimal satu proses di `04-workflow.md`
- [ ] Setiap aturan `BR-xx` yang menyangkut data punya tempat penegakan
- [ ] Setiap layar di `06-ui-ux.md` mengambil data dari entitas yang ada di sini

---

## 12. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
