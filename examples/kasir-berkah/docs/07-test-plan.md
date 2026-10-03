# 07 — Test Plan

> Dokumen ini menjawab: **bagaimana kita membuktikan sistemnya benar.** Setiap kasus uji di sini harus bisa dilacak ke requirement di `02-requirements.md`. Kalau sebuah FR tidak punya kasus uji, FR itu tidak pernah terbukti berjalan.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

---

## 1. Strategi pengujian

| Tingkat | Yang diuji | Kapan dijalankan | Otomatis? | Penanggung jawab |
|---|---|---|---|---|
| Uji unit | Fungsi logika: validasi qty (BR-001), hitung total (BR-003), kembalian (BR-004), stok (BR-005) | Setiap perubahan kode | Ya (`unittest`) | Developer |
| Uji integrasi | Lapisan logika ↔ SQLite: simpan transaksi + baris + perubahan stok dalam satu transaksi | Sebelum commit | Ya (`unittest`) | Developer |
| Uji fungsional | Setiap perintah CLI dari sisi pengguna pada basis data sementara | Per fitur selesai | Sebagian (CLI dijalankan di uji) | Developer/Penguji |
| Uji penerimaan | Kasir menyelesaikan transaksi nyata; pemilik menjalankan rekap | Sebelum rilis | Tidak | Pemilik |
| Uji regresi | Semua TC-001…TC-012 tiap kali ada perubahan | Setiap rilis | Ya | Otomatis |
| Uji non-fungsional | NFR-001…NFR-005 | Sebelum rilis | Sebagian | Penguji |

Perintah menjalankan uji otomatis:

```
python -m unittest discover -s tests -v
```

---

## 2. Lingkungan pengujian

| Aspek | Isi |
|---|---|
| Lokal | `cd <folder proyek>` lalu `python -m unittest discover -s tests -v`; uji memakai basis data sementara lewat env `KASIR_DB` |
| Data uji | Produk contoh: `BRS-5KG` (harga 65000, stok 20), `MNY-1L` (harga 18000, stok 30), `GLA-1KG` (harga 15000, stok 10) |
| Perangkat/browser | Komputer/laptop toko; tidak ada browser (CLI) |
| Akun uji | Tidak ada login. Peran diuji lewat argumen peran pada alur (kasir = semua kecuali `batal`; pemilik = termasuk `batal`) |

Aturan: setiap uji dijalankan pada basis data sementara (bukan `kasir.db` nyata), supaya data toko tidak terganggu.

---

## 3. Kasus uji fungsional

Setiap kasus uji memakai struktur: ID, terkait FR, prasyarat, langkah, hasil yang diharapkan, hasil nyata.

**TC-001 — Daftar produk menampilkan SKU, nama, harga, stok**

- **Terkait:** FR-001 / AC-001
- **Prioritas:** P0
- **Prasyarat:** Produk `BRS-5KG` (65000, stok 20) dan `MNY-1L` (18000, stok 30) sudah ditambahkan
- **Data uji:** dua produk di atas

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | `python -m app produk tambah --sku BRS-5KG --nama "Beras 5 kg" --harga 65000 --stok 20` | Keluar kode 0, produk tersimpan |
| 2 | `python -m app produk daftar` | Daftar menampilkan `BRS-5KG  Beras 5 kg  Rp65.000  20` dan baris produk kedua lengkap |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-002 — Catat satu transaksi dengan beberapa baris item**

- **Terkait:** FR-002 / AC-002
- **Prioritas:** P0
- **Prasyarat:** `BRS-5KG` dan `MNY-1L` tersedia dengan stok cukup
- **Data uji:** `BRS-5KG:1`, `MNY-1L:2`, bayar 100000

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | `python -m app jual --produk BRS-5KG:1 --produk MNY-1L:2 --bayar 100000 --kasir "Nadia"` | Keluar kode 0; transaksi tersimpan dengan dua baris |
| 2 | `python -m app rekap --tanggal <hari ini>` | Jumlah transaksi bertambah 1; total item terjual bertambah 3 |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-003 — Nomor transaksi unik dan berurutan per hari**

- **Terkait:** FR-003 / AC-003 / NFR-004
- **Prioritas:** P0
- **Prasyarat:** Hari ini belum ada transaksi
- **Data uji:** dua transaksi valid

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Simpan transaksi pertama | Kode `TRX-YYYYMMDD-001` |
| 2 | Simpan transaksi kedua | Kode `TRX-YYYYMMDD-002` (berurutan, tidak sama) |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-004 — Total dihitung dari seluruh baris**

