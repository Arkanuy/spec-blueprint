"""Unit test pembatalan -- F-05: FR-010, FR-011, FR-012 dan BR-006..BR-008."""

from __future__ import annotations

import unittest

from dukungan import KasusKasir, waktu_contoh
from app import layanan
from app.kesalahan import KesalahanAturan


class UjiPembatalan(KasusKasir):
    def setUp(self) -> None:
        super().setUp()
        self.tambah_produk("KOPI-01", "Kopi Sachet", 3500, 40)
        self.tambah_produk("ROTI-01", "Roti Tawar", 12000, 5)
        self.kode = self.jual(
            [("KOPI-01", 2), ("ROTI-01", 1)], bayar=50000, waktu=waktu_contoh()
        )["kode"]

    def test_FR010_batal_selesai_dengan_alasan_minimal_5_karakter(self):
        """FR-010: transaksi SELESAI dibatalkan bila alasan >= 5 karakter."""
        transaksi = layanan.batalkan(self.koneksi, self.kode, "salah input", waktu=waktu_contoh())
        self.assertEqual(transaksi["status"], "DIBATALKAN")
        self.assertEqual(transaksi["alasan_batal"], "salah input")
        self.assertIsNotNone(transaksi["dibatalkan_pada"])

    def test_FR011_stok_dikembalikan_saat_transaksi_dibatalkan(self):
        """FR-011 / BR-008: stok kembali sebesar qty yang dibatalkan."""
        # setelah jual: KOPI 40-2=38, ROTI 5-1=4
        self.assertEqual(self.stok("KOPI-01"), 38)
        self.assertEqual(self.stok("ROTI-01"), 4)
        layanan.batalkan(self.koneksi, self.kode, "salah input")
        self.assertEqual(self.stok("KOPI-01"), 40)
        self.assertEqual(self.stok("ROTI-01"), 5)

    def test_FR012_pembatalan_kedua_ditolak(self):
        """FR-012 / BR-006: transaksi SELESAI hanya boleh dibatalkan satu kali."""
        layanan.batalkan(self.koneksi, self.kode, "salah input")
        with self.assertRaises(KesalahanAturan) as konteks:
            layanan.batalkan(self.koneksi, self.kode, "batal lagi")
        pesan = str(konteks.exception)
        self.assertIn("sudah dibatalkan", pesan)
        # stok tidak boleh bertambah dua kali.
        self.assertEqual(self.stok("KOPI-01"), 40)

    def test_BR007_alasan_kurang_dari_5_karakter_ditolak(self):
        """BR-007: alasan minimal 5 karakter."""
        with self.assertRaises(KesalahanAturan) as konteks:
            layanan.batalkan(self.koneksi, self.kode, "err")
        pesan = str(konteks.exception)
        self.assertIn("minimal 5 karakter", pesan)
        # transaksi belum berubah
        self.assertEqual(layanan.ambil_penjualan(self.koneksi, self.kode)["status"], "SELESAI")

    def test_BR007_alasan_spasi_saja_dianggap_kosong(self):
        """BR-007: alasan yang hanya berisi spasi tetap terlalu pendek setelah dipangkas."""
        with self.assertRaises(KesalahanAturan):
            layanan.batalkan(self.koneksi, self.kode, "   ")

    def test_state_machine_transisi_terlarang_ditolak(self):
        """State machine: DIBATALKAN -> apa pun terlarang; DRAFT tidak bisa dibatalkan."""
        layanan.batalkan(self.koneksi, self.kode, "salah input")
        # DIBATALKAN -> apa pun: ditolak (sudah dibatalkan)
        with self.assertRaises(KesalahanAturan):
            layanan.batalkan(self.koneksi, self.kode, "coba lagi")
        # DRAFT -> DIBATALKAN: ditolak, dibuat manual untuk menguji transisi terlarang.
        with self.koneksi:
            kursor = self.koneksi.execute(
                "INSERT INTO sales (kode, dibuat_pada, status, total, bayar, kembalian, kasir) "
                "VALUES ('TRX-20261003-900', '2026-10-03 11:00:00', 'DRAFT', 0, 0, 0, 'Nadia')"
            )
            id_draft = kursor.lastrowid
        with self.assertRaises(KesalahanAturan) as konteks:
            layanan.batalkan(self.koneksi, "TRX-20261003-900", "salah input")
        self.assertIn("DRAFT", str(konteks.exception))

    def test_kode_transaksi_tidak_ada_ditolak(self):
        """Kode transaksi yang tidak ada memberi pesan yang menyebut kode itu."""
        with self.assertRaises(KesalahanAturan) as konteks:
            layanan.batalkan(self.koneksi, "TRX-20261003-999", "salah input")
        self.assertIn("TRX-20261003-999", str(konteks.exception))


if __name__ == "__main__":
    unittest.main()
