"""Unit test antarmuka CLI -- kontrak perintah & kode keluar (0/1/2) dan NFR-001/NFR-002.

Dijalankan in-process lewat ``cli.jalankan()`` supaya perilaku kode keluar dan
aliran stdout/stderr bisa diperiksa tanpa memanggil interpreter Python baru.
"""

from __future__ import annotations

import unittest

from dukungan import KasusKasir, waktu_contoh
from app import db, layanan


class UjiKontrakCLI(KasusKasir):
    def setUp(self) -> None:
        super().setUp()
        kode, _, _ = self.jalankan_cli(
            ["produk", "tambah", "--sku", "KOPI-01", "--nama", "Kopi Sachet",
             "--harga", "3500", "--stok", "40"]
        )
        self.assertEqual(kode, 0)

    def test_produk_tambah_dan_daftar_bentuk_kontrak(self):
        """Kontrak CLI: 'produk tambah' dan 'produk daftar' jalan dan keluar 0."""
        kode, luar, _ = self.jalankan_cli(["produk", "daftar"])
        self.assertEqual(kode, 0)
        self.assertIn("KOPI-01", luar)
        self.assertIn("Kopi Sachet", luar)

    def test_produk_tambah_dan_daftar_bentuk_ringkas(self):
        """Bentuk ringkas tanpa spasi ('produk-tambah' / 'produk-daftar') setara."""
        kode, luar, _ = self.jalankan_cli(["produk-daftar"])
        self.assertEqual(kode, 0)
        self.assertIn("KOPI-01", luar)

    def test_jual_sukses_keluar_nol(self):
        kode, luar, _ = self.jalankan_cli(
            ["jual", "--produk", "KOPI-01:2", "--bayar", "50000", "--kasir", "Nadia"]
        )
        self.assertEqual(kode, 0)
        self.assertIn("TRX-", luar)
        self.assertIn("SELESAI", luar)
        self.assertIn("Kembalian", luar)

    def test_salah_pemakaian_keluar_dua(self):
        """Kode keluar 2 untuk perintah kurang argumen atau format SKU:QTY salah."""
        for args in (
            [],  # tanpa perintah
            ["produk"],  # 'produk' tanpa aksi
            ["jual", "--produk", "KOPI-01", "--bayar", "50000", "--kasir", "Nadia"],  # tanpa ':'
            ["jual", "--produk", "KOPI-01:x", "--bayar", "50000", "--kasir", "Nadia"],  # qty bukan int
            ["jual", "--produk", "KOPI-01:1", "--bayar", "50000"],  # tanpa --kasir
            ["rekap"],  # tanpa --tanggal
        ):
            kode, _, _ = self.jalankan_cli(args)
            self.assertEqual(kode, 2, msg=f"args={args} harus keluar 2")

    def test_kesalahan_aturan_keluar_satu_dan_pesan_ke_stderr(self):
        """Kode keluar 1 untuk pelanggaran aturan bisnis; pesan masuk stderr."""
        kode, luar, galat = self.jalankan_cli(
            ["jual", "--produk", "TIDAK-ADA:1", "--bayar", "50000", "--kasir", "Nadia"]
        )
        self.assertEqual(kode, 1)
        self.assertEqual(luar, "")
        self.assertIn("Gagal:", galat)
        self.assertIn("TIDAK-ADA", galat)

    def test_NFR001_data_tetap_ada_setelah_koneksi_ditutup(self):
        """NFR-001: data tersimpan di SQLite lokal dan masih ada setelah koneksi ditutup."""
        self.jalankan_cli(
            ["jual", "--produk", "KOPI-01:3", "--bayar", "20000", "--kasir", "Nadia"]
        )
        self.koneksi.close()  # tutup koneksi test
        koneksi_baru = db.buka(self.jalur_db)  # buka ulang dari berkas yang sama
        try:
            stok = koneksi_baru.execute(
                "SELECT stok FROM products WHERE sku = 'KOPI-01'"
            ).fetchone()["stok"]
            jumlah = koneksi_baru.execute("SELECT COUNT(*) AS n FROM sales").fetchone()["n"]
            self.assertEqual(stok, 37)
            self.assertEqual(jumlah, 1)
        finally:
            koneksi_baru.close()

    def test_batal_kesalahan_aturan_keluar_satu(self):
        """Batal dengan alasan pendek lewat CLI -> keluar 1 dengan pesan jelas."""
        self.jalankan_cli(
            ["jual", "--produk", "KOPI-01:1", "--bayar", "5000", "--kasir", "Nadia"]
        )
        kode, _, galat = self.jalankan_cli(
            ["batal", "--kode", "TRX-20261003-001", "--alasan", "no"]
        )
        self.assertEqual(kode, 1)
        self.assertIn("minimal 5 karakter", galat)


class UjiPesanHasil(KasusKasir):
    """Pesan keluaran memuat informasi yang dibutuhkan kasir (NFR-003)."""

    def test_pesan_bayar_kurang_menyebut_total_dan_bayar(self):
        layanan.tambah_produk(self.koneksi, "ROTI-01", "Roti Tawar", 12000, 5)
        kode, _, galat = self.jalankan_cli(
            ["jual", "--produk", "ROTI-01:1", "--bayar", "10000", "--kasir", "Nadia"]
        )
        self.assertEqual(kode, 1)
        self.assertIn("12000", galat)
        self.assertIn("10000", galat)


if __name__ == "__main__":
    unittest.main()
