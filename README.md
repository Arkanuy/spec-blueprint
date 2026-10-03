# Spec Blueprint

**Tulis kontraknya dulu, baru minta AI menulis kode.**

Repo ini adalah *generator proyek baru*: kamu isi identitas proyek, keluar folder berisi 11 dokumen
spec-first + kontrak agen + prompt + checklist — dan opsional skeleton kode yang bisa langsung
dijalankan dan diuji.

Tanpa spec, AI akan menebak. Dan tebakan AI selalu terlihat masuk akal — sampai scope meledak,
UI tidak sesuai proses bisnis, dan tidak ada yang tahu fitur mana yang benar-benar dibutuhkan.

---

## Masalah yang diselesaikan

| Gejala saat vibecoding tanpa dokumen | Akar masalah |
|---|---|
| Fitur makin banyak, tapi produk makin tidak jelas arahnya | Tidak ada definisi masalah & tujuan bisnis tertulis |
| AI bikin hal yang tidak diminta, atau lupa hal penting | Tidak ada requirement yang bisa dilacak |
| Kode tidak konsisten antar sesi | Tidak ada batas arsitektur & konvensi |
| Scope melebar tanpa disadari | Tidak ada daftar in/out of scope |
| Sulit review hasil AI | Tidak ada kriteria selesai (definition of done) |
| Perubahan keputusan hilang jejaknya | Tidak ada catatan keputusan (ADR) |

---

## Cara pakai

### Opsi A — scaffolding otomatis (disarankan)

```bash
git clone https://github.com/Arkanuy/spec-blueprint.git
cd spec-blueprint
python scripts/new_project.py
```

Script menanyakan nama proyek, jenis, domain bisnis, stack, dan pemilik produk — lalu menghasilkan
folder proyek baru.

Non-interaktif (dengan skeleton kode yang bisa dijalankan):

```bash
python scripts/new_project.py \
  --name "Sistem Kasir Toko Berkah" \
  --target ~/projects/kasir-berkah \
  --type cli \
  --domain "retail / toko kelontong" \
  --stack "Python 3.10+ (stdlib), SQLite" \
  --owner "Toko Berkah" \
  --strip-examples --with-code
```

Flag lengkap:

| Flag | Arti |
|---|---|
| `--name` `--target` `--type` `--domain` `--stack` `--owner` | Identitas proyek (yang kosong ditanyakan, atau diisi default) |
| `--strip-examples` | Buang semua blok `<!-- EXAMPLE-START -->` dari dokumen hasil |
| `--with-code` | Sertakan skeleton kode dari `templates/code/` (bisa dijalankan & diuji) |
| `--no-git` | Jangan jalankan `git init` |
| `--in-place` | Tulis ke folder saat ini, bukan ke subfolder baru |
| `--force` | Izinkan menulis ke folder yang sudah berisi |
| `--dry-run` | Tampilkan rencana, tidak menulis apa pun |
| `--non-interactive` | Jangan bertanya; nilai kosong diisi default |
| `--list-examples` | Tampilkan contoh proyek terisi, lalu keluar |

Jenis proyek yang dikenali: `web`, `mobile`, `desktop`, `api`, `cli`, `library`.

### Opsi B — manual

Salin `templates/docs/`, `templates/AGENTS.md`, `templates/prompts/`, `templates/checklists/` ke repo
proyekmu, lalu ganti token `{{...}}` (cari semua `{{`).

---

## Lihat contoh yang sudah terisi dulu

Kelemahan terbesar template adalah orang tidak tahu "kalau sudah benar, isinya seperti apa".
Contohnya ada di repo ini, terisi penuh dari dokumen sampai kode:

```bash
python scripts/new_project.py --list-examples
```

`examples/kasir-berkah/` berisi:

- 11 dokumen yang sudah diisi (nol placeholder, nol `[isi]`)
- kode kasir Python stdlib-only yang benar-benar jalan (`python -m app --help`)
- unit test, plus bukti keluaran perintah di `examples/kasir-berkah/bukti/`

Baca contohnya **sebelum** mengisi dokumenmu sendiri — terutama `00-discovery.md` dan
`10-decisions.md`, dua dokumen yang paling sering dilewati.

---

## Alur kerja spec-first

```
1. DISCOVER    → isi 00-discovery.md         (masalah, stakeholder, proses sekarang)
2. DEFINE      → isi 01-prd.md               (tujuan, user, fitur, scope, metrik)
3. SPECIFY     → isi 02-requirements.md      (FR/NFR/BR, bisa diuji, ber-ID)
4. DESIGN      → isi 03/04/05/06             (arsitektur, workflow, data, UI)
5. GATE        → checklists/gate-1-sebelum-coding.md
6. BUILD       → prompts/02-implement-feature.md  (satu fitur, satu sesi)
7. VERIFY      → checklists/gate-2-per-fitur-selesai.md
8. RELEASE     → checklists/gate-3-sebelum-rilis.md
```

