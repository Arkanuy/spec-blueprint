"""Koneksi SQLite dan skema basis data (NFR-001).

Data disimpan di berkas SQLite lokal supaya tetap ada setelah proses ditutup
tanpa perlu server. Path diambil dari variabel lingkungan ``KASIR_DB``; default
``kasir.db`` di direktori kerja saat ini. Uang disimpan sebagai integer rupiah
penuh, bukan float.
"""

from __future__ import annotations

import os
import sqlite3

NAMA_BERKAS_DEFAULT = "kasir.db"

# Skema tiga entitas pada kontrak (products, sales, sale_items).
# Aturan integritas ditegakkan di lapisan data, bukan hanya di CLI:
#   - products.stok >= 0            -> BR-005 tidak boleh stok minus
#   - sale_items.qty > 0            -> BR-001
#   - UNIQUE(sale_id, product_id)   -> BR-009 satu SKU satu baris per transaksi
#   - products.sku UNIQUE           -> BR-010 (bagian keunikan)
#   - sales.status dibatasi daftar status state machine
SKEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    sku         TEXT    NOT NULL UNIQUE,
    nama        TEXT    NOT NULL,
    harga       INTEGER NOT NULL CHECK (harga >= 0),
    stok        INTEGER NOT NULL CHECK (stok >= 0),
    dibuat_pada TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    kode            TEXT    NOT NULL UNIQUE,
    dibuat_pada     TEXT    NOT NULL,
    status          TEXT    NOT NULL CHECK (status IN ('DRAFT', 'SELESAI', 'DIBATALKAN')),
    total           INTEGER NOT NULL DEFAULT 0 CHECK (total >= 0),
    bayar           INTEGER NOT NULL DEFAULT 0 CHECK (bayar >= 0),
    kembalian       INTEGER NOT NULL DEFAULT 0 CHECK (kembalian >= 0),
    kasir           TEXT    NOT NULL,
    alasan_batal    TEXT,
    dibatalkan_pada TEXT
);

CREATE TABLE IF NOT EXISTS sale_items (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id      INTEGER NOT NULL REFERENCES sales(id),
    product_id   INTEGER NOT NULL REFERENCES products(id),
    qty          INTEGER NOT NULL CHECK (qty > 0),
    harga_satuan INTEGER NOT NULL CHECK (harga_satuan >= 0),
    subtotal     INTEGER NOT NULL CHECK (subtotal >= 0),
    UNIQUE (sale_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_sales_dibuat_pada ON sales (dibuat_pada);
CREATE INDEX IF NOT EXISTS idx_sale_items_sale ON sale_items (sale_id);
"""


def jalur_basis_data() -> str:
    """Path berkas basis data aktif (dari env ``KASIR_DB`` atau default)."""
    jalur = os.environ.get("KASIR_DB")
    if jalur is None or not jalur.strip():
        return NAMA_BERKAS_DEFAULT
    return jalur


def hubungkan(jalur: str | None = None) -> sqlite3.Connection:
    """Buka koneksi SQLite tanpa menyiapkan skema."""
    koneksi = sqlite3.connect(jalur or jalur_basis_data())
    koneksi.row_factory = sqlite3.Row
    koneksi.execute("PRAGMA foreign_keys = ON")
    return koneksi


def siapkan_skema(koneksi: sqlite3.Connection) -> None:
    """Buat tabel bila belum ada. Aman dipanggil berulang kali."""
    koneksi.executescript(SKEMA)
    koneksi.commit()


def buka(jalur: str | None = None) -> sqlite3.Connection:
    """Buka koneksi dan pastikan skema siap dipakai."""
    koneksi = hubungkan(jalur)
    siapkan_skema(koneksi)
    return koneksi