- **Terkait:** FR-004 / AC-004 / BR-003
- **Prioritas:** P0
- **Prasyarat:** `BRS-5KG` harga 65000; `MNY-1L` harga 18000
- **Data uji:** `BRS-5KG:1`, `MNY-1L:2`

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Simpan transaksi `BRS-5KG:1` + `MNY-1L:2`, bayar 120000 | Total ditampilkan 101000 (65000 + 36000) |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-005 — Kembalian dihitung dari bayar dikurangi total**

- **Terkait:** FR-005 / AC-005 / BR-004
- **Prioritas:** P0
- **Prasyarat:** Total transaksi diketahui 101000
- **Data uji:** bayar 120000

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Simpan transaksi dengan total 101000, bayar 120000 | Kembalian ditampilkan 19000 |
| 2 | Coba bayar 100000 untuk total 101000 | Ditolak, kode keluar 1, pesan menyebut selisih 1000 |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-006 — Stok berkurang tepat sebesar qty**

- **Terkait:** FR-006 / AC-006 / BR-005
- **Prioritas:** P0
- **Prasyarat:** `BRS-5KG` stok 20
- **Data uji:** `BRS-5KG:3`

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | `produk daftar` sebelum jual | Stok `BRS-5KG` = 20 |
| 2 | Jual `BRS-5KG:3`, bayar 200000 | Transaksi tersimpan |
| 3 | `produk daftar` sesudah jual | Stok `BRS-5KG` = 17 |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-007 — Jual melebihi stok ditolak**

- **Terkait:** FR-007 / AC-007 / BR-005
- **Prioritas:** P0
- **Prasyarat:** `BRS-5KG` stok 2
- **Data uji:** `BRS-5KG:5`

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Jual `BRS-5KG:5` | Ditolak, kode keluar 1, pesan menyebut stok tersedia (2) |
| 2 | `produk daftar` | Stok `BRS-5KG` tetap 2; tidak ada transaksi tersimpan |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah; ini kasus gagal wajib yang diminta kontrak]

**TC-008 — Rekap harian menampilkan tiga angka**

- **Terkait:** FR-008 / AC-008
- **Prioritas:** P0
- **Prasyarat:** Ada dua transaksi SELESAI pada satu tanggal
- **Data uji:** tanggal yang sama dengan dua transaksi

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | `python -m app rekap --tanggal <tanggal>` | Menampilkan jumlah transaksi, total penjualan, total item terjual |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-009 — Rekap hanya menghitung transaksi SELESAI**

- **Terkait:** FR-009 / AC-009
- **Prioritas:** P0
- **Prasyarat:** Pada satu tanggal ada satu transaksi SELESAI dan satu DIBATALKAN
- **Data uji:** transaksi SELESAI + transaksi yang sudah dibatalkan

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | `rekap --tanggal <tanggal>` | Jumlah transaksi = 1; total penjualan tidak memasukkan transaksi batal |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-010 — Batal dengan alasan cukup; pembatalan kedua ditolak**

- **Terkait:** FR-010 / FR-012 / AC-010 / AC-012 / BR-006 / BR-007
- **Prioritas:** P0
- **Prasyarat:** Transaksi `TRX-...-001` berstatus SELESAI
- **Data uji:** alasan `"salah input"`; lalu percobaan kedua; lalu alasan `"xx"`

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | `batal --kode TRX-...-001 --alasan "salah input"` | Berhasil; status DIBATALKAN; alasan tersimpan |
| 2 | `batal --kode TRX-...-001 --alasan "salah lagi"` | Ditolak, kode keluar 1, pesan transaksi sudah dibatalkan |
| 3 | `batal --kode TRX-...-002 --alasan "xx"` | Ditolak, kode keluar 1, pesan alasan minimal 5 karakter |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah; dua kasus gagal wajib dari kontrak]

**TC-011 — Stok kembali setelah pembatalan**

- **Terkait:** FR-011 / AC-011 / BR-008
- **Prioritas:** P0
- **Prasyarat:** `BRS-5KG` stok 17 setelah penjualan 3
- **Data uji:** transaksi yang menjual `BRS-5KG:3`

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Batalkan transaksi yang menjual `BRS-5KG:3` | Stok `BRS-5KG` kembali menjadi 20 |
| 2 | `produk daftar` | Stok `BRS-5KG` = 20 |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

