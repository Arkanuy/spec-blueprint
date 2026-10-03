# SKILL.md — Template Skill Proyek

> File ini adalah **template**. Kalau kamu memakai sistem skill berbasis file (Claude Skills, Hermes, atau agen yang membaca folder `skills/`), salin file ini ke folder skill-mu, ganti nama, dan isi bagiannya. Satu skill = satu kemampuan yang bisa dipakai ulang.

**Nama skill:** [nama-skill]
**Kategori:** [development / data / operations / dokumentasi]
**Pemilik:** {{OWNER}}
**Versi:** 0.1

---

## Kapan skill ini dipakai

Tulis pemicunya secara spesifik. Skill yang pemicunya kabur tidak akan pernah dipakai dengan benar.

**Gunakan skill ini kalau:**

- [kondisi nyata 1]
- [kondisi nyata 2]

**Jangan gunakan skill ini kalau:**

- [kondisi yang mirip tapi butuh pendekatan berbeda]

---

## Hasil yang diharapkan

Apa yang ada di tangan setelah skill ini dijalankan. Harus bisa diamati, bukan dirasakan.

| Keluaran | Bentuk | Kriteria berhasil |
|---|---|---|
| [hasil] | [file/laporan/tindakan] | [cara memeriksa] |

---

## Prasyarat

| Prasyarat | Cara memeriksa | Kalau belum terpenuhi |
|---|---|---|
| [akses/perkakas/data] | [perintah pemeriksaan] | [langkah mengatasi] |

---

## Langkah kerja

Tulis langkah yang benar-benar dijalankan, bukan gambaran umum. Sertakan perintah nyata.

### Langkah 1 — [nama langkah]

**Tujuan:** [kenapa langkah ini ada]

```bash
[perintah nyata]
```

**Keluaran yang diharapkan:**

```
[contoh keluaran]
```

**Kalau gagal:** [gejala] → [tindakan]

### Langkah 2 — [nama langkah]

**Tujuan:** [kenapa]

```bash
[perintah]
```

**Keluaran yang diharapkan:** [...]

**Kalau gagal:** [...]

### Langkah 3 — [verifikasi]

Buktikan hasilnya benar. Jangan klaim tanpa bukti.

```bash
[perintah verifikasi]
```

| Yang diperiksa | Kriteria lulus |
|---|---|
| [misal: jumlah data] | [misal: sama dengan sumber] |
| [misal: log error] | [tidak ada error baru] |

---

## Aturan yang harus dipegang

1. [aturan penting yang menjaga kualitas hasil]
2. [aturan kedua]
3. Jangan melanjutkan kalau verifikasi gagal — perbaiki dulu atau laporkan penghambatnya.

---

## Jebakan yang sudah diketahui

| Jebakan | Gejala | Cara menghindari |
|---|---|---|
| [masalah yang sering muncul] | [tanda-tandanya] | [langkah pencegahan] |

---

## Contoh nyata

### Contoh 1 — [situasi]

**Masukan:** [kondisi awal]
**Tindakan:** [langkah yang dijalankan]
**Hasil:** [keluaran nyata]

---

## Batasan

Apa yang **tidak** bisa dilakukan skill ini, supaya tidak dipakai di luar konteksnya.

- [batasan 1]

---

## Pemeliharaan

| Kapan ditinjau | Pemicu pembaruan |
|---|---|
| [misal: setiap kali perkakas utama naik versi] | [kalau langkah gagal berulang] |

Kalau langkah di skill ini ternyata salah atau kurang lengkap saat dipakai, **perbarui skill-nya** — jangan sekadar mengingatnya.

---

## Riwayat perubahan

| Versi | Tanggal | Perubahan | Alasan |
|---|---|---|---|
| 0.1 | {{DATE}} | Dibuat | Awal proyek |
