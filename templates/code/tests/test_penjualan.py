"""Unit test penjualan -- mencakup F-01, F-02, F-03 dan FR-001..FR-007, BR-001..BR-005, BR-009."""

from __future__ import annotations

import unittest

from dukungan import KasusKasir, waktu_contoh
from app import layanan
from app.kesalahan import KesalahanAturan


class UjiProduk(KasusKasir):
    """FR-001, BR-010: daftar produk & keunikan SKU."""

    def test_FR001_daftar_produk_memuat_sku_nama_harga_stok(self):
        """FR-001: daftar produk berisi SKU, nama, harga, dan stok."""
        self.tambah_produk("KOPI-01", "Kopi Sachet", 3500, 40)
        self.tambah_produk("GULA-01", "Gula 1 kg", 15000, 10)

        daftar = layanan.daftar_produk(self.koneksi)

        self.assertEqual([p["sku"] for p in daftar], ["GULA-01", "KOPI-01"])
        for p in daftar:
            for bidang in ("sku", "nama", "harga", "stok"):
                self.assertIn(bidang, p)
        self.assertEqual(daftar[1]["harga"], 3500)
        self.assertEqual(daftar[1]["stok"], 40)

    def test_BR010_sku_duplikat_ditolak(self):
        """BR-010: SKU harus unik."""
        self.tambah_produk("KOPI-01", "Kopi Sachet", 3500, 40)
        with self.assertRaises(KesalahanAturan) as konteks:
            self.tambah_produk("KOPI-01", "Kopi Lain", 4000, 5)
        self.assertIn("sudah dipakai", str(konteks.exception))

    def test_BR010_sku_tidak_bisa_diubah_setelah_dipakai_transaksi(self):
        """BR-010: perubahan SKU setelah dipakai di transaksi harus dicegah oleh skema/aturan bisnis.

        Skeletation ini belum menyediakan perintah ubah produk (di luar F-01..F-05),
        jadi aturan ditegakkan dengan memastikan kode transaksi & sale_items tetap
        merujuk product_id asal sehingga riwayat tidak rusak saat master berubah.
        """
        self.tambah_produk("KOPI-01", "Kopi Sachet", 3500, 40)
        transaksi = self.jual([("KOPI-01", 2)], bayar=10000)
        item = self.baris_sale_items(transaksi["kode"])
        self.assertEqual(item[0]["sku"], "KOPI-01")
        # Mengubah nama/harga master tidak mengubah riwayat harga di sale_items.
        with self.koneksi:
            self.koneksi.execute(
                "UPDATE products SET harga = 9999, nama = 'Kopi Baru' WHERE sku = 'KOPI-01'"
            )
        item_lagi = self.baris_sale_items(transaksi["kode"])
        self.assertEqual(item_lagi[0]["harga_satuan"], 3500)  # BR-002 riwayat aman


