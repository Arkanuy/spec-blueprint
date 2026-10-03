# Kontribusi

Terima kasih kalau kamu mau ikut memperbaiki repo ini. Aturan mainnya sederhana.

> File ini berlaku untuk siapa pun (manusia atau agen AI) yang **mengubah kit ini**.
> Ini **bukan** kontrak untuk proyek yang dibangun dari kit ini — kontrak itu ada di
> `templates/AGENTS.md`, dan itulah yang disalin ke proyek pengguna.

---

## Peta folder — jangan tertukar

| Folder | Isi | Boleh berisi `{{TOKEN}}` / blok `EXAMPLE`? |
|---|---|---|
| `templates/**` | Bahan mentah yang disalin ke proyek baru | **Ya**, di sini tempatnya |
| `templates/code/**` | Skeleton kode yang ikut disalin kalau `--with-code` | Tidak — kode harus jalan apa adanya |
| `examples/**` | Contoh proyek terisi penuh (dokumen + kode + bukti uji) | **Tidak** — harus terisi penuh |
| akar repo | Dokumentasi kit ini sendiri | Tidak |

Berkas proyek hasil generate tinggal di folder pengguna, bukan di sini.

---

## Prinsip yang dipegang

1. **Dokumen harus bisa dipertanggungjawabkan.** Kalau kamu menambah kolom atau bagian, jelaskan pertanyaan apa yang dijawabnya.
2. **Jangan menambah bagian hanya agar dokumen terlihat lengkap.** Setiap bagian harus mencegah satu jenis kesalahan nyata.
3. **Bahasa Indonesia**, istilah teknis boleh tetap dalam bentuk aslinya.
4. **Hindari bahasa pemasaran.** Tidak ada "solusi inovatif", "canggih", "seamless", "di era digital".
5. **Sertakan contoh untuk hal yang abstrak.** Contoh nyata jauh lebih berguna daripada penjelasan
   panjang. Bungkus dengan `<!-- EXAMPLE-START -->` dan `<!-- EXAMPLE-END -->` — script scaffolding
   bisa membuangnya otomatis.
6. **Contoh terisi dan template tidak boleh berbeda cerita.** `examples/kasir-berkah/` adalah contoh
   yang dijaga: kalau kamu mengubah `templates/docs/`, periksa apakah contohnya masih sesuai. Contoh
   yang menyesatkan lebih buruk daripada tidak ada contoh.

---

## Aturan penting: template vs dokumentasi repo

- `templates/**` = bahan mentah yang **disalin ke proyek baru**. Hanya di sini `{{TOKEN}}` dan blok
  `EXAMPLE` boleh muncul.
- `examples/**` = contoh **terisi penuh**. Tidak boleh ada `{{TOKEN}}`, `[isi]`, atau blok `EXAMPLE`.
- Akar repo (`README.md`, `CONTRIBUTING.md`) = dokumentasi repo ini sendiri. Jangan taruh template di sini.
- Dokumen hasil generate tinggal di folder proyek pengguna, **bukan** di repo ini.

---

## Cara menambah atau mengubah dokumen

1. Fork repo, buat cabang: `git checkout -b perbaikan/nama-perubahan`
2. Lakukan perubahan.
3. Uji scaffolding (jalankan dari akar repo):

```bash
python -m py_compile scripts/new_project.py
python scripts/new_project.py --dry-run --name "Uji" --with-code --non-interactive
python scripts/new_project.py --name "Uji" --target ./out/uji \
  --strip-examples --with-code --no-git --non-interactive --force
grep -rn '{{[A-Z_]*}}' ./out/uji/docs   # harus kosong
grep -rn 'EXAMPLE-START' ./out/uji/docs # harus kosong
cd out/uji && python -m unittest discover -s tests   # skeleton kode harus lulus
```

4. Kalau kamu mengubah `templates/docs/`, periksa `examples/kasir-berkah/docs/` masih konsisten —
   dan sebaliknya. Dua hal ini harus bercerita sama.
5. Pastikan `README.md` dan `templates/docs/README.md` diperbarui kalau kamu menambah berkas baru.
6. Buka pull request dengan menjelaskan: masalah apa yang diselesaikan perubahan ini.

---

## Kalau kamu menemukan bagian yang tidak jelas

Jangan hanya memperbaiki kalimatnya. Tanyakan dulu: bagian ini tidak jelas karena **tulisannya buruk**, atau karena **pertanyaan yang harus dijawabnya memang belum jelas**? Kalau yang kedua, perbaiki strukturnya, bukan kata-katanya.

---

## Yang tidak diterima

- Bagian yang hanya menambah kolom tanpa menjelaskan manfaatnya
- Perubahan yang membuat dokumen lebih panjang tanpa membuat keputusan lebih mudah
- Rekomendasi teknologi tanpa kaitan ke kebutuhan (contoh: menambahkan saran "pakai microservices/AI/blockchain" sebagai default)
- Menghapus bagian "out of scope", "ide tunda", atau "pertanyaan terbuka" — tiga bagian ini yang paling mencegah proyek melenceng

---

## Verifikasi wajib sebelum menyatakan selesai

```bash
cd <repo ini>
python -m py_compile scripts/new_project.py

python scripts/new_project.py --name "Uji" --target "$LOCALAPPDATA/Temp/sb-uji" \
  --type cli --domain "uji" --stack "python" --owner "CI" \
  --strip-examples --with-code --no-git --non-interactive --force

grep -rn '{{[A-Z_]*}}' "$LOCALAPPDATA/Temp/sb-uji/docs"   # harus kosong
grep -rn 'EXAMPLE-START' "$LOCALAPPDATA/Temp/sb-uji/docs" # harus kosong

cd templates/code              && python -m unittest discover -s tests -v
cd ../../examples/kasir-berkah && python -m unittest discover -s tests -v
```

Catatan penting: `[isi]` di dokumen hasil **bukan** kesalahan — itu penanda bagian yang memang tugas
pengguna mengisi. Yang kesalahan adalah `{{TOKEN}}` atau blok contoh yang tersisa.

---

## Jebakan yang sudah diketahui

| Jebakan | Cara menghindari |
|---|---|
| `str.format()` pada template berisi `{` literal (diagram ASCII, JSON) → error | Pakai per-key `str.replace("{{KEY}}", nilai)`, jangan `.format()` |
| `input()` melempar `EOFError` saat stdin dipipa walau `isatty()` bilang interaktif | Bungkus setiap prompt dengan try/except; sediakan `--non-interactive` |
| Di Git Bash/MSYS, path argumen ke program native tidak dikonversi (`/c/Users/x` jadi `C:\c\Users\x`) | Normalisasi lewat `normalize_target_path()` sebelum dipakai |
| `__pycache__/` ikut tersalin ke proyek pengguna | Lewati `__pycache__` saat menyalin; jaga `.gitignore` |
| Generator dijalankan tanpa `--target` dari dalam repo kit → menebak folder di luar repo | Skrip menolak: minta `--target` ditentukan eksplisit |

Kalau menemukan jebakan baru, tulis di tabel ini — jangan biarkan orang berikutnya menemukan hal sama.

---

## Melaporkan masalah

Buka issue dengan isi:

```
Dokumen   : [nama berkas]
Bagian    : [judul bagian]
Masalah   : [misal: kolom ini tidak pernah dipakai / ambigu / kontradiktif]
Usulan    : [kalau ada]
```

Kalau kamu menemukan ada kontradiksi antar dokumen (misal: `02-requirements.md` dan `03-architecture.md` bertentangan), itu temuan yang penting — laporkan.
