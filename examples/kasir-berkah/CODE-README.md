# Kasir Berkah — skeleton kode (Python stdlib)

CLI kasir/POS toko kelontong kecil. Mengimplementasikan tepat lima fitur P0
(F-01..F-05) beserta `FR-001..FR-012` dan `BR-001..BR-010` pada kontrak proyek.
Hanya memakai **stdlib Python 3.10+** — tanpa dependensi pihak ketiga, ORM,
framework web, atau Docker.

## Menjalankan

Butuh Python 3.10 atau lebih baru. Tidak ada langkah instalasi.

```bash
cd templates/code
python -m app produk tambah --sku KOPI-01 --nama "Kopi Sachet" --harga 3500 --stok 40
python -m app produk tambah --sku ROTI-01 --nama "Roti Tawar" --harga 12000 --stok 5
python -m app produk daftar
python -m app jual --produk KOPI-01:2 --produk ROTI-01:1 --bayar 50000 --kasir "Nadia"
python -m app rekap --tanggal 2026-10-03
python -m app batal --kode TRX-20261003-001 --alasan "salah input"
```

Lokasi basis data diatur lewat variabel lingkungan `KASIR_DB` (default `kasir.db`
di direktori kerja):

```bash
KASIR_DB=/tmp/toko-uji.db python -m app produk daftar
```

Kode keluar: `0` berhasil, `1` kesalahan aturan bisnis (pesan ke `stderr`),
`2` salah pemakaian perintah.

## Menguji

```bash
cd templates/code
python -m unittest discover -s tests -v
```

Setiap test memakai basis data sementara sendiri di direktori temp, jadi
`kasir.db` template tidak pernah tersentuh.

## Peta berkas

| Berkas | Isi |
|---|---|
| `app/cli.py` | Antarmuka argparse: `produk tambah`, `produk daftar`, `jual`, `rekap`, `batal` |
| `app/layanan.py` | Aturan bisnis `FR-001..FR-012` dan `BR-001..BR-010` |
| `app/db.py` | Koneksi & skema SQLite (3 entitas) |
| `app/kesalahan.py` | `KesalahanAturan` → dipetakan ke kode keluar 1 |
| `tests/` | Unit test `unittest` (penjualan, pembatalan, rekap, kontrak CLI) |

## Di luar lingkup (OUT OF SCOPE)

Pembelian dari pemasok, multi-cabang, diskon/promo, cetak struk ke printer,
login berbasis password, sinkronisasi online, laporan bulanan, ekspor Excel.
