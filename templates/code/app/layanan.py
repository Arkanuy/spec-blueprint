"""Lapisan layanan: seluruh aturan bisnis P0 (FR-001..FR-012, BR-001..BR-010).

Aturan ditegakkan di lapisan ini (bukan hanya di CLI) supaya perilaku yang sama
juga berlaku bila modul dipanggil dari kode lain atau dari unit test. Setiap
pelanggaran melempar :class:`~app.kesalahan.KesalahanAturan` dengan pesan Bahasa
Indonesia yang menyebut apa yang salah + apa yang harus dilakukan (NFR-003).

Peta fitur:
    F-01 catat penjualan ....... buat_penjualan, tambah_produk, daftar_produk
    F-02 total & kembalian ..... buat_penjualan (BR-003, BR-004)
    F-03 stok otomatis ......... buat_penjualan (BR-005, FR-006, FR-007)
    F-04 rekap harian .......... rekap_harian (FR-008, FR-009)
    F-05 batal + alasan ........ batalkan (FR-010..FR-012)
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

from .kesalahan import KesalahanAturan

STATUS_DRAFT = "DRAFT"
STATUS_SELESAI = "SELESAI"
STATUS_DIBATALKAN = "DIBATALKAN"

PANJANG_ALASAN_MINIMAL = 5

# Format tanggal yang dipakai kode transaksi dan pencarian rekap.
FORMAT_TANGGAL = "%Y-%m-%d"


# --------------------------------------------------------------------------- #
# Produk (F-01; FR-001, BR-010)
# --------------------------------------------------------------------------- #
def tambah_produk(
    koneksi: sqlite3.Connection,
    sku: str,
    nama: str,
    harga: int,
    stok: int,
    waktu: datetime | None = None,
) -> dict:
    """Tambah satu produk ke master (FR-001; BR-010 SKU unik).

    ``sku`` dan ``nama`` tidak boleh kosong; ``harga`` dan ``stok`` adalah
    integer rupiah/unit (bukan float).
    """
    sku = (sku or "").strip()
    nama = (nama or "").strip()

    if not sku:
        raise KesalahanAturan(
            "SKU produk tidak boleh kosong. Isi dengan kode produk, misalnya --sku KOPI-01."
        )
    if not nama:
        raise KesalahanAturan(
            "Nama produk tidak boleh kosong. Isi nama produk yang mudah dikenali kasir."
        )
    if harga < 0:
        raise KesalahanAturan(
            f"Harga produk tidak boleh negatif (diberikan {harga}). Isi harga dalam rupiah penuh, minimal 0."
        )
    if stok < 0:
        raise KesalahanAturan(
            f"Stok awal tidak boleh negatif (diberikan {stok}). Perbaiki jumlah stok produk."
        )

    stempel = (waktu or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    try:
        with koneksi:
            kursor = koneksi.execute(
                "INSERT INTO products (sku, nama, harga, stok, dibuat_pada) "
                "VALUES (?, ?, ?, ?, ?)",
                (sku, nama, harga, stok, stempel),
            )
    except sqlite3.IntegrityError as galat:
        # BR-010: SKU unik. Pesan menyebut SKU yang bentrok + tindakannya.
        if "UNIQUE" in str(galat).upper():
            raise KesalahanAturan(
                f"SKU '{sku}' sudah dipakai produk lain. Pakai SKU yang berbeda atau ubah produk yang sudah ada."
            ) from galat
        raise

    return ambil_produk(koneksi, kursor.lastrowid)


def ambil_produk(koneksi: sqlite3.Connection, product_id: int) -> dict:
    """Ambil satu produk berdasarkan id internal."""
    baris = koneksi.execute(
        "SELECT id, sku, nama, harga, stok, dibuat_pada FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()
    if baris is None:
        raise KesalahanAturan(
            f"Produk dengan id {product_id} tidak ditemukan. Periksa kembali daftar produk."
        )
    return dict(baris)


def daftar_produk(koneksi: sqlite3.Connection) -> list[dict]:
    """Daftar produk berisi SKU, nama, harga, stok (FR-001).

    Diurutkan per SKU supaya keluaran stabil dan mudah dibaca kasir.
    """
    baris = koneksi.execute(
        "SELECT id, sku, nama, harga, stok, dibuat_pada "
        "FROM products ORDER BY sku ASC"
    ).fetchall()
    return [dict(r) for r in baris]


def _produk_menurut_sku(koneksi: sqlite3.Connection, sku: str) -> dict:
    baris = koneksi.execute(
        "SELECT id, sku, nama, harga, stok FROM products WHERE sku = ?",
        (sku,),
    ).fetchone()
    if baris is None:
        raise KesalahanAturan(
            f"Produk dengan SKU '{sku}' tidak terdaftar. Tambahkan dulu dengan "
            f"'produk tambah', atau perbaiki SKU pada perintah jual."
        )
    return dict(baris)


# --------------------------------------------------------------------------- #
# Penjualan (F-01, F-02, F-03; FR-002..FR-007, BR-001..BR-005, BR-009)
# --------------------------------------------------------------------------- #
def _buat_kode_transaksi(koneksi: sqlite3.Connection, tanggal: str) -> str:
    """Nomor transaksi unik & berurutan per hari: ``TRX-YYYYMMDD-###`` (FR-003, NFR-004).

    Urutan dihitung dari jumlah transaksi yang sudah ada pada tanggal itu,
    termasuk yang dibatalkan, agar tidak pernah ada nomor kembar.
    """
    awalan = f"TRX-{tanggal.replace('-', '')}-"
    baris = koneksi.execute(
        "SELECT COUNT(*) AS jumlah FROM sales WHERE kode LIKE ?",
        (awalan + "%",),
    ).fetchone()
    urutan = int(baris["jumlah"]) + 1
    return f"{awalan}{urutan:03d}"


def _validasi_item(koneksi: sqlite3.Connection, items: list[tuple[str, int]]) -> list[dict]:
    """Validasi baris item sebelum transaksi disimpan.

    Menegakkan BR-001 (qty bulat > 0), BR-005 (tidak melebihi stok) dan
    BR-009 (tidak boleh dua baris dengan SKU sama). Harga satuan diambil dari
    master produk (BR-002) -- kasir tidak mengetik ulang harga.
    """
    if not items:
        raise KesalahanAturan(
            "Transaksi harus punya minimal satu produk. Tambahkan dengan --produk SKU:QTY."
        )

    hasil: list[dict] = []
    dilihat: set[str] = set()

    for sku, qty in items:
        sku = (sku or "").strip()
        if sku in dilihat:
            raise KesalahanAturan(
                f"SKU '{sku}' muncul lebih dari sekali dalam satu transaksi. "
                f"Gabungkan menjadi satu baris dengan qty total."
            )
        dilihat.add(sku)

        if not isinstance(qty, int) or isinstance(qty, bool):
            raise KesalahanAturan(
                f"Qty untuk SKU '{sku}' harus bilangan bulat. Tulis misalnya --produk {sku}:2."
            )
        if qty <= 0:
            raise KesalahanAturan(
                f"Qty untuk SKU '{sku}' harus lebih besar dari 0 (diberikan {qty}). "
                f"Perbaiki jumlah yang dijual."
            )

        produk = _produk_menurut_sku(koneksi, sku)
        if qty > produk["stok"]:
            raise KesalahanAturan(
                f"Stok SKU '{sku}' tidak cukup: diminta {qty}, tersedia {produk['stok']}. "
                f"Kurangi qty atau tambah stok produk lebih dulu."
            )

        hasil.append(
            {
                "product_id": produk["id"],
                "sku": produk["sku"],
                "nama": produk["nama"],
                # BR-002: harga disalin dari master, bukan dari input kasir.
                "harga_satuan": produk["harga"],
                "qty": qty,
                "subtotal": produk["harga"] * qty,  # BR-003 per baris
            }
        )
    return hasil


def buat_penjualan(
    koneksi: sqlite3.Connection,
    items: list[tuple[str, int]],
    bayar: int,
    kasir: str,
    waktu: datetime | None = None,
) -> dict:
    """Catat satu transaksi penjualan berisi beberapa baris item (F-01, F-02, F-03).

    Alur status mengikuti state machine kontrak: transaksi dibuat ``DRAFT``,
    item ditambahkan, lalu menjadi ``SELESAI`` saat stok tersedia dan bayar
    memenuhi total. Pengurangan stok terjadi di transisi itu (FR-006).
    """
    kasir = (kasir or "").strip()
    if not kasir:
        raise KesalahanAturan(
            "Nama kasir tidak boleh kosong. Isi dengan nama kasir yang melayani, misalnya --kasir Nadia."
        )

    detail = _validasi_item(koneksi, items)

    # BR-003: total = jumlah (qty x harga satuan) seluruh baris.
    total = sum(d["subtotal"] for d in detail)

    if not isinstance(bayar, int) or isinstance(bayar, bool):
        raise KesalahanAturan(
            "Uang bayar harus bilangan bulat rupiah. Tulis misalnya --bayar 50000."
        )
    if bayar < total:
        # BR-004: bayar harus >= total.
        raise KesalahanAturan(
            f"Uang bayar kurang: total belanja {total} rupiah, dibayar {bayar} rupiah. "
            f"Terima minimal {total} rupiah atau perbaiki jumlah bayar."
        )

    sekarang = waktu or datetime.now()
    tanggal = sekarang.strftime(FORMAT_TANGGAL)
    stempel = sekarang.strftime("%Y-%m-%d %H:%M:%S")
    # BR-004: kembalian = bayar - total.
    kembalian = bayar - total

    try:
        with koneksi:  # satu transaksi SQLite: semua berhasil atau tidak sama sekali
            kode = _buat_kode_transaksi(koneksi, tanggal)

            # Transisi DRAFT: transaksi dicatat dulu, belum menyentuh stok.
            kursor = koneksi.execute(
                "INSERT INTO sales (kode, dibuat_pada, status, total, bayar, kembalian, kasir) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (kode, stempel, STATUS_DRAFT, 0, 0, 0, kasir),
            )
            sale_id = kursor.lastrowid

            for d in detail:
                koneksi.execute(
                    "INSERT INTO sale_items (sale_id, product_id, qty, harga_satuan, subtotal) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (sale_id, d["product_id"], d["qty"], d["harga_satuan"], d["subtotal"]),
                )
                # FR-006: stok berkurang sebesar qty tepat saat transaksi disimpan.
                koneksi.execute(
                    "UPDATE products SET stok = stok - ? WHERE id = ?",
                    (d["qty"], d["product_id"]),
                )

            # Transisi DRAFT -> SELESAI.
            koneksi.execute(
                "UPDATE sales SET status = ?, total = ?, bayar = ?, kembalian = ? WHERE id = ?",
                (STATUS_SELESAI, total, bayar, kembalian, sale_id),
            )
    except sqlite3.IntegrityError as galat:
        raise KesalahanAturan(
            "Transaksi gagal disimpan karena produk muncul lebih dari sekali. "
            "Gabungkan baris dengan SKU sama lalu ulangi."
        ) from galat

    return ambil_penjualan(koneksi, kode)


def ambil_penjualan(koneksi: sqlite3.Connection, kode: str) -> dict:
    """Ambil satu transaksi lengkap dengan baris itemnya berdasarkan kode."""
    baris = koneksi.execute(
        "SELECT id, kode, dibuat_pada, status, total, bayar, kembalian, kasir, "
        "alasan_batal, dibatalkan_pada FROM sales WHERE kode = ?",
        (kode,),
    ).fetchone()
    if baris is None:
        raise KesalahanAturan(
            f"Transaksi dengan kode '{kode}' tidak ditemukan. Periksa nomor nota, "
            f"formatnya TRX-YYYYMMDD-###."
        )
    transaksi = dict(baris)
    item = koneksi.execute(
        "SELECT si.id, si.product_id, p.sku, p.nama, si.qty, si.harga_satuan, si.subtotal "
        "FROM sale_items si JOIN products p ON p.id = si.product_id "
        "WHERE si.sale_id = ? ORDER BY si.id",
        (transaksi["id"],),
    ).fetchall()
    transaksi["item"] = [dict(r) for r in item]
    return transaksi


# --------------------------------------------------------------------------- #
# Pembatalan (F-05; FR-010..FR-012, BR-006..BR-008)
# --------------------------------------------------------------------------- #
def batalkan(
    koneksi: sqlite3.Connection,
    kode: str,
    alasan: str,
    waktu: datetime | None = None,
) -> dict:
    """Batalkan transaksi SELESAI bila alasannya minimal 5 karakter (FR-010).

    State machine: hanya ``SELESAI -> DIBATALKAN`` yang diizinkan. Pembatalan
    kedua (FR-012 / BR-006) dan pembatalan transaksi non-SELESAI ditolak.
    """
    alasan = (alasan or "").strip()
    if len(alasan) < PANJANG_ALASAN_MINIMAL:
        # BR-007: alasan minimal 5 karakter.
        raise KesalahanAturan(
            f"Alasan pembatalan minimal {PANJANG_ALASAN_MINIMAL} karakter "
            f"(diberikan {len(alasan)}). Jelaskan alasan dengan kalimat singkat, "
            f"misalnya --alasan \"salah input\"."
        )

    transaksi = ambil_penjualan(koneksi, kode)

    if transaksi["status"] == STATUS_DIBATALKAN:
        # FR-012 / BR-006: transaksi SELESAI hanya boleh dibatalkan satu kali.
        raise KesalahanAturan(
            f"Transaksi {kode} sudah dibatalkan sebelumnya pada {transaksi['dibatalkan_pada']} "
            f"(alasan: {transaksi['alasan_batal']}). Tidak perlu dibatalkan lagi."
        )
    if transaksi["status"] != STATUS_SELESAI:
        raise KesalahanAturan(
            f"Transaksi {kode} berstatus {transaksi['status']} dan tidak bisa dibatalkan. "
            f"Hanya transaksi berstatus SELESAI yang boleh dibatalkan."
        )

    stempel = (waktu or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    with koneksi:
        # FR-011 / BR-008: kembalikan stok sebesar qty pada baris transaksi.
        for item in transaksi["item"]:
            koneksi.execute(
                "UPDATE products SET stok = stok + ? WHERE id = ?",
                (item["qty"], item["product_id"]),
            )
        koneksi.execute(
            "UPDATE sales SET status = ?, alasan_batal = ?, dibatalkan_pada = ? WHERE id = ?",
            (STATUS_DIBATALKAN, alasan, stempel, transaksi["id"]),
        )

    return ambil_penjualan(koneksi, kode)


# --------------------------------------------------------------------------- #
# Rekap harian (F-04; FR-008, FR-009)
# --------------------------------------------------------------------------- #
def rekap_harian(koneksi: sqlite3.Connection, tanggal: str) -> dict:
    """Rekap penjualan satu hari (FR-008).

    Hanya transaksi berstatus ``SELESAI`` yang dihitung (FR-009): transaksi
    ``DIBATALKAN`` tidak menambah jumlah transaksi, total penjualan, maupun
    total item terjual.

    ``tanggal`` berformat ``YYYY-MM-DD`` (lihat :data:`FORMAT_TANGGAL`).
    """
    try:
        datetime.strptime(tanggal, FORMAT_TANGGAL)
    except ValueError as galat:
        raise KesalahanAturan(
            f"Format tanggal '{tanggal}' tidak dikenali. Pakai format YYYY-MM-DD, misalnya 2026-10-03."
        ) from galat

    ringkas = koneksi.execute(
        "SELECT COUNT(*) AS jumlah_transaksi, "
        "COALESCE(SUM(total), 0) AS total_penjualan "
        "FROM sales WHERE status = ? AND substr(dibuat_pada, 1, 10) = ?",
        (STATUS_SELESAI, tanggal),
    ).fetchone()

    item = koneksi.execute(
        "SELECT COALESCE(SUM(si.qty), 0) AS total_item "
        "FROM sale_items si JOIN sales s ON s.id = si.sale_id "
        "WHERE s.status = ? AND substr(s.dibuat_pada, 1, 10) = ?",
        (STATUS_SELESAI, tanggal),
    ).fetchone()

    daftar = koneksi.execute(
        "SELECT kode, total, bayar, kembalian, kasir, dibuat_pada FROM sales "
        "WHERE status = ? AND substr(dibuat_pada, 1, 10) = ? ORDER BY kode ASC",
        (STATUS_SELESAI, tanggal),
    ).fetchall()

    return {
        "tanggal": tanggal,
        "jumlah_transaksi": int(ringkas["jumlah_transaksi"]),
        "total_penjualan": int(ringkas["total_penjualan"]),
        "total_item_terjual": int(item["total_item"]),
        "daftar_transaksi": [dict(r) for r in daftar],
    }
