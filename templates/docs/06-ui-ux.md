# 06 — UI/UX

> Dokumen ini menjawab: **apa yang dilihat pengguna, apa yang bisa dia lakukan, dan apa yang terjadi saat sesuatu gagal.** Bagian yang paling sering dilupakan di dokumen lain — dan paling sering ditebak salah oleh AI — adalah kondisi kosong, kondisi memuat, dan kondisi error. Di sini wajib ditulis.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## 1. Prinsip desain

Batasi 4–6 prinsip. Prinsip di sini yang dipakai untuk menilai semua keputusan tampilan.

| # | Prinsip | Konsekuensi praktis |
|---|---|---|
| D-1 | Tugas utama selesai dengan langkah paling sedikit | [contoh: transaksi ≤4 interaksi] |
| D-2 | Kesalahan dicegah, bukan hanya diberitahu | [contoh: kolom terkunci sesuai peran] |
| D-3 | Status selalu jelas | [contoh: setiap baris punya label status] |

---

## 2. Konteks pemakaian

| Aspek | Isi | Implikasi desain |
|---|---|---|
| Perangkat utama | [desktop/HP/tablet] | [target ukuran, tata letak] |
| Tempat pemakaian | [contoh: depan pelanggan, di gudang] | [kontras, ukuran tombol] |
| Tingkat ketergesaan | [tinggi/sedang] | [jumlah klik, shortcut] |
| Kualitas jaringan | [stabil/tidak stabil] | [penanganan offline/loading] |
| Kemampuan pengguna | [rendah/menengah/tinggi] | [tingkat panduan di layar] |

---

## 3. Daftar layar

| ID | Layar | Tujuan | Persona | Data yang ditampilkan | Aksi utama | FR terkait | Prioritas |
|---|---|---|---|---|---|---|---|
| S-01 | [contoh: Halaman Transaksi] | [tujuan] | [persona] | [data] | [aksi] | FR-001 | P0 |

---

## 4. Detail layar

Ulangi blok berikut untuk setiap layar prioritas. Layar P0 wajib lengkap.

### S-01 — [Nama layar]

**Tujuan:** [satu kalimat]
**Masuk dari:** [layar/menu sebelumnya]
**Keluar ke:** [layar berikutnya]

**Tata letak:**

| Area | Isi | Fungsi |
|---|---|---|
| Atas | [judul, aksi global] | [fungsi] |
| Utama | [konten] | [fungsi] |
| Samping | [panel] | [fungsi] |

**Elemen interaktif:**

| Elemen | Jenis | Aksi | Validasi | Kondisi aktif/nonaktif |
|---|---|---|---|---|
| [nama tombol] | tombol | [yang terjadi] | [syarat] | [kapan bisa diklik] |

<!-- EXAMPLE-START -->
Contoh terisi dari proyek "Kasir Berkah" (versi lengkap: `examples/kasir-berkah/docs/06-ui-ux.md`). Blok ini dibuang saat `--strip-examples`. Untuk proyek CLI, "layar" adalah satu perintah beserta keluarannya.

### S-05 — Batal (`python -m app batal --kode TRX-... --alasan "..."`)

**Tujuan:** Membatalkan transaksi salah input, mengembalikan stok, dan mengeluarkannya dari rekap.
**Masuk dari:** terminal.  **Keluar ke:** perintah `rekap` (verifikasi total turun).

**Elemen interaktif:**

| Elemen | Jenis | Aksi | Validasi | Kondisi aktif/nonaktif |
|---|---|---|---|---|
| `--kode` | argumen | Menentukan transaksi | Wajib; harus ada; format `TRX-YYYYMMDD-###` | Hanya berlaku untuk transaksi SELESAI |
| `--alasan` | argumen | Alasan pembatalan | Wajib; ≥ 5 karakter (BR-007) | – |

**Status layar yang WAJIB ditangani:**

| Status | Kapan terjadi | Yang ditampilkan | Ada aksi pemulihan? |
|---|---|---|---|
| Memuat | Saat mengubah status & stok | Tidak ada indikator khusus (operasi lokal < 1 detik) | – |
| Kosong | Tidak berlaku | – | – |
| Kosong karena filter | Kode transaksi tidak ditemukan | `Gagal: transaksi dengan kode '<kode>' tidak ditemukan.` | Ya: cek kode lewat rekap |
| Berhasil | Transaksi SELESAI berhasil dibatalkan | Konfirmasi + daftar stok yang dikembalikan + `Status: DIBATALKAN` | – |
| Gagal validasi | Alasan < 5 karakter | `Gagal: alasan pembatalan minimal 5 karakter.` (kode keluar 1) | Ya: tulis alasan lebih panjang |
| Gagal validasi | Transaksi sudah DIBATALKAN | `Gagal: transaksi <kode> sudah dibatalkan. Pembatalan hanya boleh sekali.` (kode keluar 1) | Tidak ada (memang dilarang) |
| Gagal sistem | Perubahan status gagal disimpan | `Gagal membatalkan transaksi: <alasan>. Status dan stok tidak berubah.` | Ya: coba lagi |
| Tidak punya akses | Peran bukan pemilik | `Gagal: pembatalan hanya boleh dilakukan pemilik.` (kode keluar 1) | Ya: minta pemilik |
| Data besar | Transaksi dengan banyak baris | Semua baris stok yang dikembalikan dicetak | – |
<!-- EXAMPLE-END -->

