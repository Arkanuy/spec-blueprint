# 02 — Requirements

> Dokumen ini adalah **kontrak yang bisa diuji.** Kalau sebuah pernyataan tidak bisa dibuktikan salah, itu bukan requirement — itu harapan. Setiap item di sini punya ID agar bisa dilacak dari fitur → requirement → kode → uji.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

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

Format: **Sebagai** &lt;peran&gt;, **saya ingin** &lt;aksi&gt;, **supaya** &lt;manfaat&gt;.

| ID | User story | Persona | Fitur | Prioritas | Kriteria penerimaan |
|---|---|---|---|---|---|
| US-001 | Sebagai kasir, saya ingin mencatat penjualan dengan menyebut SKU dan qty, supaya saya tidak perlu menulis nota kertas | Kasir | F-01 | P0 | AC-001 |
| US-002 | Sebagai kasir, saya ingin sistem menghitung total dan kembalian, supaya saya tidak salah hitung saat ramai | Kasir | F-02 | P0 | AC-004 |
| US-003 | Sebagai kasir, saya ingin stok berkurang otomatis saat barang terjual, supaya saya tidak mencatat stok terpisah | Kasir | F-03 | P0 | AC-006 |
| US-004 | Sebagai pemilik, saya ingin melihat rekap harian, supaya saya tidak menghitung nota satu per satu tiap malam | Pemilik | F-04 | P0 | AC-008 |
| US-005 | Sebagai kasir, saya ingin membatalkan transaksi salah input dengan alasan, supaya laporan tidak menggelembung | Kasir | F-05 | P0 | AC-010 |
| US-006 | Sebagai pemilik, saya ingin mengekspor rekap, supaya saya bisa mengolah datanya sendiri | Pemilik | F-P1 | P1 | – |

---

## 2. Functional requirements

Aturan penulisan: **"Sistem harus ..."** + satu perilaku + hasil yang bisa diamati. Satu requirement = satu hal yang bisa diuji.

| ID | Requirement | Fitur | Prioritas | Sumber | Kriteria penerimaan | Uji |
|---|---|---|---|---|---|---|
| FR-001 | Sistem harus menampilkan daftar produk berisi SKU, nama, harga, dan stok | F-01 | P0 | US-001 | AC-001 | TC-001 |
| FR-002 | Sistem harus mencatat satu transaksi penjualan dengan beberapa baris item sekaligus | F-01 | P0 | US-001 | AC-002 | TC-002 |
| FR-003 | Sistem harus memberi nomor transaksi unik berurutan per hari (format `TRX-YYYYMMDD-###`) | F-01 | P0 | US-001 | AC-003 | TC-003 |
| FR-004 | Sistem harus menghitung total transaksi dari jumlah seluruh baris item | F-02 | P0 | US-002 | AC-004 | TC-004 |
| FR-005 | Sistem harus menghitung kembalian dari uang bayar dikurangi total | F-02 | P0 | US-002 | AC-005 | TC-005 |
| FR-006 | Sistem harus mengurangi stok produk sebesar qty yang terjual saat transaksi disimpan | F-03 | P0 | US-003 | AC-006 | TC-006 |
| FR-007 | Sistem harus menolak transaksi yang qty-nya melebihi stok tersedia | F-03 | P0 | US-003 | AC-007 | TC-007 |
| FR-008 | Sistem harus menampilkan rekap harian: jumlah transaksi, total penjualan, total item terjual | F-04 | P0 | US-004 | AC-008 | TC-008 |
| FR-009 | Sistem harus menghitung rekap harian hanya dari transaksi berstatus SELESAI | F-04 | P0 | US-004 | AC-009 | TC-009 |
| FR-010 | Sistem harus membatalkan transaksi berstatus SELESAI bila diberi alasan minimal 5 karakter | F-05 | P0 | US-005 | AC-010 | TC-010 |
| FR-011 | Sistem harus mengembalikan stok produk saat transaksi dibatalkan | F-05 | P0 | US-005 | AC-011 | TC-011 |
| FR-012 | Sistem harus menolak pembatalan kedua atas transaksi yang sudah dibatalkan | F-05 | P0 | US-005 | AC-012 | TC-012 |

Requirement yang **tidak boleh** ditulis seperti ini:

