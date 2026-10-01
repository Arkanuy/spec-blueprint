# 08 — Roadmap

> Dokumen ini menjawab: **dikerjakan berurutan bagaimana, dan apa yang dikirim di setiap tahap.** Urutan penting karena AI dan manusia sama-sama mudah kehilangan arah kalau semua dianggap prioritas.

**Proyek:** {{PROJECT_NAME}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## 1. Prinsip urutan pengerjaan

| # | Prinsip | Alasan |
|---|---|---|
| 1 | Yang paling mengurangi risiko dikerjakan lebih dulu | Kesalahan asumsi lebih murah diperbaiki di awal |
| 2 | Data & aturan inti sebelum tampilan | Kalau model data salah, UI harus dibongkar |
| 3 | Satu alur utuh selesai sebelum menambah alur baru | Produk setengah jalan di banyak tempat lebih buruk daripada satu alur yang tuntas |
| 4 | Tidak mulai fitur P1 sebelum semua P0 tuntas | Menjaga fokus dan mencegah scope meledak |

---

## 2. Fase pengerjaan

### Fase 0 — Fondasi (Spec & Persiapan)

**Tujuan:** semua ketidakpastian besar terjawab dan kerangka teknis siap.

| # | Pekerjaan | Keluaran | Ketergantungan | Perkiraan |
|---|---|---|---|---|
| 0.1 | Isi `00-discovery.md` sampai `02-requirements.md` | Dokumen disetujui | – | [waktu] |
| 0.2 | Tetapkan arsitektur & data model | `03` + `05` selesai | 0.1 | [waktu] |
| 0.3 | Siapkan repo, lingkungan, CI dasar | Proyek bisa dijalankan | 0.2 | [waktu] |
| 0.4 | Siapkan data contoh | Data uji tersedia | 0.2 | [waktu] |

**Kriteria selesai fase:** [gate-1](../checklists/gate-1-sebelum-coding.md) lolos semua.

### Fase 1 — Alur inti (MVP)

**Tujuan:** satu alur utama berjalan utuh dari awal sampai akhir.

| # | Fitur | FR terkait | Keluaran yang bisa dilihat | Kriteria selesai |
|---|---|---|---|---|
| 1.1 | [F-01] | FR-001 | [hasil nyata] | [kondisi teruji] |
| 1.2 | [F-02] | FR-002 | [hasil nyata] | [kondisi teruji] |

**Kriteria selesai fase:** alur utama selesai tanpa pekerjaan manual di luar sistem; semua TC P0 lulus.

### Fase 2 — Melengkapi

| # | Fitur | FR terkait | Prioritas | Catatan |
|---|---|---|---|---|

**Kriteria selesai fase:** [kondisi]

### Fase 3 — Pengerasan & rilis

| # | Pekerjaan | Tujuan |
|---|---|---|
| 3.1 | Perbaikan bug hasil pengujian | Stabilitas |
| 3.2 | Uji penerimaan pengguna nyata | Kesesuaian kebutuhan |
| 3.3 | Dokumentasi pemasangan & panduan pakai | Bisa dipakai orang lain |
| 3.4 | Deploy produksi + backup | Bisa diandalkan |

---

## 3. Urutan pekerjaan teknis

Urutan ini membantu AI menentukan langkah berikutnya tanpa bertanya.

```
1. Skema database + migrasi
2. Model & validasi data
3. Aturan bisnis (BR) di lapisan logika
4. Endpoint/API inti
5. Layar utama + alur utama
6. Status kosong / memuat / error
7. Fitur P1
8. Pengujian menyeluruh
9. Pengerasan (keamanan, performa, pemulihan)
```

---

## 4. Definisi selesai (per fitur)

Sebuah fitur baru boleh dianggap selesai kalau **semua** poin ini benar:

- [ ] Perilaku sesuai FR dan kriteria penerimaan
- [ ] Aturan bisnis terkait ditegakkan di server, bukan hanya di UI
- [ ] Status kosong, memuat, dan error sudah ditangani
- [ ] Hak akses diperiksa di server
- [ ] Validasi input ada dan pesannya jelas
- [ ] Kasus uji terkait lulus, dengan bukti
- [ ] Dokumentasi (`02`–`06`) diperbarui kalau ada yang berubah
- [ ] Tidak menambah ketergantungan baru tanpa dicatat di `03-architecture.md`

---

## 5. Yang ditunda

| Item | Kenapa ditunda | Syarat untuk mengerjakan nanti |
|---|---|---|
| [fitur] | [alasan] | [kondisi pemicu] |

---

## 6. Milestone

| Milestone | Isi | Kriteria tercapai | Target |
|---|---|---|---|
| M1 | Fondasi siap | Gate 1 lolos | [tanggal] |
| M2 | Alur inti jalan | Semua TC P0 lulus | [tanggal] |
| M3 | Siap dipakai | Gate 3 lolos | [tanggal] |

---

## 7. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
