# 07 — Test Plan

> Dokumen ini menjawab: **bagaimana kita membuktikan sistemnya benar.** Setiap kasus uji di sini harus bisa dilacak ke requirement di `02-requirements.md`. Kalau sebuah FR tidak punya kasus uji, FR itu tidak pernah terbukti berjalan.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## 1. Strategi pengujian

| Tingkat | Yang diuji | Kapan dijalankan | Otomatis? | Penanggung jawab |
|---|---|---|---|---|
| Uji unit | Fungsi/logika terkecil | Setiap perubahan kode | Ya | Developer |
| Uji integrasi | Interaksi antar komponen (API↔DB) | Sebelum commit | Ya | Developer |
| Uji fungsional | Alur dari sisi pengguna | Per fitur selesai | Sebagian | Developer/Penguji |
| Uji penerimaan | Kesesuaian dengan kebutuhan pengguna | Sebelum rilis | Tidak | Pemilik produk |
| Uji regresi | Fitur lama tidak rusak | Setiap rilis | Ya | Otomatis |
| Uji non-fungsional | Performa, keamanan | Sebelum rilis | Sebagian | Penguji |

---

## 2. Lingkungan pengujian

| Aspek | Isi |
|---|---|
| Lokal | [cara menjalankan] |
| Data uji | [data contoh yang dipakai] |
| Perangkat/browser | [daftar] |
| Akun uji | [peran yang tersedia, jangan tulis kata sandi nyata di dokumen] |

---

## 3. Kasus uji fungsional

Setiap kasus uji memakai struktur: ID, terkait FR, prasyarat, langkah, hasil yang diharapkan, hasil nyata.

**TC-001 — [judul kasus]**

- **Terkait:** FR-001 / AC-001
- **Prioritas:** P0
- **Prasyarat:** [kondisi sebelum diuji]
- **Data uji:** [data yang dipakai]

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | [aksi] | [hasil] |
| 2 | [aksi] | [hasil] |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Lulus / Gagal / Belum diuji
- **Catatan:** [bukti: tangkapan layar, log]

<!-- EXAMPLE-START -->
Contoh:
**TC-002 — Sistem menolak pembayaran kurang dari total**

- **Terkait:** FR-002 / AC-002
- **Prioritas:** P0
- **Prasyarat:** Ada produk dengan harga 25.000, kasir berada di halaman transaksi
- **Data uji:** total transaksi 25.000, jumlah bayar 20.000

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Masukkan produk dengan harga 25.000 ke keranjang | Keranjang menampilkan total 25.000 |
| 2 | Isi jumlah bayar 20.000 | Kolom bayar menerima angka 20.000 |
| 3 | Tekan tombol "Bayar" | Sistem menolak, menampilkan selisih kurang 5.000, transaksi tidak tersimpan |
<!-- EXAMPLE-END -->

---

## 4. Matriks cakupan uji

| FR | Kriteria penerimaan | Kasus uji | Status |
|---|---|---|---|
| FR-001 | AC-001 | TC-001 | [ ] |
| FR-002 | AC-002 | TC-002 | [ ] |

Aturan: setiap FR prioritas P0 **wajib** punya minimal satu `TC-xx`.

---

## 5. Kasus uji jalur tidak normal

Justru di sinilah bug biasanya bersembunyi. Wajib ada, bukan opsional.

| # | Kondisi | Kasus uji | Hasil yang diharapkan |
|---|---|---|---|
| 1 | Input kosong pada kolom wajib | TC-0xx | Ditolak dengan pesan jelas, tidak tersimpan |
| 2 | Data ganda (nomor/email sama) | TC-0xx | Ditolak dengan pesan yang menyebut data mana yang bentrok |
| 3 | Aksi ganda cepat (klik dua kali) | TC-0xx | Hanya satu data yang tercipta |
| 4 | Hak akses tidak sesuai | TC-0xx | Ditolak di server, bukan hanya disembunyikan |
| 5 | Koneksi terputus saat menyimpan | TC-0xx | Data konsisten, pengguna diberi tahu, bisa mencoba lagi |
| 6 | Angka tak wajar (nol, negatif, sangat besar) | TC-0xx | Ditolak atau ditangani sesuai aturan |
| 7 | Data hilang / sudah dihapus oleh pengguna lain | TC-0xx | Pesan jelas, tidak error teknis |
| 8 | Input dengan karakter khusus / sangat panjang | TC-0xx | Aman, tidak merusak tampilan atau query |

---

## 6. Kasus uji non-fungsional

| NFR | Cara uji | Alat | Target | Hasil |
|---|---|---|---|---|
| NFR-001 (performa) | [metode] | [alat] | [target] | [hasil] |
| NFR-003 (keamanan) | [metode] | [alat] | [target] | [hasil] |

---

## 7. Uji penerimaan pengguna

| # | Skenario nyata | Siapa yang menguji | Kriteria diterima |
|---|---|---|---|
| 1 | [tugas nyata dari pekerjaan sehari-hari] | [peran] | [kondisi] |

Uji penerimaan memakai tugas nyata, bukan klik tombol satu-satu. Contoh: "kasir menyelesaikan 10 transaksi berturut-turut tanpa bantuan".

---

## 8. Kriteria keluar (exit criteria)

Rilis dinyatakan layak kalau:

- [ ] 100% kasus uji P0 statusnya Lulus
- [ ] Tidak ada bug keparahan kritis terbuka
- [ ] Bug keparahan tinggi punya rencana perbaikan dengan tanggal
- [ ] Semua alur error utama sudah dicoba
- [ ] Dokumen `03`–`06` sudah disesuaikan dengan kenyataan kode

---

## 9. Log cacat

| ID | Deskripsi | Terkait | Keparahan | Langkah reproduksi | Status | Perbaikan |
|---|---|---|---|---|---|---|
| BUG-001 | [deskripsi] | FR-00x | Kritis/Tinggi/Sedang/Rendah | [langkah] | Terbuka/Diperbaiki/Tertutup | [ringkas] |

Definisi keparahan:

- **Kritis** — data hilang/salah, atau alur utama tidak jalan sama sekali
- **Tinggi** — ada cara memakai tapi menyusahkan, atau hasil salah pada kasus tertentu
- **Sedang** — mengganggu tapi ada jalan lain
- **Rendah** — kosmetik, teks, tata letak

---

## 10. Bukti pengujian

| Kasus uji | Tanggal | Pelaksana | Bukti | Catatan |
|---|---|---|---|---|
| TC-001 | [tanggal] | [nama] | [tautan berkas/tangkapan layar] | [catatan] |

Aturan: klaim "sudah diuji" tanpa bukti dihitung belum diuji.

---

## 11. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
