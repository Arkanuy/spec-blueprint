#!/usr/bin/env python3
"""Salin dokumen template ke folder proyek baru.

Contoh:
    python scripts/new_project.py --target ~/projects/kasir-berkah
    python scripts/new_project.py --target ./proyek-baru --force

Yang disalin: docs/ (sembilan dokumen kosong) + AGENTS.md (kontrak untuk agen AI).
Semuanya masih kosong dan memang untuk kamu isi sendiri.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
# Sumber ditulis ATURAN-AGEN.md supaya berkas di repo ini tidak disalahartikan sebagai
# kontrak untuk repo ini sendiri. Di folder proyek hasil, namanya dikembalikan ke AGENTS.md.
AGENTS_SRC = REPO_ROOT / "templates" / "ATURAN-AGEN.md"
AGENTS_NAME = "AGENTS.md"


class SalinError(Exception):
    """Kesalahan yang bisa dijelaskan ke pengguna tanpa pelacakan tumpukan."""


def normalize_target(raw: str) -> str:
    """Ubah path gaya MSYS (/c/Users/...) jadi gaya Windows (C:/Users/...).

    Di Git Bash, konversi path otomatis kadang dimatikan, sehingga /c/Users/x
    diteruskan apa adanya dan terbaca sebagai C:\\c\\Users\\x.
    """
    if sys.platform.startswith("win") and re.match(r"^/[a-zA-Z]/", raw):
        return f"{raw[1].upper()}:{raw[2:]}"
    return raw


def berkas_sumber() -> list[tuple[Path, Path]]:
    """Pasangan (sumber, tujuan relatif) yang akan disalin."""
    if not DOCS_DIR.is_dir():
        raise SalinError(f"Folder docs/ tidak ditemukan di {REPO_ROOT}")
    if not AGENTS_SRC.is_file():
        raise SalinError(f"{AGENTS_SRC.relative_to(REPO_ROOT)} tidak ditemukan di {REPO_ROOT}")

    pasangan: list[tuple[Path, Path]] = []
    for f in sorted(DOCS_DIR.glob("*.md")):
        pasangan.append((f, Path("docs") / f.name))
    pasangan.append((AGENTS_SRC, Path(AGENTS_NAME)))
    return pasangan


def jalankan(args: argparse.Namespace) -> int:
    tujuan = Path(normalize_target(args.target)).expanduser().resolve()

    if tujuan == REPO_ROOT:
        print("Gagal: tujuan sama dengan repo template. Pakai --target ke folder proyekmu.",
              file=sys.stderr)
        return 2

    if tujuan.exists() and any(tujuan.iterdir()) and not args.force:
        print(f"Gagal: {tujuan} sudah ada dan tidak kosong.\n"
              f"Pakai --force kalau memang mau menulis ke sana.", file=sys.stderr)
        return 2

    pasangan = berkas_sumber()

    if args.dry_run:
        print(f"Tujuan : {tujuan}")
        print(f"Berkas : {len(pasangan)}")
        for sumber, rel in pasangan:
            print(f"  {rel}   (dari {sumber.relative_to(REPO_ROOT)})")
        return 0

    try:
        for sumber, rel in pasangan:
            out = tujuan / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sumber, out)
    except OSError as exc:
        print(f"Gagal menulis berkas: {exc}", file=sys.stderr)
        return 1

    jumlah_dok = len(pasangan) - 1
    print(f"Tujuan : {tujuan}")
    print(f"Disalin: {len(pasangan)} berkas ({jumlah_dok} dokumen + {AGENTS_NAME})")
    print(f"""
Selesai. Langkah berikutnya:
  cd "{tujuan}"
  1. Isi docs/00-masalah.md   (masalah, akar masalah, pilihan solusi)
  2. Isi docs/01-kebutuhan.md (fitur, kebutuhan ber-ID, kriteria penerimaan)
  3. Isi docs/02-desain.md dan seterusnya sesuai urutan di docs/README.md
  4. Isi bagian identitas di {AGENTS_NAME} sebelum minta agen AI menulis kode
""")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="new_project.py",
        description="Salin dokumen template (docs/ + AGENTS.md) ke folder proyek baru.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--target", required=True,
                   help="Folder proyek baru. Wajib — script tidak menebak tujuan.")
    p.add_argument("--force", action="store_true",
                   help="Izinkan menulis ke folder yang sudah berisi berkas")
    p.add_argument("--dry-run", action="store_true",
                   help="Tampilkan rencana, tidak menulis apa pun")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return jalankan(args)
    except SalinError as exc:
        print(f"Gagal: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
