"""CLI Kasir Berkah -- skeleton kasir/POS toko kelontong kecil.

Lingkup: tepat lima fitur P0 (F-01..F-05) dan requirement yang diturunkan
(FR-001..FR-012, BR-001..BR-010) pada kontrak proyek. Tidak ada dependensi
pihak ketiga; hanya stdlib Python 3.10+.

Modul:
    cli       -- antarmuka argparse (produk tambah/daftar, jual, rekap, batal)
    db        -- koneksi & skema SQLite (NFR-001)
    layanan   -- aturan bisnis FR/BR
    kesalahan -- exception domain KesalahanAturan -> kode keluar 1
"""

__versi__ = "1.0.0"

__all__ = ["cli", "db", "layanan", "kesalahan"]