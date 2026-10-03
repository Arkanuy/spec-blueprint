# 08 — Roadmap

> Dokumen ini menjawab: **dikerjakan berurutan bagaimana, dan apa yang dikirim di setiap tahap.** Urutan penting karena AI dan manusia sama-sama mudah kehilangan arah kalau semua dianggap prioritas.

**Proyek:** Kasir Berkah
**Versi:** 0.1
**Terakhir diperbarui:** 2026-10-03

---

## 1. Prinsip urutan pengerjaan

| # | Prinsip | Alasan |
|---|---|---|
| 1 | Yang paling mengurangi risiko dikerjakan lebih dulu | Skema data & aturan bisnis salah lebih mahal diperbaiki setelah CLI jadi |
| 2 | Data & aturan inti sebelum tampilan | Kalau model `products`/`sales`/`sale_items` salah, perintah CLI harus dibongkar |
| 3 | Satu alur utuh selesai sebelum menambah alur baru | Alur `jual` harus tuntas (termasuk stok & kembalian) sebelum `rekap`/`batal` ditambah |
| 4 | Tidak mulai fitur P1 sebelum semua P0 tuntas | Menjaga fokus; F-P1 (ekspor) tidak dikerjakan sekarang |

---

## 2. Fase pengerjaan

### Fase 0 — Fondasi (Spec & Persiapan)

**Tujuan:** semua ketidakpastian besar terjawab dan kerangka teknis siap.

| # | Pekerjaan | Keluaran | Ketergantungan | Perkiraan |
|---|---|---|---|---|
| 0.1 | Isi `00-discovery.md` sampai `02-requirements.md` | Dokumen disetujui pemilik | – | [butuh data] |
| 0.2 | Tetapkan arsitektur & data model | `03` + `05` selesai | 0.1 | [butuh data] |
| 0.3 | Siapkan repo, skema SQLite, dan kerangka `unittest` | `python -m app --help` jalan | 0.2 | [butuh data] |
| 0.4 | Siapkan data contoh (BRS-5KG, MNY-1L, GLA-1KG) | Data uji tersedia | 0.3 | [butuh data] |
| 0.5 | Jawab Q-01 dan Q-04 (volume transaksi & perangkat) | Angka nyata untuk NFR-005 | – | [butuh data] |

**Kriteria selesai fase:** [gate-1](../checklists/gate-1-sebelum-coding.md) lolos semua; Q-01 dan Q-04 terjawab.

### Fase 1 — Alur inti (MVP)

**Tujuan:** satu alur utama (jual) berjalan utuh dari awal sampai akhir, termasuk pengurangan stok.

| # | Fitur | FR terkait | Keluaran yang bisa dilihat | Kriteria selesai |
|---|---|---|---|---|
| 1.1 | F-01 Catat penjualan | FR-001, FR-002, FR-003 | `produk tambah`, `produk daftar`, `jual` menghasilkan transaksi bernomor | TC-001, TC-002, TC-003 lulus |
| 1.2 | F-02 Hitung total & kembalian | FR-004, FR-005 | Keluaran `jual` menampilkan total & kembalian | TC-004, TC-005 lulus |
| 1.3 | F-03 Stok berkurang otomatis | FR-006, FR-007 | Stok di `produk daftar` turun setelah jual | TC-006, TC-007 lulus |

**Kriteria selesai fase:** alur jual selesai tanpa perhitungan manual di luar sistem; semua TC Fase 1 lulus dengan bukti.

### Fase 2 — Melengkapi

**Tujuan:** melengkapi lima fitur P0 dan alur pembatalan.

| # | Fitur | FR terkait | Prioritas | Catatan |
|---|---|---|---|---|
| 2.1 | F-04 Rekap harian | FR-008, FR-009 | P0 | Hitung hanya dari transaksi SELESAI; tangani tanggal tanpa transaksi |
| 2.2 | F-05 Batal transaksi dengan alasan | FR-010, FR-011, FR-012 | P0 | Batal sekali, kembalikan stok, tolak pembatalan kedua & alasan pendek |
| 2.3 | Kode keluar & pesan error Bahasa Indonesia | NFR-003 | P0 | Seluruh kasus gagal punya pesan penyebab + tindakan |