**TC-012 — Pembatalan mengeluarkan transaksi dari rekap**

- **Terkait:** FR-012 / FR-009 / BR-006
- **Prioritas:** P0
- **Prasyarat:** Ada transaksi SELESAI yang lalu dibatalkan pada satu tanggal
- **Data uji:** tanggal dengan transaksi yang dibatalkan

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Catat total rekap sebelum batal | Total = X |
| 2 | Batalkan transaksi | Berhasil |
| 3 | `rekap --tanggal <tanggal>` | Total turun sebesar nilai transaksi yang dibatalkan |

- **Hasil nyata:** [diisi saat eksekusi]
- **Status:** Belum diuji
- **Catatan:** [bukti: keluaran perintah]

---

## 4. Matriks cakupan uji

| FR | Kriteria penerimaan | Kasus uji | Status |
|---|---|---|---|
| FR-001 | AC-001 | TC-001 | [ ] |
| FR-002 | AC-002 | TC-002 | [ ] |
| FR-003 | AC-003 | TC-003 | [ ] |
| FR-004 | AC-004 | TC-004 | [ ] |
| FR-005 | AC-005 | TC-005 | [ ] |
| FR-006 | AC-006 | TC-006 | [ ] |
| FR-007 | AC-007 | TC-007 | [ ] |
| FR-008 | AC-008 | TC-008 | [ ] |
| FR-009 | AC-009 | TC-009 | [ ] |
| FR-010 | AC-010 | TC-010 | [ ] |
| FR-011 | AC-011 | TC-011 | [ ] |
| FR-012 | AC-012 | TC-010, TC-012 | [ ] |

Evaluasi matriks:

| Uji | Hasil |
|---|---|
| FR yang tidak punya TC | Tidak ada. FR-001…FR-012 semuanya tercakup. |
| TC yang tidak terkait FR | Tidak ada. TC-001…TC-012 semuanya menunjuk FR. |
| TC di luar happy path | TC-005 (bayar kurang), TC-007 (stok kurang), TC-010 (batal kedua & alasan pendek), TC-003 (duplikasi kode) |
| FR dengan lebih dari satu TC | FR-010 & FR-012 diuji lewat jalur normal (TC-010 langkah 1) dan jalur tolak (TC-010 langkah 2, TC-012) |

Aturan: setiap FR prioritas P0 **wajib** punya minimal satu `TC-xx`. Terpenuhi.

---

## 5. Kasus uji jalur tidak normal

Justru di sinilah bug biasanya bersembunyi. Wajib ada, bukan opsional.

| # | Kondisi | Kasus uji | Hasil yang diharapkan |
|---|---|---|---|
| 1 | Kolom/nama kosong pada argumen wajib (`--nama ""`, `--kasir ""`) | TC-013 | Ditolak dengan pesan jelas, kode keluar 1, tidak tersimpan |
| 2 | Duplikat SKU saat `produk tambah` (BR-010) | TC-014 | Ditolak, pesan menyebut SKU sudah dipakai |
| 3 | Qty 0 atau negatif (BR-001) | TC-015 | Ditolak, pesan qty harus bilangan bulat > 0 |
| 4 | Bayar kurang dari total (BR-004) | TC-005 langkah 2 | Ditolak, pesan menyebut selisih kurang |
| 5 | Stok kurang dari qty (BR-005) | TC-007 | Ditolak, pesan menyebut stok tersedia |
| 6 | SKU duplikat dalam satu transaksi (BR-009) | TC-016 | Ditolak, pesan menyebut SKU muncul lebih dari sekali |
| 7 | Batal kedua kali atas transaksi yang sama (BR-006) | TC-010 langkah 2 | Ditolak, kode keluar 1 |
| 8 | Alasan pembatalan < 5 karakter (BR-007) | TC-010 langkah 3 | Ditolak, kode keluar 1 |
| 9 | Angka tidak masuk akal (harga/stok negatif, bayar sangat besar) | TC-017 | Harga/stok negatif ditolak; bayar besar tetap dihitung benar (kembalian besar) |
| 10 | Qty bukan bilangan bulat (mis. `BRS-5KG:1.5`) | TC-018 | Ditolak, pesan qty harus bilangan bulat |
| 11 | Format tanggal salah pada `rekap` (mis. `03-10-2026`) | TC-019 | Ditolak, kode keluar 1, contoh format yang benar ditampilkan |
| 12 | Kode transaksi tidak ditemukan saat `batal` | TC-020 | Ditolak, pesan transaksi tidak ditemukan |
| 13 | Salah pemakaian perintah (argumen tidak dikenal, subperintah salah) | TC-021 | Keluar kode 2, menampilkan cara pakai |
| 14 | SKU tidak ada saat `jual` | TC-022 | Ditolak, pesan menyarankan `produk daftar` |
| 15 | Tanggal rekap tanpa transaksi | TC-023 | Bukan error; menampilkan angka nol dengan kalimat netral |

