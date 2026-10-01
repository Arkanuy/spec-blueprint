# 03 — Architecture

> Dokumen ini menjawab: **sistemnya tersusun dari apa, batasnya di mana, dan bagaimana bagian-bagiannya bicara satu sama lain.** Ditulis setelah requirement jelas. Arsitektur mengikuti kebutuhan — bukan kebutuhan yang dipaksa mengikuti arsitektur yang sedang populer.

**Proyek:** {{PROJECT_NAME}}
**Stack:** {{STACK}}
**Versi:** 0.1
**Terakhir diperbarui:** {{DATE}}

---

## 1. Prinsip arsitektur

Tulis 3–6 prinsip yang mengikat semua keputusan teknis. Prinsip ini yang dipakai untuk menolak usulan yang tidak sesuai.

| # | Prinsip | Konsekuensi praktis |
|---|---|---|
| P-1 | Sesederhana yang bisa menyelesaikan masalah | Tidak menambah layanan/infra tanpa kebutuhan yang terbukti |
| P-2 | Satu sumber kebenaran untuk setiap data | Tidak ada data penting yang hidup di dua tempat tanpa sinkronisasi |
| P-3 | [prinsip proyek] | [konsekuensi] |

<!-- EXAMPLE-START -->
Contoh prinsip yang sering benar untuk proyek kecil:
- P-1: Aplikasi monolit sederhana. Tidak ada microservices sebelum ada masalah skala nyata.
- P-2: Validasi ditegakkan di sisi server, bukan hanya di UI.
- P-3: Semua perubahan data penting tercatat (siapa, kapan, apa).
- P-4: Bisa dijalankan di satu mesin dengan `docker compose up`.
<!-- EXAMPLE-END -->

---

## 2. Scope sistem

### 2.1 Yang termasuk sistem ini

- [komponen/kapabilitas]

### 2.2 Yang di luar sistem ini

| Hal | Kenapa di luar | Ditangani oleh |
|---|---|---|
| [fungsi] | [alasan] | [orang/proses/sistem lain] |

### 2.3 Konteks sistem (siapa bicara dengan sistem)

```
                 ┌──────────────────────────────┐
   [Pengguna] ──▶│                              │
                 │        {{PROJECT_NAME}}      │──▶ [Layanan eksternal]
   [Staf]    ──▶ │                              │
                 └──────────────────────────────┘
                            │
                            ▼
                       [Database]
```

Ganti kotak di atas dengan aktor & sistem nyata proyek ini.

---

## 3. Daftar komponen

| Komponen | Tanggung jawab | Teknologi | Alasan memilih | Batasan |
|---|---|---|---|---|
| [nama] | [satu tanggung jawab utama] | [stack] | [kenapa ini, kaitkan ke kebutuhan] | [keterbatasan] |

Aturan: satu komponen, satu tanggung jawab. Kalau deskripsinya perlu kata "dan" untuk tanggung jawab yang tidak berhubungan, itu tanda komponennya harus dipecah — atau memang perlu digabung dan alasannya ditulis.

---

## 4. Diagram arsitektur

```
[Ganti dengan diagram komponen sistem ini]

Contoh bentuk umum:

  ┌─────────────┐      ┌──────────────────┐      ┌──────────────┐
  │  Frontend   │◀────▶│  Backend / API   │◀────▶│   Database   │
  └─────────────┘ HTTP └──────────────────┘ SQL  └──────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Layanan eksternal│
                     └──────────────────┘
```

Setiap kotak di diagram harus muncul di tabel komponen. Setiap garis harus punya label protokolnya.

---

## 5. Alur data

Untuk setiap alur penting, tulis: **siapa** → **apa** → **disimpan di mana** → **siapa yang membaca**.

### 5.1 Alur: [nama alur]

| Langkah | Dari | Ke | Data | Format | Sifat |
|---|---|---|---|---|---|
| 1 | [pengguna] | [frontend] | [data] | [form/JSON] | [sinkron] |
| 2 | [frontend] | [API] | [data] | [JSON] | [sinkron] |
| 3 | [API] | [DB] | [data] | [SQL] | [transaksional] |