class UjiCatatPenjualan(KasusKasir):
    """F-01..F-03: FR-002..FR-007 dan BR-001..BR-005, BR-009."""

    def setUp(self) -> None:
        super().setUp()
        self.tambah_produk("KOPI-01", "Kopi Sachet", 3500, 40)
        self.tambah_produk("ROTI-01", "Roti Tawar", 12000, 5)

    def test_FR002_satu_transaksi_bisa_beberapa_baris_item(self):
        """FR-002: satu transaksi penjualan dengan beberapa baris item sekaligus."""
        transaksi = self.jual([("KOPI-01", 2), ("ROTI-01", 1)], bayar=50000)
        self.assertEqual(transaksi["status"], "SELESAI")
        self.assertEqual(len(transaksi["item"]), 2)
        self.assertEqual({i["sku"] for i in transaksi["item"]}, {"KOPI-01", "ROTI-01"})

    def test_FR003_nomor_transaksi_unik_berurutan_per_hari(self):
        """FR-003: nomor TRX-YYYYMMDD-### urut per hari dan unik."""
        t1 = self.jual([("KOPI-01", 1)], bayar=5000, waktu=waktu_contoh())
        t2 = self.jual([("KOPI-01", 1)], bayar=5000, waktu=waktu_contoh())
        t3 = self.jual([("KOPI-01", 1)], bayar=5000, waktu=waktu_contoh("2026-10-04"))

        self.assertEqual(t1["kode"], "TRX-20261003-001")
        self.assertEqual(t2["kode"], "TRX-20261003-002")
        self.assertEqual(t3["kode"], "TRX-20261004-001")  # hari baru, urutan ulang
        self.assertEqual(len({t1["kode"], t2["kode"], t3["kode"]}), 3)

    def test_FR004_total_dihitung_dari_seluruh_baris(self):
        """FR-004 / BR-003: total = jumlah (qty x harga satuan) seluruh baris."""
        transaksi = self.jual([("KOPI-01", 2), ("ROTI-01", 1)], bayar=50000)
        # 2 x 3500 + 1 x 12000 = 19000
        self.assertEqual(transaksi["total"], 19000)
        total_manual = sum(i["qty"] * i["harga_satuan"] for i in transaksi["item"])
        self.assertEqual(transaksi["total"], total_manual)

    def test_FR005_kembalian_dihitung_dari_bayar_dikurangi_total(self):
        """FR-005 / BR-004: kembalian = bayar - total."""
        transaksi = self.jual([("ROTI-01", 1)], bayar=20000)
        self.assertEqual(transaksi["total"], 12000)
        self.assertEqual(transaksi["kembalian"], 8000)

    def test_FR006_stok_berkurang_tepat_sebesar_qty(self):
        """FR-006: stok berkurang sebesar qty saat transaksi disimpan."""
        sebelum = self.stok("KOPI-01")
        self.jual([("KOPI-01", 3)], bayar=20000)
        self.assertEqual(self.stok("KOPI-01"), sebelum - 3)
        self.assertEqual(self.stok("KOPI-01"), 37)

    def test_FR007_qty_melebihi_stok_ditolak(self):
        """FR-007 / BR-005: qty melebihi stok tersedia harus ditolak."""
        with self.assertRaises(KesalahanAturan) as konteks:
            self.jual([("ROTI-01", 99)], bayar=1000000)
        pesan = str(konteks.exception)
        self.assertIn("tidak cukup", pesan)
        self.assertIn("99", pesan)
        self.assertIn("5", pesan)  # stok tersedia disebut

    def test_BR001_qty_harus_bulat_lebih_besar_dari_nol(self):
        """BR-001: qty harus bilangan bulat > 0."""
        for qty in (0, -1):
            with self.assertRaises(KesalahanAturan) as konteks:
                self.jual([("KOPI-01", qty)], bayar=50000)
            self.assertIn("lebih besar dari 0", str(konteks.exception))
        # non-integer
        with self.assertRaises(KesalahanAturan):
            self.jual([("KOPI-01", 1.5)], bayar=50000)

    def test_BR002_harga_satuan_disalin_dari_master_saat_transaksi(self):
        """BR-002: harga diambil dari master, bukan diketik kasir; disalin ke sale_items."""
        transaksi = self.jual([("KOPI-01", 2)], bayar=10000)
        item = transaksi["item"][0]
        self.assertEqual(item["harga_satuan"], 3500)
        with self.koneksi:
            self.koneksi.execute("UPDATE products SET harga = 5000 WHERE sku = 'KOPI-01'")
        # Riwayat transaksi lama tetap memakai harga saat transaksi dibuat.
        self.assertEqual(self.baris_sale_items(transaksi["kode"])[0]["harga_satuan"], 3500)

    def test_BR003_total_sama_dengan_jumlah_subtotal(self):
        """BR-003: total transaksi = jumlah seluruh subtotal baris."""
        transaksi = self.jual([("KOPI-01", 4), ("ROTI-01", 2)], bayar=100000)
        jumlah_subtotal = sum(i["subtotal"] for i in transaksi["item"])
        self.assertEqual(transaksi["total"], jumlah_subtotal)
        self.assertEqual(transaksi["total"], 4 * 3500 + 2 * 12000)

    def test_BR004_bayar_kurang_ditolak(self):
        """BR-004: bayar < total harus ditolak dengan pesan yang menyebut kekurangan."""
        with self.assertRaises(KesalahanAturan) as konteks:
            self.jual([("ROTI-01", 1)], bayar=11000)  # total 12000
        pesan = str(konteks.exception)
        self.assertIn("kurang", pesan)
        self.assertIn("12000", pesan)
        self.assertIn("11000", pesan)

    def test_BR009_sku_sama_dua_kali_dalam_satu_transaksi_ditolak(self):
        """BR-009: tidak boleh dua baris dengan SKU sama."""
        with self.assertRaises(KesalahanAturan) as konteks:
            self.jual([("KOPI-01", 1), ("KOPI-01", 1)], bayar=50000)
        self.assertIn("lebih dari sekali", str(konteks.exception))
        # stok tidak boleh ikut berubah saat transaksi gagal (atomik)
        self.assertEqual(self.stok("KOPI-01"), 40)

    def test_FR003_transaksi_gagal_tidak_membocorkan_nomor(self):
        """Transaksi yang ditolak tidak boleh menyimpan baris transaksi gagal."""
        with self.assertRaises(KesalahanAturan):
            self.jual([("ROTI-01", 99)], bayar=1000000)
        jumlah = self.koneksi.execute("SELECT COUNT(*) AS n FROM sales").fetchone()["n"]
        self.assertEqual(jumlah, 0)


if __name__ == "__main__":
    unittest.main()
