#!/usr/bin/env python3
"""Buat kerangka dokumen spec-first untuk proyek baru dari template Spec Blueprint.

Contoh:
    python scripts/new_project.py
    python scripts/new_project.py --name "Sistem Kasir" --target ~/projects/kasir \
        --type web --domain "retail" --stack "Next.js, Prisma, PostgreSQL" \
        --owner "Toko Berkah" --strip-examples
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Folder / file yang disalin ke proyek baru.
COPY_ITEMS = ["docs", "prompts", "checklists", "AGENTS.md", "SKILL.md"]

# Placeholder yang dikenali. Kunci tanpa kurung kurawal.
PLACEHOLDER_KEYS = ["PROJECT_NAME", "PROJECT_TYPE", "DOMAIN", "STACK", "OWNER", "DATE"]

PROJECT_TYPES = ["web", "mobile", "desktop", "api", "cli", "library"]

EXAMPLE_BLOCK = re.compile(
    r"[ \t]*<!--\s*EXAMPLE-START\s*-->.*?<!--\s*EXAMPLE-END\s*-->[ \t]*\n?",
    re.DOTALL,
)

PROJECT_README = """# {name}

{description}

**Jenis:** {type}
**Domain:** {domain}
**Stack:** {stack}

---

## Dokumen spec

Semua dokumen perencanaan ada di [`docs/`](docs/README.md). Baca berurutan:

1. [Discovery & konteks bisnis](docs/00-discovery.md)
2. [PRD](docs/01-prd.md)
3. [Requirements](docs/02-requirements.md)
4. [Architecture](docs/03-architecture.md)
5. [Workflow](docs/04-workflow.md)
6. [Data model](docs/05-data-model.md)
7. [UI/UX](docs/06-ui-ux.md)
8. [Test plan](docs/07-test-plan.md)
9. [Roadmap](docs/08-roadmap.md)
10. [Risks](docs/09-risks.md)
11. [Decisions](docs/10-decisions.md)

## Cara kerja

Dokumen dulu, kode kemudian. Alur lengkap ada di [docs/README.md](docs/README.md).

Prompt siap pakai untuk agen AI: [prompts/](prompts/).
Pemeriksaan sebelum coding / per fitur / sebelum rilis: [checklists/](checklists/).

Aturan untuk agen AI ada di [AGENTS.md](AGENTS.md) — wajib dibaca sebelum agen menulis kode.

## Menjalankan

```bash
# isi dulu bagian ini setelah kode mulai dibuat
```

## Status

