# Contoh: Kasir Berkah

Contoh proyek **terisi penuh** untuk kit Spec Blueprint. Bukan contoh sebagian: dokumennya selesai,
kodenya jalan, dan bukti ujinya ada.

Tujuannya satu: menjawab pertanyaan "kalau sudah benar, isinya seperti apa?" — yang paling sering
membuat orang bingung saat pertama kali membuka template.

---

## Isi folder

```
kasir-berkah/
├── docs/                 11 dokumen spec, terisi penuh (nol placeholder)
├── app/                  kode kasir, Python 3.10+ stdlib saja (tanpa dependensi)
├── tests/                35 unit test, semuanya lulus
└── bukti/                keluaran mentah perintah: unit test, sesi CLI, kasus gagal
```

---

## Coba jalankan

```bash
cd examples/kasir-berkah
python -m unittest discover -s tests -v      # 35 test, semua lulus

export KASIR_DB="$PWD/contoh.db"             # basis data terpisah untuk coba-coba
python -m app produk tambah --sku KOPI --nama "Kopi Sachet" --harga 3500 --stok 40
python -m app produk daftar
python -m app jual --produk KOPI:3 --bayar 20000 --kasir "Nadia"
python -m app rekap --tanggal 2026-10-03
python -m app batal --kode TRX-20261003-001 --alasan "salah input"
python -m app rekap --tanggal 2026-10-03     # total turun setelah dibatalkan
```

---

## Isi singkat proyek contoh

- **Masalah (asalnya di `docs/00-discovery.md`):** nota kertas, rekap manual 1–2 jam tiap malam,
  stok buku tidak cocok dengan rak, salah hitung kembalian.
- **Lima fitur P0:** catat penjualan (F-01), hitung total & kembalian (F-02), stok berkurang otomatis
  (F-03), rekap harian (F-04), batal transaksi beralasan (F-05).
- **12 FR, 5 NFR, 10 BR, 3 entitas** (`products`, `sales`, `sale_items`), status transaksi
  `DRAFT → SELESAI → DIBATALKAN`.
- **Alternatif solusi yang ditolak** justru ditulis lengkap di `docs/00-discovery.md` — termasuk opsi
  "tanpa sistem" (SOP + spreadsheet) dan alasan kenapa akhirnya memilih aplikasi.

---

## Yang paling berguna dibaca dulu

Kalau waktumu terbatas, baca dua berkas ini:

1. `docs/00-discovery.md` — cara membuktikan masalahnya nyata dan kenapa solusinya proporsional.
2. `docs/10-decisions.md` — kenapa CLI bukan web, kenapa SQLite, kenapa harga disalin ke baris
   transaksi, kenapa pembatalan hanya boleh sekali.

Dua dokumen itu yang paling sering diisi asal di pekerjaan nyata, dan dua itu yang paling menentukan
kualitas dokumen sisanya.

---

## Cara memakai contoh ini untuk proyekmu

1. Jalankan generator dari akar repo kit:
   `python scripts/new_project.py --name "Proyekmu" --target ~/projects/proyekmu --strip-examples --with-code`
2. Buka `docs/00-discovery.md` hasilnya **berdampingan** dengan contoh ini.
3. Ikuti struktur dan tingkat kedetailannya — bukan isinya. Isi dokumenmu harus berasal dari masalah
   organisasimu sendiri, bukan disalin dari Toko Berkah.

Contohnya bukan jawaban; contohnya hanya patokan kerapian.