- ❌ "Sistem harus user-friendly." → tidak bisa diuji. Ganti: "Pesan error menyebut penyebab dan langkah perbaikan dalam Bahasa Indonesia" (lihat NFR-003).
- ❌ "Sistem harus cepat." → tidak jelas ukurannya. Ganti: lihat NFR-005.
- ❌ "Sistem harus menangani semua kemungkinan error." → tidak terbatas. Ganti: daftar error konkret di bagian 5 dan 07-test-plan.md.

---

## 3. Kriteria penerimaan

Format Gherkin agar bisa langsung jadi kasus uji.

**AC-001 — Daftar produk terisi benar**
Terhubung ke: FR-001

```
Diberikan  ada dua produk: "BRS-5KG" (Beras 5 kg, harga 65000, stok 20) dan "MNY-1L" (Minyak 1 L, harga 18000, stok 30)
Ketika    kasir menjalankan perintah "produk daftar"
Maka      sistem menampilkan kedua produk dengan SKU, nama, harga, dan stok sesuai data tersimpan
```

**AC-002 — Satu transaksi berisi beberapa baris item**
Terhubung ke: FR-002

```
Diberikan  produk "BRS-5KG" dan "MNY-1L" tersedia dengan stok cukup
Ketika    kasir menjalankan "jual --produk BRS-5KG:1 --produk MNY-1L:2 --bayar 100000 --kasir Nadia"
Maka      sistem menyimpan satu transaksi berisi dua baris item
Dan       baris "BRS-5KG" punya qty 1 dan baris "MNY-1L" punya qty 2
```

**AC-003 — Nomor transaksi unik per hari**
Terhubung ke: FR-003

```
Diberikan  hari ini belum ada transaksi
Ketika    kasir menyimpan transaksi kedua pada hari yang sama
Maka      transaksi pertama bernomor TRX-YYYYMMDD-001 dan transaksi kedua TRX-YYYYMMDD-002
Dan       tidak ada dua transaksi dengan kode yang sama
```

**AC-004 — Total dihitung dari seluruh baris**
Terhubung ke: FR-004

```
Diberikan  "BRS-5KG" harga 65000 dan "MNY-1L" harga 18000
Ketika    kasir menjual BRS-5KG:1 dan MNY-1L:2
Maka      sistem menampilkan total 101000 (65000 + 2 × 18000)
```

**AC-005 — Kembalian dihitung dari bayar dikurangi total**
Terhubung ke: FR-005

```
Diberikan  total transaksi 101000
Ketika    kasir memasukkan bayar 120000
Maka      sistem menampilkan kembalian 19000
Dan       transaksi tidak disimpan bila bayar kurang dari total
```

**AC-006 — Stok berkurang tepat sebesar qty**
Terhubung ke: FR-006

```
Diberikan  "BRS-5KG" stok 20
Ketika    kasir menjual BRS-5KG:3 dan transaksi disimpan
Maka      stok "BRS-5KG" menjadi 17
```

**AC-007 — Jual melebihi stok ditolak**
Terhubung ke: FR-007

```
Diberikan  "BRS-5KG" stok 2
Ketika    kasir mencoba menjual BRS-5KG:5
Maka      sistem menolak transaksi, keluar dengan kode 1, dan menyebut stok tersedia (2)
Dan       stok tidak berubah dan tidak ada transaksi tersimpan
```

**AC-008 — Rekap harian menampilkan tiga angka**
Terhubung ke: FR-008

```
Diberikan  pada tanggal 2026-10-03 ada dua transaksi SELESAI
Ketika    pemilik menjalankan "rekap --tanggal 2026-10-03"
Maka      sistem menampilkan jumlah transaksi 2, total penjualan, dan total item terjual
```

**AC-009 — Hanya transaksi SELESAI yang dihitung**
Terhubung ke: FR-009

```
Diberikan  pada tanggal 2026-10-03 ada satu transaksi SELESAI dan satu transaksi DIBATALKAN
Ketika    pemilik menjalankan "rekap --tanggal 2026-10-03"
Maka      jumlah transaksi pada rekap adalah 1
Dan       total penjualan tidak memasukkan nilai transaksi yang dibatalkan
```

**AC-010 — Batal dengan alasan yang cukup**
Terhubung ke: FR-010

