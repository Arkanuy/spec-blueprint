"""Unit test rekap harian -- F-04: FR-008, FR-009, dan pemakaian NFR-003 pada pesan error."""

from __future__ import annotations

import unittest

from dukungan import KasusKasir, waktu_contoh
from app import layanan
from app.kesalahan import KesalahanAturan


class UjiRekap(KasusKasir):
    def setUp(self) -> None:
        super().setUp()
        self.tambah_produk("KOPI-01", "Kopi Sachet", 3500, 40)
        self.tambah_produk("ROTI-01", "Roti Tawar", 12000, 5)

    def test_FR008_rekap_menampilkan_jumlah_total_dan_item(self):
        """FR-008: rekap harian berisi jumlah transaksi, total penjualan, total item terjual."""
        self.jual([("KOPI-01", 2)], bayar=10000, waktu=waktu_contoh())
        self.jual([("ROTI-01", 1)], bayar=20000, waktu=waktu_contoh())

        rekap = layanan.rekap_harian(self.koneksi, "2026-10-03")
        self.assertEqual(rekap["tanggal"], "2026-10-03")
        self.assertEqual(rekap["jumlah_transaksi"], 2)
        self.assertEqual(rekap["total_penjualan"], 2 * 3500 + 12000)  # 19000
        self.assertEqual(rekap["total_item_terjual"], 3)

    def test_FR009_rekap_hanya_menghitung_transaksi_selesai(self):
        """FR-009: transaksi DIBATALKAN tidak masuk rekap."""
        t1 = self.jual([("KOPI-01", 2)], bayar=10000, waktu=waktu_contoh())["kode"]
        self.jual([("ROTI-01", 1)], bayar=20000, waktu=waktu_contoh())

        sebelum = layanan.rekap_harian(self.koneksi, "2026-10-03")
        self.assertEqual(sebelum["jumlah_transaksi"], 2)
        self.assertEqual(sebelum["total_penjualan"], 19000)
        self.assertEqual(sebelum["total_item_terjual"], 3)

        layanan.batalkan(self.koneksi, t1, "salah input")

        sesudah = layanan.rekap_harian(self.koneksi, "2026-10-03")
        self.assertEqual(sesudah["jumlah_transaksi"], 1)
        self.assertEqual(sesudah["total_penjualan"], 12000)  # hanya ROTI yang tersisa
        self.assertEqual(sesudah["total_item_terjual"], 1)
        # total rekap turun setelah batal
        self.assertLess(sesudah["total_penjualan"], sebelum["total_penjualan"])

    def test_FR009_rekap_hari_lain_tidak_tercampur(self):
        """Rekap per tanggal hanya menghitung transaksi pada tanggal itu."""
        self.jual([("KOPI-01", 1)], bayar=5000, waktu=waktu_contoh("2026-10-03"))
        self.jual([("ROTI-01", 1)], bayar=20000, waktu=waktu_contoh("2026-10-04"))

        rekap_03 = layanan.rekap_harian(self.koneksi, "2026-10-03")
        rekap_04 = layanan.rekap_harian(self.koneksi, "2026-10-04")
        self.assertEqual(rekap_03["total_penjualan"], 3500)
        self.assertEqual(rekap_04["total_penjualan"], 12000)

    def test_FR009_rekap_hari_kosong_bernilai_nol(self):
        """Rekap hari tanpa transaksi SELESAI mengembalikan nol, bukan error."""
        rekap = layanan.rekap_harian(self.koneksi, "2026-01-01")
        self.assertEqual(rekap["jumlah_transaksi"], 0)
        self.assertEqual(rekap["total_penjualan"], 0)
        self.assertEqual(rekap["total_item_terjual"], 0)
        self.assertEqual(rekap["daftar_transaksi"], [])

    def test_NFR003_tanggal_salah_format_pesan_jelas(self):
        """NFR-003: tanggal salah format menghasilkan pesan Indonesia yang menjelaskan tindakan."""
        with self.assertRaises(KesalahanAturan) as konteks:
            layanan.rekap_harian(self.koneksi, "03-10-2026")
        pesan = str(konteks.exception)
        self.assertIn("YYYY-MM-DD", pesan)


if __name__ == "__main__":
    unittest.main()
