"""Antarmuka baris perintah (argparse) untuk Kasir Berkah.

Perintah yang tersedia (lihat kontrak CLI):

    python -m app produk tambah --sku SKU --nama "Nama" --harga 3500 --stok 40
    python -m app produk daftar
    python -m app jual --produk SKU:QTY [--produk SKU:QTY ...] --bayar 50000 --kasir "Nadia"
    python -m app rekap --tanggal 2026-10-03
    python -m app batal --kode TRX-20261003-001 --alasan "salah input"

Bentuk ringkas ``produk-tambah`` / ``produk-daftar`` juga diterima (nama
subcommand tanpa spasi dan tanpa underscore) dan berperilaku sama.

Kode keluar: 0 berhasil, 1 kesalahan aturan bisnis, 2 salah pemakaian perintah.
"""

from __future__ import annotations

import argparse
import sys

from . import db, layanan
from .kesalahan import KesalahanAturan

KODE_BERHASIL = 0
KODE_ATURAN = 1
KODE_PEMAKAIAN = 2


# --------------------------------------------------------------------------- #
# Pem-parsing argumen
# --------------------------------------------------------------------------- #
def _urai_item(teks: str) -> tuple[str, int]:
    """Ubah ``SKU:QTY`` menjadi pasangan (sku, qty).

    Kesalahan format dianggap salah pemakaian perintah (kode keluar 2) karena
    ditangkap argparse; ini berbeda dari pelanggaran aturan bisnis.
    """
    if ":" not in teks:
        raise argparse.ArgumentTypeError(
            f"Nilai --produk '{teks}' salah format. Pakai SKU:QTY, misalnya --produk KOPI-01:2."
        )
    sku, _, qty_teks = teks.rpartition(":")
    sku = sku.strip()
    if not sku:
        raise argparse.ArgumentTypeError(
            f"Nilai --produk '{teks}' tidak menyebut SKU. Pakai SKU:QTY, misalnya --produk KOPI-01:2."
        )
    try:
        qty = int(qty_teks)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Qty pada --produk '{teks}' harus bilangan bulat. Contoh benar: --produk {sku}:2."
        ) from None
    return sku, qty