Setiap kasus di atas wajib punya hasil yang jelas: **ditolak** atau **disimpan**, tidak boleh "kadang-kadang".

---

## 6. Kasus uji non-fungsional

| NFR | Cara uji | Alat | Target | Hasil |
|---|---|---|---|---|
| NFR-001 (data tetap ada) | Simpan transaksi, tutup proses, buka lagi, jalankan `produk daftar` & `rekap` | terminal + SQLite | Data sama sebelum & sesudah | [belum diuji] |
| NFR-002 (tanpa internet) | Matikan jaringan, jalankan alur inti | terminal | Semua perintah P0 tetap berfungsi | [belum diuji] |
| NFR-003 (pesan Indonesia) | Jalankan seluruh kasus gagal di bagian 5, periksa pesan | terminal | 100% pesan Bahasa Indonesia, menyebut penyebab + tindakan, keluar di stderr | [belum diuji] |
| NFR-004 (nomor unik berurutan) | Simpan beberapa transaksi berurutan dalam satu hari | terminal | Kode `...-001`, `...-002`, `...-003`; tidak ada duplikat | [belum diuji] |
| NFR-005 (performa simpan < 1 detik) | Ukur waktu perintah `jual` pada perangkat toko nyata | `time` / pencatatan manual | < 1 detik `[asumsi — perlu diukur]` | [belum diuji; menunggu Q-04] |

---

## 7. Uji penerimaan pengguna

| # | Skenario nyata | Siapa yang menguji | Kriteria diterima |
|---|---|---|---|
| 1 | Kasir menyelesaikan 10 transaksi berturut-turut tanpa bantuan dan tanpa menulis nota | Kasir | 10 transaksi tersimpan; kembalian benar tiap kali; tidak kembali ke nota kertas |
| 2 | Pemilik menutup toko: jalankan `rekap` untuk hari itu | Pemilik | Rekap keluar < 1 menit dan angkanya cocok dengan pengamatan |
| 3 | Pemilik membatalkan satu transaksi salah input dengan alasan | Pemilik | Transaksi keluar dari rekap; stok kembali; tidak bisa dibatalkan dua kali |
| 4 | Kasir mencoba menjual barang yang stoknya habis | Kasir | Ditolak dengan pesan yang jelas; kasir tahu harus berkata apa ke pelanggan |

Uji penerimaan memakai tugas nyata, bukan klik tombol satu-satu.

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
| BUG-001 | *contoh format, diisi saat ada temuan nyata* | FR-00x | Kritis/Tinggi/Sedang/Rendah | [langkah] | Terbuka/Diperbaiki/Tertutup | [ringkas] |

Definisi keparahan:

- **Kritis** — data hilang/salah, atau alur utama tidak jalan sama sekali
- **Tinggi** — ada cara memakai tapi menyusahkan, atau hasil salah pada kasus tertentu
- **Sedang** — mengganggu tapi ada jalan lain
- **Rendah** — kosmetik, teks, tata letak

Belum ada temuan; baris BUG-001 hanya penanda format sampai pengujian dijalankan.

---

## 10. Bukti pengujian

| Kasus uji | Tanggal | Pelaksana | Bukti | Catatan |
|---|---|---|---|---|
| TC-001…TC-023 | [tanggal eksekusi] | [nama] | `examples/kasir-berkah/bukti/` (keluaran perintah apa adanya) | [catatan] |

Aturan: klaim "sudah diuji" tanpa bukti dihitung belum diuji. Bukti disimpan apa adanya (keluaran perintah), bukan rangkuman.

---

## 11. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |