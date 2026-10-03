"""Perkakas bersama untuk unit test Kasir Berkah.

Setiap test mendapat basis data SQLite sementara sendiri (``KASIR_DB`` diarahkan
ke berkas di dalam direktori temp) supaya test tidak saling mengotori dan tidak
pernah menyentuh ``kasir.db`` template asli (NFR-001 diuji di sini).
"""

from __future__ import annotations

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

# Pastikan paket 'app' bisa diimpor walau test dijalankan dari mana saja.
AKAR = Path(__file__).resolve().parent.parent
if str(AKAR) not in sys.path:
    sys.path.insert(0, str(AKAR))

from app import cli, db, layanan  # noqa: E402


class KasusKasir(unittest.TestCase):
    """Basis test: basis data bersih per test + pembantu singkat."""

    def setUp(self) -> None:
        self.direktori = tempfile.mkdtemp(prefix="kasir-uji-")
        self.jalur_db = str(Path(self.direktori) / "kasir-uji.db")
        self._env_lama = os.environ.get("KASIR_DB")
        os.environ["KASIR_DB"] = self.jalur_db
        self.koneksi = db.buka(self.jalur_db)

    def tearDown(self) -> None:
        self.koneksi.close()
        if self._env_lama is None:
            os.environ.pop("KASIR_DB", None)
        else:
            os.environ["KASIR_DB"] = self._env_lama
        shutil.rmtree(self.direktori, ignore_errors=True)

    # -- pembantu -----------------------------------------------------------------
    def stok(self, sku: str) -> int:
        baris = self.koneksi.execute(
            "SELECT stok FROM products WHERE sku = ?", (sku,)
        ).fetchone()
        return int(baris["stok"])

    def tambah_produk(self, sku: str, nama: str, harga: int, stok: int) -> dict:
        return layanan.tambah_produk(self.koneksi, sku, nama, harga, stok)

    def jual(self, items, bayar, kasir="Nadia", waktu=None) -> dict:
        return layanan.buat_penjualan(self.koneksi, items, bayar, kasir, waktu=waktu)

    def jalankan_cli(self, args) -> tuple[int, str, str]:
        """Jalankan CLI in-process; kembalikan (kode_keluar, stdout, stderr)."""
        keluaran, galat = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(keluaran), contextlib.redirect_stderr(galat):
            try:
                kode = cli.jalankan(args)
            except SystemExit as keluar:  # argparse memakai SystemExit untuk kode 2
                kode = keluar.code if isinstance(keluar.code, int) else 2
        return kode, keluaran.getvalue(), galat.getvalue()

    def baris_sale_items(self, kode: str) -> list[dict]:
        return layanan.ambil_penjualan(self.koneksi, kode)["item"]


def waktu_contoh(tanggal="2026-10-03", jam=10, menit=30) -> datetime:
    return datetime.strptime(f"{tanggal} {jam:02d}:{menit:02d}:00", "%Y-%m-%d %H:%M:%S")