def _tambah_produk_ke(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--sku", required=True, help="kode produk, unik (mis. KOPI-01)")
    parser.add_argument("--nama", required=True, help="nama produk yang tampil ke kasir")
    parser.add_argument("--harga", required=True, type=int, help="harga satuan dalam rupiah penuh")
    parser.add_argument("--stok", required=True, type=int, help="jumlah stok awal")
    parser.set_defaults(fungsi="produk-tambah")


def bangun_parser() -> argparse.ArgumentParser:
    """Rakit parser argparse lengkap dengan semua subcommand."""
    parser = argparse.ArgumentParser(
        prog="app",
        description="Kasir Berkah -- catat penjualan, rekap harian, dan batalkan transaksi.",
    )
    sub = parser.add_subparsers(dest="perintah", metavar="PERINTAH")

    # Bentuk kontrak: 'produk tambah' dan 'produk daftar'.
    produk = sub.add_parser("produk", help="kelola master produk")
    aksi = produk.add_subparsers(dest="aksi", metavar="AKSI")

    produk_tambah = aksi.add_parser("tambah", help="tambah produk baru")
    _tambah_produk_ke(produk_tambah)

    produk_daftar = aksi.add_parser("daftar", help="tampilkan daftar produk")
    produk_daftar.set_defaults(fungsi="produk-daftar")

    # Bentuk ringkas tanpa spasi (nama subcommand tanpa underscore).
    ringkas_tambah = sub.add_parser("produk-tambah", help="tambah produk baru (ringkas)")
    _tambah_produk_ke(ringkas_tambah)

    ringkas_daftar = sub.add_parser("produk-daftar", help="tampilkan daftar produk (ringkas)")
    ringkas_daftar.set_defaults(fungsi="produk-daftar")

    jual = sub.add_parser("jual", help="catat satu transaksi penjualan")
    jual.add_argument(
        "--produk",
        action="append",
        type=_urai_item,
        required=True,
        metavar="SKU:QTY",
        help="baris item, boleh diulang (mis. --produk KOPI-01:2)",
    )
    jual.add_argument("--bayar", required=True, type=int, help="uang yang diterima, rupiah penuh")
    jual.add_argument("--kasir", required=True, help="nama kasir yang melayani")
    jual.set_defaults(fungsi="jual")

    rekap = sub.add_parser("rekap", help="tampilkan rekap penjualan harian")
    rekap.add_argument("--tanggal", required=True, help="tanggal rekap, format YYYY-MM-DD")
    rekap.set_defaults(fungsi="rekap")

    batal = sub.add_parser("batal", help="batalkan transaksi yang sudah selesai")
    batal.add_argument("--kode", required=True, help="nomor transaksi, mis. TRX-20261003-001")
    batal.add_argument("--alasan", required=True, help="alasan pembatalan, minimal 5 karakter")
    batal.set_defaults(fungsi="batal")

    return parser


# --------------------------------------------------------------------------- #
# Penangan tiap perintah
# --------------------------------------------------------------------------- #
def _rupiah(nilai: int) -> str:
    """Format integer rupiah dengan pemisah ribuan titik (mis. 1.250.000)."""
    return f"{nilai:,}".replace(",", ".")


def tangani_produk_tambah(koneksi, argumen) -> int:
    produk = layanan.tambah_produk(
        koneksi,
        sku=argumen.sku,
        nama=argumen.nama,
        harga=argumen.harga,
        stok=argumen.stok,
    )
    print(
        f"Produk ditambahkan: {produk['sku']} - {produk['nama']} "
        f"| harga Rp{_rupiah(produk['harga'])} | stok {produk['stok']}"
    )
    return KODE_BERHASIL


def tangani_produk_daftar(koneksi, argumen) -> int:
    produk = layanan.daftar_produk(koneksi)
    if not produk:
        print("Belum ada produk terdaftar. Tambahkan dengan: python -m app produk tambah ...")
        return KODE_BERHASIL
    print(f"DAFTAR PRODUK ({len(produk)} item)")
    print(f"{'SKU':<12} {'NAMA':<20} {'HARGA':>12} {'STOK':>6}")
    print("-" * 54)
    for p in produk:
        print(f"{p['sku']:<12} {p['nama']:<20} {_rupiah(p['harga']):>12} {p['stok']:>6}")
    return KODE_BERHASIL


def tangani_jual(koneksi, argumen) -> int:
    transaksi = layanan.buat_penjualan(
        koneksi,
        items=argumen.produk,
        bayar=argumen.bayar,
        kasir=argumen.kasir,
    )
    print(f"Transaksi tersimpan: {transaksi['kode']} ({transaksi['status']})")
    print(f"Kasir           : {transaksi['kasir']}")
    print(f"Waktu           : {transaksi['dibuat_pada']}")
    print("Baris item:")
    for item in transaksi["item"]:
        print(
            f"  - {item['sku']:<12} {item['nama']:<20} "
            f"{item['qty']} x Rp{_rupiah(item['harga_satuan'])} = Rp{_rupiah(item['subtotal'])}"
        )
    print(f"Total           : Rp{_rupiah(transaksi['total'])}")
    print(f"Bayar           : Rp{_rupiah(transaksi['bayar'])}")
    print(f"Kembalian       : Rp{_rupiah(transaksi['kembalian'])}")
    return KODE_BERHASIL


def tangani_rekap(koneksi, argumen) -> int:
    rekap = layanan.rekap_harian(koneksi, tanggal=argumen.tanggal)
    print(f"REKAP HARIAN {rekap['tanggal']}")
    print(f"Jumlah transaksi    : {rekap['jumlah_transaksi']}")
    print(f"Total penjualan     : Rp{_rupiah(rekap['total_penjualan'])}")
    print(f"Total item terjual  : {rekap['total_item_terjual']}")
    if rekap["daftar_transaksi"]:
        print("Transaksi (status SELESAI):")
        for t in rekap["daftar_transaksi"]:
            print(
                f"  - {t['kode']} | Rp{_rupiah(t['total'])} | "
                f"kembalian Rp{_rupiah(t['kembalian'])} | kasir {t['kasir']}"
            )
    else:
        print("(tidak ada transaksi berstatus SELESAI pada tanggal ini)")
    return KODE_BERHASIL


def tangani_batal(koneksi, argumen) -> int:
    transaksi = layanan.batalkan(koneksi, kode=argumen.kode, alasan=argumen.alasan)
    print(f"Transaksi {transaksi['kode']} DIBATALKAN.")
    print(f"Alasan          : {transaksi['alasan_batal']}")
    print(f"Dibatalkan pada : {transaksi['dibatalkan_pada']}")
    print("Stok produk pada transaksi ini sudah dikembalikan.")
    return KODE_BERHASIL


# --------------------------------------------------------------------------- #
# Titik masuk
# --------------------------------------------------------------------------- #
def jalankan(argv: list[str] | None = None) -> int:
    """Jalankan satu perintah CLI dan kembalikan kode keluar."""
    parser = bangun_parser()
    argumen = parser.parse_args(argv)

    fungsi = getattr(argumen, "fungsi", None)
    if fungsi is None:
        # Perintah kosong atau 'produk' tanpa aksi -> salah pemakaian.
        parser.print_usage(sys.stderr)
        print(
            "Perintah belum lengkap. Pilih salah satu: produk tambah, produk daftar, "
            "jual, rekap, atau batal.",
            file=sys.stderr,
        )
        return KODE_PEMAKAIAN

    penangan = {
        "produk-tambah": tangani_produk_tambah,
        "produk-daftar": tangani_produk_daftar,
        "jual": tangani_jual,
        "rekap": tangani_rekap,
        "batal": tangani_batal,
    }[fungsi]

    try:
        koneksi = db.buka()
        try:
            return penangan(koneksi, argumen)
        finally:
            koneksi.close()
    except KesalahanAturan as galat:
        print(f"Gagal: {galat.pesan}", file=sys.stderr)
        return KODE_ATURAN