```
Diberikan  transaksi TRX-20261003-001 berstatus SELESAI
Ketika    kasir menjalankan "batal --kode TRX-20261003-001 --alasan \"salah input\""
Maka      status transaksi menjadi DIBATALKAN dan alasan tersimpan
Dan       bila alasan kurang dari 5 karakter, sistem menolak dengan kode keluar 1
```

**AC-011 — Stok kembali setelah pembatalan**
Terhubung ke: FR-011

```
Diberikan  "BRS-5KG" stok 17 setelah penjualan 3
Ketika    transaksi tersebut dibatalkan
Maka      stok "BRS-5KG" kembali menjadi 20
```

**AC-012 — Pembatalan kedua ditolak**
Terhubung ke: FR-012

```
Diberikan  transaksi TRX-20261003-001 sudah berstatus DIBATALKAN
Ketika    kasir menjalankan "batal" untuk kedua kalinya pada transaksi itu
Maka      sistem menolak dengan kode keluar 1 dan pesan bahwa transaksi sudah dibatalkan
Dan       stok tidak bertambah lagi
```

---

## 4. Non-functional requirements

Hanya tulis NFR yang **benar-benar dibutuhkan**. Jangan mengarang angka demi kelengkapan.

| ID | Kategori | Requirement | Target terukur | Alasan (kenapa angka ini) | Cara verifikasi |
|---|---|---|---|---|---|
| NFR-001 | Keandalan | Data tersimpan di SQLite lokal dan tetap ada setelah proses ditutup | 100% transaksi tersimpan; data terbaca setelah program ditutup dan dibuka lagi | Toko tidak punya server; data tidak boleh hilang saat program ditutup | Tutup proses lalu jalankan `produk daftar` & `rekap`, bandingkan dengan sebelum ditutup |
| NFR-002 | Kompatibilitas | Sistem berjalan tanpa koneksi internet | Berfungsi penuh saat jaringan dimatikan | Koneksi toko tidak stabil | Matikan jaringan, jalankan alur inti, pastikan tetap jalan |
| NFR-003 | Keterpakaian | Setiap pesan kesalahan ditulis dalam Bahasa Indonesia dan menyebut apa yang salah + apa yang harus dilakukan | 100% pesan error memuat penyebab + langkah perbaikan, keluar di stderr dengan kode 1 | Kasir bukan orang teknis | Periksa keluaran tiap kasus gagal di 07-test-plan.md |
| NFR-004 | Auditabilitas | Nomor transaksi unik dan berurutan per hari | Tidak pernah ada kode `TRX-YYYYMMDD-###` yang sama; urutan tanpa lompatan untuk hari yang sama | Dibutuhkan agar nota bisa dicocokkan saat ada sengketa | Bandingkan kode transaksi hasil beberapa penjualan berurutan |
| NFR-005 | Performa | Waktu simpan satu transaksi (menulis ke basis data) di bawah 1 detik pada perangkat toko | < 1 detik `[asumsi — perlu diukur di perangkat nyata]` | Kasir melayani antrean sehingga transaksi tidak boleh terasa lambat | Ukur waktu eksekusi perintah `jual` di perangkat toko (Q-04) |

Kategori yang tersedia: performa, ketersediaan, keandalan, keamanan, keterpakaian, aksesibilitas, pemeliharaan, skalabilitas, kompatibilitas, auditabilitas, pemulihan, privasi.

Kalau kebutuhan belum jelas, tulis `[belum dibutuhkan sekarang]` — bukan angka asal. Di proyek ini tidak ada kebutuhan ketersediaan server (NFR ketersediaan tidak berlaku karena aplikasi lokal) dan tidak ada ketersediaan data pribadi (privasi belum berlaku).

---

## 5. Business rules

Aturan yang mengikat proses, terlepas dari tampilan aplikasi. AI wajib menegakkan aturan ini di mana pun relevan.

