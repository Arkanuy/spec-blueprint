# Dokumen Proyek

Sembilan dokumen yang diisi berurutan saat memulai proyek baru. Semuanya masih kosong —
isinya dari kamu, bukan dari repo ini.

Kalau dokumen dan kode bertentangan, dokumen yang menang — atau dokumennya diperbarui dulu,
baru kode.

---

## Urutan pengisian

Jangan dilompati. Setiap dokumen menjawab satu pertanyaan, dan dokumen berikutnya bergantung
pada jawaban sebelumnya.

| # | Dokumen | Menjawab | Selesai kalau |
|---|---|---|---|
| 0 | [00-masalah.md](00-masalah.md) | Masalah apa yang diselesaikan, dan apakah sistem memang jawabannya? | Ada satu masalah utama + akar masalah + pilihan solusi beralasan |
| 1 | [01-kebutuhan.md](01-kebutuhan.md) | Perilaku apa yang harus dipenuhi | Setiap fitur P0 punya kebutuhan ber-ID + kriteria penerimaan |
| 2 | [02-desain.md](02-desain.md) | Sistemnya disusun bagaimana | Ada batas sistem, komponen, dan hak akses |
| 3 | [03-proses.md](03-proses.md) | Pekerjaan berjalan sekarang vs nanti | Ada proses SEKARANG, proses NANTI, dan pemetaan masalahnya |
| 4 | [04-data.md](04-data.md) | Data apa yang disimpan | Ada entitas, kolom, aturan, dan daur hidup |
| 5 | [05-tampilan.md](05-tampilan.md) | Apa yang dilihat pengguna | Setiap layar punya kondisi kosong, memuat, dan gagal |
| 6 | [06-uji.md](06-uji.md) | Bagaimana dibuktikan benar | Setiap kebutuhan P0 punya minimal satu kasus uji |
| 7 | [07-urutan-kerja.md](07-urutan-kerja.md) | Dikerjakan berurutan bagaimana | Ada tahap, urutan fitur, dan definisi selesai |
| 8 | [08-risiko.md](08-risiko.md) | Apa yang bisa gagal, dan kenapa keputusan diambil | Ada risiko, asumsi, pertanyaan terbuka, dan catatan keputusan |

---

## Format ID

Semua ID ditulis dengan pola **prefix + tiga angka**: `PREFIX-001`, `PREFIX-002`, dan seterusnya.

| Prefix | Arti | Dipakai di |
|---|---|---|
| `US` | User story | `01-kebutuhan.md` |
| `FR` | Kebutuhan fungsional | `01-kebutuhan.md` |
| `NFR` | Kebutuhan non-fungsional | `01-kebutuhan.md` |
| `BR` | Aturan bisnis | `01-kebutuhan.md` |
| `DR` | Kebutuhan data | `01-kebutuhan.md` |
| `TC` | Kasus uji | `06-uji.md` |

---

## Aturan pengisian

1. **Satu dokumen, satu audiens.** `00` dan `01` dibaca pemilik produk; `02` dan `04` oleh developer;
   `06` oleh penguji.
2. **Tandai asal klaim.** Tulis `(Fakta)`, `(Asumsi)`, atau `(Perlu dikonfirmasi)` di belakang klaim
   yang tidak jelas asalnya.
3. **Setiap fitur bisa dilacak** ke masalah di `00-masalah.md`.
4. **Angka yang belum ada datanya jangan dikarang.** Tulis `[butuh data]`, lalu catat di
   `08-risiko.md`.

---

## Konteks untuk agen AI

```
docs/01-kebutuhan.md  +  docs/02-desain.md  +  docs/04-data.md  +  docs/05-tampilan.md  +  AGENTS.md
```

Aturan kerasnya satu: **AI tidak boleh menulis fitur yang belum punya ID kebutuhan.** Ide tambahan
masuk `00-masalah.md` bagian "Ide tunda" dulu, bukan langsung ke kode.