Spec: {spec_status}
"""


class ScaffoldError(Exception):
    """Kesalahan yang bisa dijelaskan ke pengguna tanpa pelacakan tumpukan."""


def detect_placeholders(text: str) -> list[str]:
    """Kembalikan daftar kunci placeholder yang muncul di teks."""
    found = re.findall(r"\{\{([A-Z_]+)\}\}", text)
    return sorted(set(found))


def interpolate(text: str, values: dict[str, str]) -> str:
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def strip_examples(text: str) -> str:
    """Buang blok contoh agar dokumen bersih untuk proyek nyata."""
    return EXAMPLE_BLOCK.sub("", text)


def _ask(question: str, default: str) -> str:
    """Tanya sekali; kalau stdin tidak bisa dibaca, pakai nilai default."""
    try:
        raw = input(question).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default
    return raw or default


def prompt_if_missing(args: argparse.Namespace) -> argparse.Namespace:
    """Tanya nilai yang belum diberikan lewat argumen (hanya kalau mode interaktif)."""
    defaults = {
        "name": "Proyek Baru",
        "type": "web",
        "domain": "belum ditentukan",
        "stack": "belum ditentukan",
        "owner": "belum ditentukan",
    }

    interactive = sys.stdin.isatty() and not args.non_interactive

    if not interactive:
        for key, val in defaults.items():
            if not getattr(args, key):
                setattr(args, key, val)
        return args

    print("=== Spec Blueprint — proyek baru ===")
    print("Tekan Enter untuk memakai nilai dalam tanda [ ].\n")

    if not args.name:
        args.name = _ask("Nama proyek [Proyek Baru]: ", defaults["name"])
    if not args.type:
        args.type = _ask(f"Jenis proyek {PROJECT_TYPES} [web]: ", defaults["type"]).lower()
    if not args.domain:
        args.domain = _ask("Domain bisnis (contoh: retail / penjualan barang) "
                           "[belum ditentukan]: ", defaults["domain"])
    if not args.stack:
        args.stack = _ask("Stack teknologi [belum ditentukan]: ", defaults["stack"])
    if not args.owner:
        args.owner = _ask("Pemilik produk / organisasi [belum ditentukan]: ", defaults["owner"])

    return args


def normalize_target_path(raw: str) -> str:
    """Ubah path gaya MSYS (/c/Users/...) menjadi gaya Windows (C:/Users/...).

    Di lingkungan Git Bash, konversi path otomatis kadang dimatikan sehingga argumen
    seperti /c/Users/x diteruskan apa adanya dan dibaca sebagai C:\\c\\Users\\x.
    Fungsi ini mencegah folder yang salah terbentuk.
    """
    if sys.platform.startswith("win") and re.match(r"^/[a-zA-Z]/", raw):
        drive = raw[1].upper()
        return f"{drive}:{raw[2:]}"
    return raw


def resolve_target(args: argparse.Namespace) -> Path:
    if args.target:
        return Path(normalize_target_path(args.target)).expanduser().resolve()
    slug = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-") or "proyek-baru"
    cwd = Path.cwd()
    if cwd.resolve() == REPO_ROOT and not args.in_place:
        # Jangan menimpa repo template sendiri.
        return (cwd.parent / slug).resolve()
    return (cwd / slug).resolve() if not args.in_place else cwd.resolve()


def plan_files(target: Path, strip: bool) -> list[tuple[str, str]]:
    """Susun rencana tindakan: (jenis, keterangan)."""
    plan: list[tuple[str, str]] = []

    for item in COPY_ITEMS:
        src = REPO_ROOT / item
        if not src.exists():
            raise ScaffoldError(f"Template tidak lengkap: {item} tidak ditemukan di {REPO_ROOT}")
        dest = target / item
        if src.is_dir():
            for p in sorted(src.rglob("*")):
                if p.is_dir():
                    continue
                rel = p.relative_to(REPO_ROOT)
                plan.append(("salin", str(dest / p.relative_to(src)) + f"  (dari {rel})"))
        else:
            plan.append(("salin", str(dest) + f"  (dari {item})"))

    plan.append(("tulis", str(target / "README.md")))
    if not strip:
        pass
    return plan


def copy_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in sorted(src.rglob("*")):
        rel = item.relative_to(src)
        out = dst / rel
        if item.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, out)


def process_files(target: Path, values: dict[str, str], strip: bool,
                  dry_run: bool) -> dict[str, int]:
    """Salin, ganti placeholder, dan (opsional) buang blok contoh."""
    stats = {"disalin": 0, "placeholder_diganti": 0, "blok_contoh_dibuang": 0}

    for item in COPY_ITEMS:
        src = REPO_ROOT / item
        if src.is_dir():
            for f in sorted(src.rglob("*")):
                if f.is_dir():
                    continue
                rel = f.relative_to(REPO_ROOT)
                _write_one(f, target / rel, values, strip, dry_run, stats)
        else:
            _write_one(src, target / item, values, strip, dry_run, stats)

    return stats


def _write_one(src: Path, dest: Path, values: dict[str, str], strip: bool,
               dry_run: bool, stats: dict[str, int]) -> None:
    if dry_run:
        stats["disalin"] += 1
        return

    text = src.read_text(encoding="utf-8")

    before = set(detect_placeholders(text))
    text = interpolate(text, values)
    stats["placeholder_diganti"] += len(before)

    if strip:
        n = len(EXAMPLE_BLOCK.findall(text))
        if n:
            text = strip_examples(text)
            stats["blok_contoh_dibuang"] += n

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8", newline="\n")
    stats["disalin"] += 1


def write_readme(target: Path, args: argparse.Namespace, values: dict[str, str],
                 dry_run: bool) -> None:
    spec_status = "semua dokumen masih kosong — mulai dari docs/00-discovery.md"
    content = PROJECT_README.format(
        name=args.name,
        description=f"Dokumen perencanaan (PRD, requirements, arsitektur, workflow) untuk {args.name}.",
        type=args.type,
        domain=args.domain,
        stack=args.stack,
        spec_status=spec_status,
    )
    if dry_run:
        return
    target.joinpath("README.md").write_text(content, encoding="utf-8", newline="\n")


def git_init(target: Path) -> str:
    if (target / ".git").exists():
        return "git: repositori sudah ada, dilewati"
    try:
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=target, check=True,
                       capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return f"git: gagal menginisialisasi ({exc})"
    return "git: repositori dibuat (branch main)"


def check_unreplaced(target: Path) -> list[str]:
    """Cari placeholder yang belum tergantikan di hasil."""
    leftovers: list[str] = []
    for f in sorted(target.rglob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        keys = detect_placeholders(text)
        if keys:
            leftovers.append(f"{f.relative_to(target)}: {', '.join(keys)}")
    return leftovers


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="new_project.py",
        description="Buat kerangka dokumen spec-first untuk proyek baru.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--name", help="Nama proyek")
    p.add_argument("--target", help="Folder tujuan (default: <cwd>/<slug nama>)")
    p.add_argument("--type", choices=PROJECT_TYPES, help="Jenis proyek")
    p.add_argument("--domain", help="Domain bisnis, contoh: 'retail / penjualan barang'")
    p.add_argument("--stack", help="Stack teknologi, contoh: 'Next.js, Prisma, PostgreSQL'")
    p.add_argument("--owner", help="Pemilik produk / organisasi")
    p.add_argument("--strip-examples", action="store_true",
                   help="Buang semua blok contoh (<!-- EXAMPLE-START --> ... END)")
    p.add_argument("--no-git", action="store_true", help="Jangan jalankan git init")
    p.add_argument("--in-place", action="store_true",
                   help="Tulis ke folder saat ini, bukan ke subfolder baru")
    p.add_argument("--force", action="store_true",
                   help="Izinkan menulis ke folder yang sudah berisi file")
    p.add_argument("--dry-run", action="store_true",
                   help="Tampilkan rencana tanpa menulis apa pun")
    p.add_argument("--non-interactive", action="store_true",
                   help="Jangan bertanya; nilai yang kosong diisi default")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not REPO_ROOT.joinpath("docs").is_dir():
        print("Gagal: folder docs/ tidak ditemukan. Jalankan skrip ini dari dalam repo "
              "Spec Blueprint.", file=sys.stderr)
        return 2

    args = prompt_if_missing(args)
    target = resolve_target(args)

    if target == REPO_ROOT:
        print("Gagal: folder tujuan sama dengan repo template. Pakai --target atau --in-place "
              "dari folder proyek lain.", file=sys.stderr)
        return 2

    if target.exists() and any(target.iterdir()) and not args.force and not args.dry_run:
        print(f"Gagal: {target} sudah ada dan tidak kosong.\n"
              f"Pakai --force kalau memang mau menulis ke sana, atau tentukan --target lain.",
              file=sys.stderr)
        return 2

    values = {
        "PROJECT_NAME": args.name,
        "PROJECT_TYPE": args.type,
        "DOMAIN": args.domain,
        "STACK": args.stack,
        "OWNER": args.owner,
        "DATE": dt.date.today().isoformat(),
    }

    print(f"Proyek  : {args.name}")
    print(f"Tujuan  : {target}")
    print(f"Jenis   : {args.type}")
    print(f"Stack   : {args.stack}")
    print(f"Contoh  : {'dibuang' if args.strip_examples else 'dipertahankan'}")
    print()

    if args.dry_run:
        print("=== RENCANA (dry-run, tidak ada yang ditulis) ===")
        for action, desc in plan_files(target, args.strip_examples):
            print(f"  [{action}] {desc}")
        print(f"\nTotal berkas: {len(plan_files(target, args.strip_examples))}")
        return 0

    try:
        target.mkdir(parents=True, exist_ok=True)
        stats = process_files(target, values, args.strip_examples, dry_run=False)
        write_readme(target, args, values, dry_run=False)
    except ScaffoldError as exc:
        print(f"Gagal: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Gagal menulis berkas: {exc}", file=sys.stderr)
        return 1

    print(f"Berkas disalin        : {stats['disalin']} (+1 README.md proyek)")
    print(f"Nilai placeholder diisi: {stats['placeholder_diganti']} kemunculan")
    if args.strip_examples:
        print(f"Blok contoh dibuang   : {stats['blok_contoh_dibuang']}")

    if not args.no_git:
        print(git_init(target))

    leftovers = check_unreplaced(target)
    print()
    if leftovers:
        print("PERINGATAN — placeholder masih tersisa:")
        for line in leftovers:
            print(f"  {line}")
    else:
        print("Tidak ada placeholder tersisa. Semua dokumen siap diisi.")

    print(f"""
Selesai. Langkah berikutnya:
  cd "{target}"
  1. Isi docs/00-discovery.md   (masalah, stakeholder, proses sekarang)
  2. Isi docs/01-prd.md         (tujuan, fitur, scope)
  3. Jalankan checklists/gate-1-sebelum-coding.md sebelum minta AI menulis kode
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