<!--- Sifat: sinkron/asinkron, realtime/batch, idempoten/tidak --->

---

## 6. Boundary & kontrak

### 6.1 Endpoint internal (kalau ada backend)

| Metode | Path | Tujuan | Masukan | Keluaran | Butuh autentikasi | Peran yang boleh | FR terkait |
|---|---|---|---|---|---|---|---|
| POST | /api/[resource] | [tujuan] | [body] | [respons] | Ya | [peran] | FR-00x |

Aturan: setiap endpoint harus terhubung ke minimal satu FR. Endpoint tanpa FR dicurigai tidak dibutuhkan.

### 6.2 Integrasi pihak ketiga

| Layanan | Untuk apa | Protokol | Kalau mati apa yang terjadi | Data yang dikirim | Risiko |
|---|---|---|---|---|---|
| [layanan] | [fungsi] | [REST/Webhook] | [dampak] | [data] | [risiko] |

---

## 7. Model otorisasi

| Peran | Bisa melihat | Bisa membuat | Bisa mengubah | Bisa menghapus | Catatan |
|---|---|---|---|---|---|
| [peran] | [scope] | [scope] | [scope] | [scope] | [khusus] |

Aturan penting: hak akses **ditegakkan di server**. Menyembunyikan tombol di UI bukan pengamanan.

---

## 8. Struktur folder proyek

```
{{PROJECT_NAME}}/
├── src/
│   ├── [folder per tanggung jawab]
│   └── ...
├── docs/            # dokumen spec ini
├── tests/
├── .env.example
├── README.md
└── ...
```

Ganti dengan struktur nyata. Setiap folder harus punya satu alasan keberadaan.

---

## 9. Konfigurasi & rahasia

| Variabel | Kegunaan | Wajib | Nilai contoh (bukan rahasia nyata) | Di mana diisi |
|---|---|---|---|---|
| [NAMA_VAR] | [fungsi] | Ya | [contoh] | [.env / panel hosting] |

Aturan:

- Rahasia **tidak pernah** ditulis di kode atau di dokumen ini.
- `.env.example` memuat nama variabel + contoh dummy, tanpa nilai asli.
- `.env` masuk `.gitignore`.

---

## 10. Deployment

| Aspek | Isi |
|---|---|
| Lingkungan | [dev / staging / produksi] |
| Cara menjalankan lokal | [perintah] |
| Cara deploy | [langkah] |
| Di mana di-host | [layanan] |
| Migrasi database | [perintah/tool] |
| Backup | [cara & frekuensi] |
| Rollback | [cara kembali ke versi sebelumnya] |
| Pemantauan | [log/health check] |

---

## 11. Kebutuhan non-fungsional teknis

| Kebutuhan | Keputusan teknis | Alasan |
|---|---|---|
| Performa | [pilihan] | [terkait NFR-00x] |
| Keamanan | [pilihan] | [terkait NFR-00x] |
| Skalabilitas | [pilihan] | [terkait NFR-00x] |

---

## 12. Keputusan yang sengaja tidak diambil

Teknologi/pendekatan yang sering diusulkan tapi **ditolak** untuk proyek ini. Ini pengaman agar AI tidak menambahkannya seenaknya.

| Ditolak | Kenapa ditolak sekarang | Kapan jadi masuk akal |
|---|---|---|
| [contoh: microservices] | [contoh: tim 1 orang, beban rendah] | [kalau ada tim terpisah & beban tinggi] |
| [contoh: message queue] | [belum ada kebutuhan asinkron] | [kalau ada proses berat/jadwal] |
| [contoh: AI/ML] | [tidak ada keputusan bisnis yang butuh prediksi] | [kalau ada data historis & masalah prediktif nyata] |

---

## 13. Utang teknis & catatan

| # | Catatan | Alasan diambil sekarang | Kapan diperbaiki |
|---|---|---|---|

---

## 14. Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dokumen dibuat | Awal proyek |
