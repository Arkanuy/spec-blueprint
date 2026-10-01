# Kontribusi

Terima kasih kalau kamu mau ikut memperbaiki repo ini. Aturan mainnya sederhana.

---

## Prinsip yang dipegang

1. **Dokumen harus bisa dipertanggungjawabkan.** Kalau kamu menambah kolom atau bagian, jelaskan pertanyaan apa yang dijawabnya.
2. **Jangan menambah bagian hanya agar dokumen terlihat lengkap.** Setiap bagian harus mencegah satu jenis kesalahan nyata.
3. **Bahasa Indonesia**, istilah teknis boleh tetap dalam bentuk aslinya.
4. **Hindari bahasa pemasaran.** Tidak ada "solusi inovatif", "canggih", "seamless", "di era digital".
5. **Sertakan contoh untuk hal yang abstrak.** Contoh nyata jauh lebih berguna daripada penjelasan panjang. Bungkus dengan `<!-- EXAMPLE-START -->` dan `<!-- EXAMPLE-END -->` — script scaffolding bisa membuangnya otomatis.

---

## Cara menambah atau mengubah dokumen

1. Fork repo, buat cabang: `git checkout -b perbaikan/nama-perubahan`
2. Lakukan perubahan.
3. Uji scaffolding:

```bash
python scripts/new_project.py --dry-run --name "Uji" --non-interactive
python scripts/new_project.py --name "Uji" --target ./out/uji \
  --strip-examples --no-git --non-interactive
grep -rn '{{[A-Z_]*}}' ./out/uji/docs   # harus kosong
```

4. Pastikan `README.md` dan `docs/README.md` diperbarui kalau kamu menambah berkas baru.
5. Buka pull request dengan menjelaskan: masalah apa yang diselesaikan perubahan ini.

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

## Melaporkan masalah

Buka issue dengan isi:

```
Dokumen   : [nama berkas]
Bagian    : [judul bagian]
Masalah   : [misal: kolom ini tidak pernah dipakai / ambigu / kontradiktif]
Usulan    : [kalau ada]
```

Kalau kamu menemukan ada kontradiksi antar dokumen (misal: `02-requirements.md` dan `03-architecture.md` bertentangan), itu temuan yang penting — laporkan.