**Status layar yang WAJIB ditangani:**

| Status | Kapan terjadi | Yang ditampilkan | Ada aksi pemulihan? |
|---|---|---|---|
| Memuat | Saat data sedang diambil | [indikator muat / skeleton] | – |
| Kosong | Saat belum ada data sama sekali | [pesan + ajakan aksi] | Ya: [aksi] |
| Kosong karena filter | Saat pencarian tidak menemukan hasil | [pesan "tidak ditemukan"] | Ya: [reset filter] |
| Berhasil | Setelah aksi selesai | [konfirmasi] | – |
| Gagal validasi | Input tidak sesuai aturan | [pesan di kolom terkait] | Ya: [perbaiki input] |
| Gagal sistem | Server/DB gagal | [pesan + coba lagi] | Ya: [coba lagi] |
| Tidak punya akses | Peran tidak diizinkan | [pesan + arah kembali] | Ya: [kembali] |
| Data besar | Jumlah data banyak | [paginasi/scroll] | – |

**Aturan tampilan:**

- Jangan menampilkan [data sensitif] ke peran [x].
- Kolom [x] hanya bisa diubah selama status [y].
- Tombol [x] harus minta konfirmasi karena [alasan].

---

## 5. Navigasi

```
[Ganti dengan struktur navigasi proyek ini]

Contoh:

  Login
    └─ Dasbor
        ├─ Transaksi
        ├─ Produk
        ├─ Laporan
        └─ Pengaturan (admin)
```

| Dari | Aksi | Ke | Siapa yang boleh |
|---|---|---|---|
| [layar] | [aksi navigasi] | [layar] | [peran] |

---

## 6. Peran & tampilan

| Peran | Layar yang bisa diakses | Elemen yang disembunyikan | Aksi yang dilarang |
|---|---|---|---|
| [peran] | [daftar] | [daftar] | [daftar] |

Catatan penting: menyembunyikan elemen di UI **bukan** pengamanan. Penegakan hak akses tetap dilakukan di server (lihat `03-architecture.md` bagian otorisasi).

---

## 7. Bahasa & penulisan teks

| Aspek | Aturan | Contoh |
|---|---|---|
| Bahasa antarmuka | [Indonesia/Inggris] | – |
| Nada pesan | [netral, tidak menyalahkan] | "Data belum lengkap" bukan "Input Anda salah" |
| Pesan error | [sebutkan penyebab + cara memperbaiki] | [contoh] |
| Label tombol | [kata kerja, spesifik] | "Simpan Transaksi" bukan "OK" |
| Format angka | [pemisah ribuan, desimal] | [contoh] |
| Format tanggal | [format] | [contoh] |

---

## 8. Umpan balik & keamanan tindakan

| Tindakan | Tingkat risiko | Konfirmasi | Bisa dibatalkan | Pemberitahuan |
|---|---|---|---|---|
| Simpan data | rendah | tidak | ya (edit lagi) | [toast kecil] |
| Hapus data | tinggi | ya, sebutkan nama data | tidak | [dialog konfirmasi] |
| Kirim ke pihak luar | tinggi | ya | tidak | [ringkasan apa yang dikirim] |
| Ubah hak akses | tinggi | ya | ya | [catat di log] |

---

## 9. Aksesibilitas & kenyamanan

Hanya tulis yang relevan dengan konteks pemakaian nyata.

| Aspek | Target | Alasan |
|---|---|---|
| Ukuran teks minimum | [nilai] | [kondisi pengguna/tempat] |
| Kontras | [standar] | [bisa dibaca di cahaya terang] |
| Navigasi keyboard | [didukung/tidak] | [kecepatan kerja kasir] |
| Label kolom wajib | [penanda jelas] | [mengurangi error input] |

---

## 10. Yang belum didesain

Bagian ini mencegah AI "mengisi sendiri" tampilan yang belum diputuskan.

| Layar/fitur | Kenapa belum didesain | Rencana |
|---|---|---|

---

## 11. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
