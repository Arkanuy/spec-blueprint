# Spec Blueprint

Repo isinya **dokumen kosong untuk diisi** saat kamu memulai proyek baru. Sembilan berkas `.md`
di folder `docs/`, satu kontrak untuk agen AI, dan satu script untuk menyalinnya.

Bukan aplikasi. Bukan contoh proyek. Isinya kosong dan memang untuk kamu isi.

---

## Kenapa perlu

Kalau kamu minta AI menulis kode tanpa dokumen, AI akan menebak. Tebakan AI selalu terlihat masuk
akal — sampai ruang lingkupnya meledak, tampilannya tidak sesuai proses kerja, dan tidak ada yang
tahu fitur mana yang benar-benar dibutuhkan.

| Gejala | Akar masalah |
|---|---|
| Fitur makin banyak, arah produk makin kabur | Masalah & tujuannya tidak tertulis |
| AI membuat hal yang tidak diminta, atau lupa yang penting | Tidak ada kebutuhan yang bisa dilacak |
| Kode tidak konsisten antar sesi | Tidak ada batas desain & konvensi |
| Ruang lingkup melebar tanpa disadari | Tidak ada daftar "termasuk / tidak termasuk" |
| Sulit menilai hasil AI | Tidak ada definisi selesai |
| Keputusan hilang jejaknya | Tidak ada catatan keputusan |

---

## Isinya

```
docs/
├── README.md              # urutan pengisian + format ID
├── 00-masalah.md          # masalah, akar masalah, dampak, alternatif solusi, ruang lingkup
├── 01-kebutuhan.md        # pengguna, user story, FR/NFR/BR/DR, kriteria penerimaan, keterlacakan
├── 02-desain.md           # batas sistem, komponen, alur data, hak akses, deploy, teknologi yang ditolak
├── 03-proses.md           # proses SEKARANG, proses NANTI, status, kondisi tidak normal
├── 04-data.md             # entitas, kolom, hubungan, aturan, daur hidup, data sensitif
├── 05-tampilan.md         # layar, elemen, semua kondisi (kosong/memuat/gagal/berhasil)
├── 06-uji.md              # strategi, kasus uji, kasus di luar jalur normal, bukti
├── 07-urutan-kerja.md     # tahap, urutan fitur, definisi selesai, tonggak
└── 08-risiko.md           # risiko, asumsi, pertanyaan terbuka, catatan keputusan
templates/ATURAN-AGEN.md   # kontrak untuk agen AI — disalin jadi AGENTS.md di proyekmu
scripts/new_project.py     # salin docs/ + AGENTS.md ke folder proyek baru
```

Sembilan dokumen, bukan dua belas. Yang dipakai saja — tidak ada dokumen yang cuma jadi hiasan.
Total ±900 baris untuk kesembilannya, jadi tidak ada yang berat diisi.

---

## Cara pakai

```bash
git clone https://github.com/Arkanuy/spec-blueprint.git
cd spec-blueprint
python scripts/new_project.py --target ~/projects/nama-proyekmu
```

Tidak ada script? Salin manual juga bisa — nama sumbernya `ATURAN-AGEN.md`, tapi di foldermu
beri nama `AGENTS.md` supaya agen AI otomatis membacanya:

```bash
mkdir -p ~/projects/nama-proyekmu
cp -r docs ~/projects/nama-proyekmu/
cp templates/ATURAN-AGEN.md ~/projects/nama-proyekmu/AGENTS.md
```

Lalu isi berurutan mulai dari `docs/00-masalah.md`. Urutan lengkapnya ada di `docs/README.md`.

Flag `new_project.py`:

| Flag | Arti |
|---|---|
| `--target` | Folder proyek baru (wajib) |
| `--force` | Izinkan menulis ke folder yang sudah berisi |
| `--dry-run` | Tampilkan rencana, tidak menulis apa pun |

---

## Alur pengisian

```
1. MASALAH   → 00-masalah.md     apa masalahnya, apa akar masalahnya, sistem memang jawabannya?
2. KEBUTUHAN → 01-kebutuhan.md   perilaku apa yang harus dipenuhi (ber-ID, bisa diuji)
3. DESAIN    → 02-desain.md      disusun bagaimana, batasnya di mana
4. PROSES    → 03-proses.md      sekarang vs nanti
5. DATA      → 04-data.md        apa yang disimpan dan apa yang menjaganya benar
6. TAMPILAN  → 05-tampilan.md    apa yang dilihat pengguna, termasuk kondisi gagal
7. UJI       → 06-uji.md         bagaimana dibuktikan benar
8. URUTAN    → 07-urutan-kerja.md dikerjakan berurutan bagaimana
9. RISIKO    → 08-risiko.md      apa yang bisa gagal, kenapa keputusan diambil
```

Aturan kerasnya satu: **jangan minta AI menulis fitur yang belum punya ID kebutuhan.**

---

## Prinsip

1. **Masalah dulu, teknologi terakhir.** Teknologi dipilih karena kebutuhan, bukan sebaliknya.
2. **Setiap fitur bisa dilacak** ke masalah → kebutuhan → kode → uji.
3. **Pisahkan fakta, asumsi, dan dugaan.** Yang belum diverifikasi ditulis apa adanya.
4. **Ruang lingkup kecil tapi jelas menang** atas ruang lingkup besar yang samar.
5. **Tidak ada kebutuhan yang tidak bisa diuji.**
6. **Tidak ada kolom yang hanya jadi hiasan.** Setiap bagian harus mencegah satu jenis kesalahan.

---

## Untuk tugas kuliah (Sistem Informasi)

Struktur ini memetakan artefak yang biasa diminta di mata kuliah Analisis & Perancangan Sistem:
konteks bisnis, stakeholder, AS-IS/TO-BE, kebutuhan fungsional & non-fungsional, aturan bisnis,
model data, use case, dan justifikasi kelayakan.

Bagian yang paling sering hilang di pekerjaan mahasiswa — *kenapa masalahnya nyata* dan *kenapa
solusinya proporsional* — ditangani di `00-masalah.md` (bagian akar masalah dan tabel alternatif
solusi yang menyertakan opsi tanpa sistem) dan `07-urutan-kerja.md`.

---

## Lisensi

MIT.
