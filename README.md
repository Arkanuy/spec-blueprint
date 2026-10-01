# Spec Blueprint

Kerangka dokumentasi **spec-first** untuk proyek software: tulis kontrak dulu (apa masalahnya, siapa penggunanya, proses bisnisnya, aturannya), baru minta AI menulis kode.

Tanpa dokumen ini, AI akan menebak. Dan tebakan AI selalu terlihat masuk akal — sampai scope meledak, UI tidak sesuai proses bisnis, dan tidak ada yang tahu fitur mana yang benar-benar dibutuhkan.

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

Dokumen di repo ini adalah jawaban langsung untuk enam hal itu.

---

## Isi repo

```
spec-blueprint/
├── AGENTS.md                  # kontrak kerja untuk agen AI di proyek kamu
├── SKILL.md                   # template skill (kalau kamu pakai sistem skill)
├── docs/                      # 11 dokumen inti (urutan permintaan)
│   ├── README.md              # indeks + urutan pengisian + contoh alur penuh
│   ├── 00-discovery.md        # konteks bisnis, stakeholder, as-is, akar masalah
│   ├── 01-prd.md              # PRD: tujuan, user, fitur, metrik, scope
│   ├── 02-requirements.md     # FR / NFR / business rules / data + traceability
│   ├── 03-architecture.md     # boundary sistem, komponen, integrasi, deployment
│   ├── 04-workflow.md         # alur proses as-is vs to-be, alur user, alur data
│   ├── 05-data-model.md       # entitas, relasi, status lifecycle, aturan validasi
│   ├── 06-ui-ux.md            # layar, state kosong/error/loading, navigasi
│   ├── 07-test-plan.md        # strategi uji + kasus uji turunan requirement
│   ├── 08-roadmap.md          # fase kerja, urutan pengiriman per fitur
│   ├── 09-risks.md            # risiko, asumsi yang belum terverifikasi, pertanyaan terbuka
│   └── 10-decisions.md        # log keputusan (ADR) + riwayat perubahan scope
├── prompts/                   # prompt siap pakai untuk agen AI
│   ├── 01-generate-docs.md
│   ├── 02-implement-feature.md
│   ├── 03-code-review.md
│   └── 04-sync-docs.md
├── checklists/
│   ├── gate-1-sebelum-coding.md
│   ├── gate-2-per-fitur-selesai.md
│   └── gate-3-sebelum-rilis.md
└── scripts/
    └── new_project.py         # salin template ke proyek baru, isi placeholder
```

---

## Cara pakai

### Opsi A — scaffolding otomatis (disarankan)

```bash
git clone https://github.com/Arkanuy/spec-blueprint.git
cd spec-blueprint
python scripts/new_project.py
```

Script akan menanyakan nama proyek, deskripsi, jenis aplikasi, stack, dan domain bisnis — lalu menghasilkan folder proyek berisi `docs/` + `AGENTS.md` + `prompts/` + `checklists/` yang sudah terisi.

Non-interaktif:

```bash
python scripts/new_project.py \
  --name "Sistem Kasir Toko Berkah" \
  --target ~/projects/kasir-berkah \
  --type web \
  --domain "retail / penjualan barang" \
  --stack "Next.js 15, Prisma, PostgreSQL" \
  --owner "Toko Berkah" \
  --strip-examples
```

Flag:

- `--strip-examples` — buang semua blok contoh (bagian `<!-- EXAMPLE-START -->`) agar dokumen bersih
- `--no-git` — jangan jalankan `git init`
- `--force` — izinkan menulis ke folder yang sudah punya isi
- `--dry-run` — tampilkan rencana tanpa menulis apa pun

### Opsi B — manual

Copy folder `docs/`, `AGENTS.md`, `prompts/`, `checklists/` ke repo proyekmu, lalu ganti token `{{...}}` secara manual (cari semua `{{`).

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

## Prinsip yang dipegang

1. **Business first, technology last.** Teknologi dipilih karena kebutuhan, bukan sebaliknya.
2. **Setiap fitur harus bisa dilacak** ke masalah → kebutuhan → requirement → fungsi → uji.
3. **Pisahkan fakta, asumsi, dan dugaan.** Kalau belum diverifikasi, tulis apa adanya di `09-risks.md`.
4. **Scope yang kecil tapi jelas menang** atas scope besar yang samar.
5. **Dokumen ikut berubah** setiap kali scope berubah (`10-decisions.md` wajib diisi).
6. **Tidak ada requirement yang tidak bisa diuji.**

---

## Untuk tugas kuliah (Sistem Informasi)

Struktur di repo ini sudah memetakan artefak yang biasa diminta di mata kuliah Analisis & Perancangan Sistem: konteks bisnis, stakeholder, AS-IS/TO-BE, kebutuhan fungsional & non-fungsional, aturan bisnis, model data, use case, dan justifikasi kelayakan. Bagian penilaian yang sering hilang di pekerjaan mahasiswa — *kenapa masalahnya nyata* dan *kenapa solusinya proporsional* — ditangani di `00-discovery.md` dan `08-roadmap.md`.

---

## Kontribusi

Lihat [CONTRIBUTING.md](CONTRIBUTING.md). Lisensi MIT.