**Kriteria selesai fase:** TC-008…TC-012 dan seluruh kasus non-happy-path di `07-test-plan.md` bagian 5 lulus.

### Fase 3 — Pengerasan & rilis

| # | Pekerjaan | Tujuan |
|---|---|---|
| 3.1 | Perbaikan bug hasil pengujian | Stabilitas |
| 3.2 | Uji penerimaan pengguna nyata (kasir & pemilik) | Kesesuaian kebutuhan |
| 3.3 | Dokumentasi pemasangan & panduan pakai (`README.md`) | Bisa dipakai orang lain |
| 3.4 | Aturan & uji pencadangan `kasir.db` | Data tidak hilang (NFR-001) |

---

## 3. Urutan pekerjaan teknis

Urutan ini membantu AI menentukan langkah berikutnya tanpa bertanya.

```
1. Skema SQLite: products, sales, sale_items + indeks (SKU unik, kode unik)
2. Lapisan data: buka koneksi, baca/tulis, bungkus dalam transaksi DB
3. Model & validasi: qty bulat >0, angka tidak negatif, SKU unik
4. Aturan bisnis (BR-001..BR-010) di lapisan layanan
5. Perintah CLI: produk tambah → produk daftar → jual → rekap → batal
6. Status kosong / gagal validasi / gagal sistem + pesan Bahasa Indonesia + kode keluar
7. Uji unit & integrasi (TC-001..TC-012) di basis data sementara
8. Kasus non-happy-path (TC-013..TC-023)
9. Pengerasan: pencadangan kasir.db, uji NFR-001 & NFR-005
```

Aturan: langkah 1–4 selesai sebelum CLI dibangun, karena CLI hanya lapisan tipis di atas logika bisnis.

---

## 4. Definisi selesai (per fitur)

Sebuah fitur baru boleh dianggap selesai kalau **semua** poin ini benar:

- [ ] Perilaku sesuai FR dan kriteria penerimaan
- [ ] Aturan bisnis terkait ditegakkan di lapisan logika, bukan hanya di CLI
- [ ] Status kosong, dan error sudah ditangani (memuat tidak berlaku untuk operasi lokal < 1 detik)
- [ ] Hak akses diperiksa di lapisan logika (`batal` hanya pemilik)
- [ ] Validasi input ada dan pesannya jelas
- [ ] Kasus uji terkait lulus, dengan bukti
- [ ] Dokumentasi (`02`–`06`) diperbarui kalau ada yang berubah
- [ ] Tidak menambah ketergantungan baru tanpa dicatat di `03-architecture.md`

---

## 5. Yang ditunda

| Item | Kenapa ditunda | Syarat untuk mengerjakan nanti |
|---|---|---|
| Ekspor rekap (F-P1) | Bukan bagian dari lima fitur P0 | Setelah P0 stabil dan pemilik memang ingin mengolah data sendiri |
| Cetak struk ke printer | Butuh perangkat & driver | Pelanggan menuntut bukti cetak |
| Login berbasis password | Satu perangkat, dua aktor saling percaya | Ada kasir tambahan dengan hak berbeda |
| Penyesuaian stok manual | Butuh aturan hak akses + jejak audit | Ada selisih stok yang perlu dibetulkan tanpa transaksi |
| Laporan bulanan | Belum ada keputusan bisnis yang butuh periode itu | Rekap harian terbukti dipakai |

---

## 6. Milestone

| Milestone | Isi | Kriteria tercapai | Target |
|---|---|---|---|
| M1 | Fondasi siap | Gate 1 lolos; Q-01 & Q-04 terjawab | [butuh data] |
| M2 | Alur inti jalan (F-01,F-02,F-03) | TC-001…TC-007 lulus | [butuh data] |
| M3 | Lima fitur P0 siap dipakai | TC-001…TC-023 lulus; Gate 3 lolos | [butuh data] |

Target tanggal belum ditetapkan karena tenggat proyek belum diputuskan pemilik — dicatat sebagai Q-05 di [09-risks.md](09-risks.md).

---

## 7. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | 2026-10-03 | Dokumen dibuat | Awal proyek |