Aturan kerasnya hanya satu: **jangan minta AI menulis fitur yang requirement-nya belum ada ID-nya.**

---

## Isi repo

```
spec-blueprint/
├── templates/                  # yang disalin ke proyek baru
│   ├── docs/                   #   11 dokumen inti (00-discovery … 10-decisions)
│   ├── AGENTS.md               #   kontrak kerja untuk agen AI di proyekmu
│   ├── prompts/                #   4 prompt siap pakai (generate/implement/review/sync)
│   ├── checklists/             #   3 gate (sebelum coding / per fitur / sebelum rilis)
│   ├── SKILL.md                #   template skill (kalau kamu pakai sistem skill)
│   └── code/                   #   skeleton kode contoh (--with-code)
├── examples/kasir-berkah/      # contoh terisi penuh: 11 dokumen + kode + bukti uji
├── scripts/new_project.py      # generator proyek baru
└── .github/workflows/verify.yml
```

Catatan: **dokumen proyek hasil generate ada di folder proyekmu, bukan di repo ini.** Repo ini
adalah kit-nya; `templates/` adalah bahan mentahnya.

---

## Urutan 11 dokumen (jangan dilompati)

| # | Dokumen | Menjawab |
|---|---|---|
| 0 | `00-discovery.md` | Apa masalah nyatanya, dan apakah sistem layak dibuat? |
| 1 | `01-prd.md` | Apa yang dibangun, untuk siapa, sampai mana batasnya |
| 2 | `02-requirements.md` | Syarat detail yang bisa diuji (US/FR/NFR/BR/DR + AC) |
| 3 | `03-architecture.md` | Sistem tersusun dari apa, batasnya di mana |
| 4 | `04-workflow.md` | Proses berjalan sekarang vs sesudahnya |
| 5 | `05-data-model.md` | Data apa yang disimpan dan apa yang menjaganya benar |
| 6 | `06-ui-ux.md` | Apa yang dilihat pengguna, termasuk semua kondisi gagal |
| 7 | `07-test-plan.md` | Bagaimana dibuktikan benar |
| 8 | `08-roadmap.md` | Dikerjakan berurutan bagaimana |
| 9 | `09-risks.md` | Apa yang bisa gagal, apa yang masih diasumsikan |
| 10 | `10-decisions.md` | Kenapa keputusan diambil (ADR) + catatan perubahan scope |

---

## Prinsip yang dipegang

1. **Business first, technology last.** Teknologi dipilih karena kebutuhan, bukan sebaliknya.
2. **Setiap fitur harus bisa dilacak** ke masalah → kebutuhan → requirement → fungsi → uji.
3. **Pisahkan fakta, asumsi, dan dugaan.** Kalau belum diverifikasi, tulis apa adanya di `09-risks.md`.
4. **Scope yang kecil tapi jelas menang** atas scope besar yang samar.
5. **Dokumen ikut berubah** setiap kali scope berubah (`10-decisions.md` wajib diisi).
6. **Tidak ada requirement yang tidak bisa diuji.**
7. **Contoh lebih meyakinkan daripada janji.** Karena itu repo ini menyertakan satu proyek contoh
   yang dokumennya terisi sampai ke kode dan bukti ujinya.

---

## Verifikasi

Repo ini diverifikasi otomatis di setiap push (`.github/workflows/verify.yml`):

1. Struktur berkas wajib lengkap
2. `python -m py_compile` untuk generator
3. Dry-run generator
4. Generate nyata + periksa **nol sisa `{{...}}`**, **nol sisa blok contoh**, nilai proyek benar-benar tersubstitusi
5. Folder target yang tidak kosong harus ditolak (exit code ≠ 0)
6. Jalankan unit test skeleton kode contoh

---

## Untuk tugas kuliah (Sistem Informasi)

Struktur di repo ini memetakan artefak yang biasa diminta di mata kuliah Analisis & Perancangan
Sistem: konteks bisnis, stakeholder, AS-IS/TO-BE, kebutuhan fungsional & non-fungsional, aturan
bisnis, model data, use case, dan justifikasi kelayakan. Bagian penilaian yang sering hilang di
pekerjaan mahasiswa — *kenapa masalahnya nyata* dan *kenapa solusinya proporsional* — ditangani di
`00-discovery.md` (termasuk tabel alternatif solusi) dan `08-roadmap.md`.

---

## Kontribusi

Lihat [CONTRIBUTING.md](CONTRIBUTING.md). Lisensi MIT.