| ID | Aturan | Sumber aturan | Kalau dilanggar |
|---|---|---|---|
| BR-001 | Qty harus bilangan bulat lebih besar dari 0 | Kesepakatan toko | Transaksi ditolak, kode keluar 1, pesan menyebut qty harus bilangan bulat > 0 |
| BR-002 | Harga satuan diambil dari master produk saat transaksi dibuat, bukan diketik ulang kasir | Agar harga seragam dan tidak bisa dicurangi | Kasir tidak memiliki cara memasukkan harga; sistem memakai harga master |
| BR-003 | Total transaksi = jumlah dari (qty × harga satuan) seluruh baris | Konsistensi rekap | Total tidak cocok; rekap salah |
| BR-004 | Uang bayar harus lebih besar atau sama dengan total; kembalian = bayar − total | Kesepakatan toko | Transaksi ditolak, kode keluar 1, pesan menyebut selisih kurang |
| BR-005 | Sistem tidak boleh menjual melebihi stok tersedia | Kesepakatan toko | Transaksi ditolak, kode keluar 1, pesan menyebut stok tersedia |
| BR-006 | Transaksi berstatus SELESAI hanya boleh dibatalkan satu kali | Kesepakatan toko | Pembatalan kedua ditolak, kode keluar 1 |
| BR-007 | Pembatalan wajib menyertakan alasan minimal 5 karakter | Kesepakatan toko | Pembatalan ditolak, kode keluar 1 |
| BR-008 | Pembatalan mengembalikan stok sebesar qty yang dibatalkan | Konsistensi stok | Stok sistem tidak kembali; barang seperti hilang |
| BR-009 | Transaksi tidak boleh punya dua produk dengan SKU sama dalam satu baris transaksi | Hindari baris ganda yang membingungkan | Transaksi ditolak, kode keluar 1, pesan menyebut SKU ganda |
| BR-010 | SKU produk unik dan tidak boleh diubah setelah produk dipakai di transaksi | Menjaga keterlacakan riwayat | Produk baru ditolak bila SKU sudah ada; SKU terkunci setelah dipakai |

### 5.1 Aturan transisi status

| Entitas | Dari status | Ke status | Pemicu | Syarat | Aktor yang boleh |
|---|---|---|---|---|---|
| sales | DRAFT | SELESAI | Perintah `jual` disimpan | Semua baris valid (BR-001, BR-009), stok cukup (BR-005), bayar ≥ total (BR-004) | Kasir |
| sales | SELESAI | DIBATALKAN | Perintah `batal` | Alasan ≥ 5 karakter (BR-007), transaksi belum pernah dibatalkan (BR-006) | Pemilik (lihat keputusan Q-03) |
| sales | DIBATALKAN | – | Tidak ada | Transisi akhir, tidak boleh berubah lagi (BR-006) | – |

Transisi terlarang: `DIBATALKAN → apa pun`, `SELESAI → SELESAI`, `DRAFT → DIBATALKAN`.

Catatan keputusan: hak membatalkan transaksi dipegang pemilik. Alasannya dan dampaknya ke matriks akses ada di [03-architecture.md](03-architecture.md) bagian 7 dan [10-decisions.md](10-decisions.md) ADR-004. Status akhir transaksi yang dibatalkan tetap tercatat, bukan dihapus.

---

## 6. Data requirements

| ID | Data | Sumber | Pemilik data | Wajib? | Aturan validasi | Dipakai untuk |
|---|---|---|---|---|---|---|
| DR-001 | Produk: sku, nama, harga, stok | Kasir/pemilik lewat `produk tambah` | Pemilik | Ya | SKU unik & tidak diubah setelah dipakai (BR-010); harga & stok bilangan bulat ≥ 0 | FR-001, FR-006, FR-007, FR-011 |
| DR-002 | Baris transaksi: qty, harga_satuan, subtotal | Kasir lewat `jual` (harga disalin dari master) | Kasir | Ya | Qty bilangan bulat > 0 (BR-001); harga_satuan = harga master (BR-002); subtotal = qty × harga (BR-003) | FR-002, FR-004 |
| DR-003 | Kepala transaksi: kode, tanggal, kasir, status | Dibuat sistem saat `jual` | Sistem | Ya | Kode unik format `TRX-YYYYMMDD-###` (FR-003, NFR-004); status ∈ {DRAFT, SELESAI, DIBATALKAN} | FR-002, FR-003, FR-008, FR-009 |
| DR-004 | Uang: total, bayar, kembalian | Sistem menghitung dari baris & masukan kasir | Sistem | Ya | Bayar ≥ total (BR-004); kembalian = bayar − total | FR-004, FR-005 |
| DR-005 | Jejak pembatalan: alasan_batal, dibatalkan_pada | Kasir/pemilik lewat `batal` | Pemilik | Tidak (hanya bila dibatalkan) | Alasan ≥ 5 karakter (BR-007); diisi sekali saat status → DIBATALKAN | FR-010, FR-011, FR-012 |

