# Kontribusi

Repo ini kumpulan dokumen kosong untuk diisi orang lain. Aturannya sederhana.

---

## Peta folder

| Folder | Isi | Boleh berisi contoh? |
|---|---|---|
| `docs/**` | Dokumen yang disalin ke proyek pengguna | **Tidak.** Harus kosong dan siap diisi |
| `templates/ATURAN-AGEN.md` | Kontrak agen AI untuk proyek pengguna | Tidak |
| `scripts/` | Alat, bukan dokumentasi | – |
| Akar repo (`README.md`, `CONTRIBUTING.md`) | Dokumentasi repo ini | – |

---

## Aturan yang dipegang

1. **Tidak ada contoh di dalam dokumen.** Kalau sebuah bagian sulit dipahami, perbaiki judul atau
   pertanyaan penuntunnya — jangan tambahkan contoh. Contoh membuat orang menyalin, bukan berpikir.
2. **Tidak ada kolom hiasan.** Setiap bagian harus mencegah satu jenis kesalahan nyata. Kalau kamu
   tidak bisa menyebut kesalahan apa yang dicegahnya, hapus bagiannya.
3. **Tidak ada placeholder `{{...}}`.** Tulis "Proyek:" saja, biar langsung diisi.
4. **Bahasa Indonesia**, istilah teknis boleh tetap aslinya.
5. **Hindari bahasa pemasaran.** Tidak ada "solusi inovatif", "canggih", "seamless", "di era digital".
6. **Jumlah dokumen dijaga kecil.** Sembilan sudah batas atas. Menambah dokumen berarti setiap orang
   harus mengisi satu berkas lagi sebelum mulai kerja — itu biaya nyata, bukan kelengkapan.

---

## Keunikan nama berkas

`templates/ATURAN-AGEN.md` sengaja **tidak** dinamai `AGENTS.md` di repo ini. Alasannya: berkas
bernama `AGENTS.md` di akar atau di dalam repo akan otomatis dibaca sebagai *kontrak untuk repo ini
sendiri* oleh sebagian besar agen AI. Itu membuat repo kit disalahartikan sebagai proyek aplikasi —
persis masalah yang ingin dihindari. Script `new_project.py` yang mengubah namanya jadi `AGENTS.md`
saat menyalin.

Semua nama berkas `docs/` dan `templates/` **wajib huruf kecil** dengan pemisah tanda hubung
(`00-masalah.md`, bukan `00_Masalah.md`). Alasannya sama seperti di atas: `README.md` dan `AGENTS.md`
satu-satunya nama yang boleh huruf besar, karena itu konvensi yang sudah terbaca agen dan platform.

---

## Mengubah dokumen

1. Fork, buat cabang: `git checkout -b perbaikan/nama-perubahan`
2. Lakukan perubahan.
3. Uji penyalinan:

```bash
python -m py_compile scripts/new_project.py
python scripts/new_project.py --dry-run --target "$LOCALAPPDATA/Temp/sb-uji"
python scripts/new_project.py --target "$LOCALAPPDATA/Temp/sb-uji-2" --force
ls "$LOCALAPPDATA/Temp/sb-uji-2/docs"
```

4. Pastikan `docs/README.md` dan `README.md` ikut diperbarui kalau nama atau jumlah berkas berubah.
5. Buka pull request: jelaskan **kesalahan apa yang dicegah** oleh perubahan ini.

---

## Yang tidak diterima

- Menambahkan contoh, contoh terisi, atau proyek percontohan
- Menambahkan dokumen baru tanpa menghapus yang lain (kecuali sangat kuat alasannya)
- Menambahkan kolom tanpa menjelaskan manfaatnya
- Menghapus bagian "tidak termasuk ruang lingkup", "ide tunda", atau "pertanyaan terbuka" — tiga
  bagian itu yang paling mencegah proyek melenceng
- Saran teknologi sebagai default (microservices, AI, blockchain) tanpa kaitan ke kebutuhan

---

## Melaporkan masalah

```
Dokumen : [nama berkas]
Bagian  : [judul bagian]
Masalah : [misal: pertanyaannya ambigu / kolomnya tidak pernah dipakai / jawabannya tidak jelas]
Usulan  : [kalau ada]
```

Kalau ada kontradiksi antar dokumen (`01-kebutuhan.md` bertentangan dengan `02-desain.md`),
itu temuan penting — laporkan.
