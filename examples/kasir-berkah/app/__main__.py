"""Titik masuk paket: ``python -m app``.

Meneruskan argumen ke :func:`app.cli.jalankan` dan memakai kode keluarnya
sebagai kode keluar proses (0 berhasil, 1 kesalahan aturan, 2 salah pemakaian).
"""

import sys

from .cli import jalankan

if __name__ == "__main__":
    sys.exit(jalankan(sys.argv[1:]))