### 6.1 Kualitas data

| Aspek | Aturan |
|---|---|
| Hanya boleh ada satu data produk untuk satu SKU | SKU unik di tabel `products` (BR-010) |
| Data yang wajib diisi | SKU, nama, harga, stok (produk); kode, status, total, bayar, kembalian, kasir (transaksi); qty, harga_satuan, subtotal (baris) |
| Data yang boleh kosong | `alasan_batal` dan `dibatalkan_pada` (kosong selama transaksi belum dibatalkan) |
| Data yang tidak boleh diubah setelah dibuat | `sku` (setelah dipakai di transaksi), `harga_satuan` dan `subtotal` pada baris, `total`, `bayar`, `kembalian` pada transaksi SELESAI |
| Transaksi tidak boleh dihapus setelah status bukan DRAFT | Alasan audit: transaksi yang dibatalkan harus tetap terlihat beserta alasannya (BR-006, BR-008) |

---

## 7. Traceability matrix

Tabel ini yang membuktikan tidak ada fitur nganggur dan tidak ada requirement yang terlupa.

| Fitur | User story | FR | NFR | BR | Data | Uji |
|---|---|---|---|---|---|---|
| F-01 | US-001 | FR-001, FR-002, FR-003 | NFR-002, NFR-004, NFR-005 | BR-001, BR-002, BR-009, BR-010 | DR-001, DR-002, DR-003 | TC-001, TC-002, TC-003 |
| F-02 | US-002 | FR-004, FR-005 | NFR-003 | BR-003, BR-004 | DR-002, DR-004 | TC-004, TC-005 |
| F-03 | US-003 | FR-006, FR-007 | NFR-001 | BR-005 | DR-001, DR-002 | TC-006, TC-007 |
| F-04 | US-004 | FR-008, FR-009 | NFR-001, NFR-002 | BR-003 | DR-003, DR-004 | TC-008, TC-009 |
| F-05 | US-005 | FR-010, FR-011, FR-012 | NFR-003 | BR-006, BR-007, BR-008 | DR-001, DR-005 | TC-010, TC-011, TC-012 |
| F-P1 | US-006 | – (belum diturunkan) | – | – | – | – |

Catatan: NFR-004 (nomor unik) menyangkut F-01 dan F-05 (kode dipakai saat pembatalan), NFR-005 (performa) menyangkut F-01. NFR-001 (data tetap ada) menyangkut F-03 (stok) dan F-04 (rekap). F-P1 belum punya FR karena ditunda di luar rilis pertama — lihat [01-prd.md](01-prd.md) bagian 6.3.

### 7.1 Uji kelengkapan

- [x] Setiap fitur P0 punya minimal satu US dan satu FR
- [x] Setiap FR P0 punya minimal satu kriteria penerimaan `AC-xx`
- [x] Setiap FR P0 punya minimal satu kasus uji `TC-xx`
- [x] Setiap BR punya tempat di kode atau proses yang menegakkannya
- [x] Tidak ada FR yang tidak terhubung ke fitur mana pun
- [x] Tidak ada data (`DR-`) yang tidak dipakai proses mana pun

Uji kelengkapan ini diperiksa ulang saat rilis; status `[x]` di sini berarti sudah dirancang, bukan berarti sudah diuji di kode.

---

## 8. Yang sengaja belum ditentukan

Keputusan yang sengaja ditunda, beserta alasannya. Ini mencegah AI mengisi kekosongan dengan asumsinya sendiri.

| Hal | Kenapa ditunda | Siapa yang memutuskan | Kapan |
|---|---|---|---|
| Diskon/promo | Menambah aturan harga di luar BR yang disepakati | Pemilik | Setelah rekap harian terbukti dipakai |
| Login berbasis password | Satu perangkat, dua aktor yang saling percaya | Pemilik | Kalau ada kasir tambahan dengan hak berbeda |
| Cetak struk ke printer | Butuh perangkat & driver; belum ada permintaan | Pemilik | Kalau pelanggan menuntut struk |
| Penyesuaian stok manual | Butuh aturan siapa boleh + jejak audit | Pemilik | Kalau selisih stok perlu dibetulkan tanpa transaksi |

---

## 9. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |