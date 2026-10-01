# 02 — Requirements

> Dokumen ini adalah **kontrak yang bisa diuji.** Kalau sebuah pernyataan tidak bisa dibuktikan salah, itu bukan requirement — itu harapan. Setiap item di sini punya ID agar bisa dilacak dari fitur → requirement → kode → uji.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## Cara membaca ID

| Prefix | Arti | Contoh |
|---|---|---|
| `US-` | User story (kebutuhan pengguna) | US-001 |
| `FR-` | Functional requirement (yang sistem harus lakukan) | FR-001 |
| `NFR-` | Non-functional requirement (bagaimana sistem harus bersikap) | NFR-001 |
| `BR-` | Business rule (aturan yang mengikat perilaku) | BR-001 |
| `DR-` | Data requirement (data yang wajib ada) | DR-001 |
| `TC-` | Test case (di 07-test-plan.md) | TC-001 |

---

## 1. User stories

Format: **Sebagai** [peran], **saya ingin** [aksi], **supaya** [manfaat].

| ID | User story | Persona | Fitur | Prioritas | Kriteria penerimaan |
|---|---|---|---|---|---|
| US-001 | Sebagai [peran], saya ingin [aksi], supaya [manfaat] | [persona] | F-01 | P0 | AC-001 |

<!-- EXAMPLE-START -->
Contoh:
| US-001 | Sebagai kasir, saya ingin mencatat transaksi penjualan dengan memilih barang dari daftar, supaya saya tidak perlu menulis nama barang secara manual | Kasir | F-01 | P0 | AC-001 |
<!-- EXAMPLE-END -->

---

## 2. Functional requirements

Aturan penulisan: **"Sistem harus ..."** + satu perilaku + hasil yang bisa diamati. Satu requirement = satu hal yang bisa diuji.

| ID | Requirement | Fitur | Prioritas | Sumber | Kriteria penerimaan | Uji |
|---|---|---|---|---|---|---|
| FR-001 | Sistem harus [perilaku] ketika [kondisi] | F-01 | P0 | US-001 | AC-001 | TC-001 |

<!-- EXAMPLE-START -->
Contoh:
| FR-001 | Sistem harus menampilkan daftar produk yang cocok dengan kata kunci yang diketik kasir | F-01 | P0 | US-001 | AC-001 | TC-001 |
| FR-002 | Sistem harus menolak transaksi bila jumlah bayar kurang dari total dan menampilkan selisihnya | F-01 | P0 | US-001 | AC-002 | TC-002 |
<!-- EXAMPLE-END -->

Requirement yang **tidak boleh** ditulis seperti ini:

- ❌ "Sistem harus user-friendly." → tidak bisa diuji. Ganti: "Sistem harus menyelesaikan proses penjualan dalam ≤4 interaksi dari pemilihan produk sampai cetak struk."
- ❌ "Sistem harus cepat." → tidak jelas ukurannya. Ganti: lihat NFR-001.
- ❌ "Sistem harus menangani semua kemungkinan error." → tidak terbatas. Sebutkan error yang dimaksud.

---

## 3. Kriteria penerimaan

Format Gherkin agar bisa langsung jadi kasus uji.

**AC-001 — [judul singkat]**
Terhubung ke: FR-001

```
Diberikan  [kondisi awal]
Ketika    [aksi pengguna]
Maka      [hasil yang diharapkan]
```

<!-- EXAMPLE-START -->
Contoh:
**AC-001 — Pencarian produk menampilkan hasil yang cocok**
Terhubung ke: FR-001

```
Diberikan  kasir berada di halaman transaksi dan ada produk "Buku Tulis 38"
Ketika    kasir mengetik "buku" pada kolom pencarian
Maka      sistem menampilkan daftar produk yang namanya mengandung "buku"
Dan       daftar muncul dalam waktu kurang dari 1 detik
```
<!-- EXAMPLE-END -->

---

## 4. Non-functional requirements

Hanya tulis NFR yang **benar-benar dibutuhkan**. Jangan mengarang angka demi kelengkapan.

| ID | Kategori | Requirement | Target terukur | Alasan (kenapa angka ini) | Cara verifikasi |
|---|---|---|---|---|---|
| NFR-001 | Performa | Sistem harus merespons [aksi] dalam waktu [x] | < [x] detik pada [kondisi data] | [kondisi nyata pengguna] | [uji] |
| NFR-002 | Ketersediaan | Sistem harus tersedia selama jam operasional [jam] | ≥ [x]% uptime | [jam operasional bisnis] | [metode] |
| NFR-003 | Keamanan | Sistem harus [aturan akses/enkripsi] | [standar] | [risiko yang dihindari] | [uji] |
| NFR-004 | Keterpakaian | Sistem harus dapat [dilakukan] oleh pengguna baru tanpa pelatihan | [skenario] | [kemampuan pengguna] | [uji] |
| NFR-005 | Auditabilitas | Sistem harus merekam [perubahan] beserta [siapa/kapan] | [detail] | [kebutuhan kontrol] | [uji] |

Kategori yang tersedia: performa, ketersediaan, keandalan, keamanan, keterpakaian, aksesibilitas, pemeliharaan, skalabilitas, kompatibilitas, auditabilitas, pemulihan, privasi.

Kalau kebutuhan belum jelas, tulis `[belum dibutuhkan sekarang]` — bukan angka asal.

---

## 5. Business rules

Aturan yang mengikat proses, terlepas dari tampilan aplikasi. AI wajib menegakkan aturan ini di mana pun relevan.

| ID | Aturan | Sumber aturan | Kalau dilanggar |
|---|---|---|---|
| BR-001 | [ktata] | [kebijakan bisnis / kesepakatan] | [apa yang terjadi] |

<!-- EXAMPLE-START -->
Contoh:
| BR-001 | Harga jual tidak boleh lebih rendah dari harga beli terakhir tanpa persetujuan pemilik | Kebijakan toko | Transaksi ditolak dan butuh persetujuan |
| BR-002 | Stok tidak boleh negatif; penjualan melebihi stok harus dicegah | Kebijakan gudang | Sistem menolak transaksi |
| BR-003 | Diskon karyawan maksimal 20% dan hanya untuk pegawai aktif | Kebijakan HR | Diskon dibatasi otomatis |
<!-- EXAMPLE-END -->

### 5.1 Aturan transisi status

| Entitas | Dari status | Ke status | Pemicu | Syarat | Aktor yang boleh |
|---|---|---|---|---|---|
| [entitas] | [status] | [status] | [event] | [syarat] | [peran] |

---

## 6. Data requirements

| ID | Data | Sumber | Pemilik data | Wajib? | Aturan validasi | Dipakai untuk |
|---|---|---|---|---|---|---|
| DR-001 | [data] | [siapa/apa yang mengisi] | [peran] | Ya/Tidak | [aturan] | [proses/fitur] |

### 6.1 Kualitas data

| Aspek | Aturan |
|---|---|
| Hanya boleh ada satu data [X] untuk [Y] | [contoh: satu nomor telepon aktif per pelanggan] |
| Data yang wajib diisi | [daftar] |
| Data yang boleh kosong | [daftar] |
| Data yang tidak boleh diubah setelah dibuat | [daftar] |
| [entitas] harus diarsipkan setelah [kondisi], tidak dihapus | [alasan audit] |

---

## 7. Traceability matrix

Tabel ini yang membuktikan tidak ada fitur nganggur dan tidak ada requirement yang terlupa.

| Fitur | User story | FR | NFR | BR | Data | Uji |
|---|---|---|---|---|---|---|
| F-01 | US-001 | FR-001, FR-002 | NFR-001 | BR-002 | DR-001, DR-002 | TC-001, TC-002 |
| F-02 | US-002 | FR-003 | – | – | DR-003 | TC-003 |

### 7.1 Uji kelengkapan

- [ ] Setiap fitur P0 punya minimal satu US dan satu FR
- [ ] Setiap FR P0 punya minimal satu kriteria penerimaan `AC-xx`
- [ ] Setiap FR P0 punya minimal satu kasus uji `TC-xx`
- [ ] Setiap BR punya tempat di kode atau proses yang menegakkannya
- [ ] Tidak ada FR yang tidak terhubung ke fitur mana pun
- [ ] Tidak ada data (`DR-`) yang tidak dipakai proses mana pun

---

## 8. Yang sengaja belum ditentukan

Keputusan yang sengaja ditunda, beserta alasannya. Ini mencegah AI mengisi kekosongan dengan asumsinya sendiri.

| Hal | Kenapa ditunda | Siapa yang memutuskan | Kapan |
|---|---|---|---|

---

## 9. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
