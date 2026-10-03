#!/usr/bin/env python3
"""Buat kerangka proyek baru dari template Spec Blueprint.

Menghasilkan dokumen spec-first (docs/ + AGENTS.md + prompts/ + checklists/),
dan opsional skeleton kode yang bisa dijalankan.

Contoh:
    python scripts/new_project.py
    python scripts/new_project.py --name "Sistem Kasir" --target ~/projects/kasir \
        --type cli --domain "retail / toko kelontong" \
        --stack "Python 3.10+ (stdlib), SQLite" \
        --owner "Toko Berkah" --strip-examples --with-code
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
TEMPLATE_DIR = REPO_ROOT / "templates"
EXAMPLE_DIR = REPO_ROOT / "examples"

# Isi template yang disalin ke proyek baru. Ambil dari templates/, bukan dari akar repo,
# supaya akar repo dipakai untuk dokumentasi repo ini sendiri.
COPY_ITEMS = ["docs", "prompts", "checklists", "AGENTS.md", "SKILL.md"]

# Skeleton kode yang bisa dijalankan (dipakai lewat --with-code).
CODE_ITEM = "code"

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
{code_section}
## Status

Spec: {spec_status}
"""

PROJECT_CODE_SECTION = """
## Menjalankan skeleton

Skeleton kode ada di `app/`. Jalankan dari akar proyek:

```bash
python -m app --help
python -m unittest discover -s tests -v
```

Skeleton ini hanya titik mulai: sesuaikan dengan FR di `docs/02-requirements.md`,
jangan menambah fitur yang belum punya ID requirement.
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
    if cwd.resolve() == REPO_ROOT:
        if args.in_place:
            # Menulis ke repo kit sendiri hampir selalu keliru: hasilnya mengotori template.
            raise ScaffoldError(
                "--in-place dijalankan dari dalam repo Spec Blueprint. Jalankan dari folder "
                "proyekmu, atau pakai --target untuk menentukan folder tujuan.")
        # Jangan menebak folder di luar repo (mis. langsung ke home). Minta ditentukan.
        raise ScaffoldError(
            "Skrip ini dijalankan dari dalam repo Spec Blueprint dan belum ada --target.\n"
            "  Tentukan tujuan, contoh:\n"
            f'    python scripts/new_project.py --name "{args.name}" --target ~/projects/{slug}')
    return cwd.resolve() if args.in_place else (cwd / slug).resolve()


# Berkas di dalam templates/code yang TIDAK disalin (sudah diwakili bagian lain proyek hasil).
CODE_SKIP = ["README.md"]


def code_dest(target: Path, rel: Path) -> Path:
    """Isi templates/code ditanam di akar proyek: app/, tests/, .gitignore — bukan di code/."""
    return target / rel


def template_sources(with_code: bool) -> list[tuple[str, Path]]:
    """Pasangan (nama relatif di proyek baru, path sumber di template)."""
    pairs: list[tuple[str, Path]] = []
    for item in COPY_ITEMS:
        src = TEMPLATE_DIR / item
        if not src.exists():
            raise ScaffoldError(
                f"Template tidak lengkap: templates/{item} tidak ditemukan di {REPO_ROOT}")
        pairs.append((item, src))
    if with_code:
        src = TEMPLATE_DIR / CODE_ITEM
        if not src.is_dir():
            raise ScaffoldError(
                f"--with-code diminta, tapi templates/{CODE_ITEM}/ tidak ada.")
        pairs.append((CODE_ITEM, src))
    return pairs


def _code_files(src: Path) -> list[Path]:
    """Semua berkas yang akan ditanam dari templates/code, di luar yang dilewati."""
    out: list[Path] = []
    for p in sorted(src.rglob("*")):
        if p.is_dir() or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(src)
        if rel.as_posix() in CODE_SKIP:
            continue
        out.append(p)
    return out


def plan_files(target: Path, with_code: bool) -> list[tuple[str, str]]:
    """Susun rencana tindakan: (jenis, keterangan)."""
    plan: list[tuple[str, str]] = []

    for item, src in template_sources(with_code):
        if item == CODE_ITEM:
            for f in _code_files(src):
                rel = f.relative_to(src)
                plan.append(("tanam", str(code_dest(target, rel)) + f"  (dari templates/code/{rel})"))
            continue
        dest = target / item
        if src.is_dir():
            for p in sorted(src.rglob("*")):
                if p.is_dir() or "__pycache__" in p.parts:
                    continue
                rel = p.relative_to(src)
                plan.append(("salin", str(dest / rel) + f"  (dari templates/{item}/{rel})"))
        else:
            plan.append(("salin", str(dest) + f"  (dari templates/{item})"))

    plan.append(("tulis", str(target / "README.md")))
    plan.append(("gerak", f"{target.name}/.git  (git init, kecuali --no-git)"))
    return plan


def process_files(target: Path, values: dict[str, str], strip: bool, with_code: bool,
                  dry_run: bool) -> dict[str, int]:
    """Salin, ganti placeholder, dan (opsional) buang blok contoh.

    Skeleton kode disalin apa adanya tanpa interpolasi: kalau ia berisi token {{...}}
    berarti template kodenya salah, dan itu harus terlihat — bukan ditutupi.
    """
    stats = {"disalin": 0, "placeholder_diganti": 0, "blok_contoh_dibuang": 0, "kode_disalin": 0}

    for item, src in template_sources(with_code):
        if item == CODE_ITEM:
            for f in _code_files(src):
                rel = f.relative_to(src)
                dest = code_dest(target, rel)
                if not dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dest)
                stats["kode_disalin"] += 1
            continue
        if src.is_dir():
            for f in sorted(src.rglob("*")):
                if f.is_dir() or "__pycache__" in f.parts:
                    continue
                rel = f.relative_to(src)
                _write_one(f, target / item / rel, values, strip, dry_run, stats)
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


def write_readme(target: Path, args: argparse.Namespace, with_code: bool, dry_run: bool) -> None:
    spec_status = "semua dokumen masih kosong — mulai dari docs/00-discovery.md"
    content = PROJECT_README.format(
        name=args.name,
        description=f"Dokumen perencanaan (PRD, requirements, arsitektur, workflow) untuk {args.name}.",
        type=args.type,
        domain=args.domain,
        stack=args.stack,
        spec_status=spec_status,
        code_section=PROJECT_CODE_SECTION if with_code else "",
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


def check_ui_noise(target: Path) -> tuple[list[str], int]:
    """Cari sisa blok contoh di hasil, dan hitung bagian yang masih harus diisi pengguna.

    `[isi]` BUKAN kesalahan: itu penanda bagian yang memang tugas pengguna mengisi.
    Yang kesalahan adalah blok contoh yang gagal dibuang saat --strip-examples.
    """
    noise: list[str] = []
    todo = 0
    for f in sorted(target.rglob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        if "EXAMPLE-START" in text:
            noise.append(f"{f.relative_to(target)}: blok contoh tidak terbuang")
        todo += text.count("[isi")
    return noise, todo


def list_examples() -> int:
    """Tampilkan contoh proyek terisi penuh yang tersedia."""
    if not EXAMPLE_DIR.is_dir():
        print("Belum ada contoh terisi di examples/.")
        return 0
    names = sorted(p.name for p in EXAMPLE_DIR.iterdir() if p.is_dir())
    if not names:
        print("Belum ada contoh terisi di examples/.")
        return 0
    print("Contoh proyek terisi penuh (lihat dulu sebelum mengisi dokumen sendiri):")
    for n in names:
        docs = EXAMPLE_DIR / n / "docs"
        jumlah = len(list(docs.glob("*.md"))) if docs.is_dir() else 0
        print(f"  examples/{n}  ({jumlah} dokumen terisi)")
    print("\nCoba jalankan contohnya, atau pakai sebagai acuan cara mengisi.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="new_project.py",
        description="Buat kerangka proyek baru (dokumen spec-first, opsional skeleton kode).",
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
    p.add_argument("--with-code", action="store_true",
                   help="Sertakan skeleton kode dari templates/code (bisa dijalankan & diuji)")
    p.add_argument("--no-git", action="store_true", help="Jangan jalankan git init")
    p.add_argument("--in-place", action="store_true",
                   help="Tulis ke folder saat ini, bukan ke subfolder baru")
    p.add_argument("--force", action="store_true",
                   help="Izinkan menulis ke folder yang sudah berisi file")
    p.add_argument("--dry-run", action="store_true",
                   help="Tampilkan rencana tanpa menulis apa pun")
    p.add_argument("--non-interactive", action="store_true",
                   help="Jangan bertanya; nilai yang kosong diisi default")
    p.add_argument("--list-examples", action="store_true",
                   help="Tampilkan contoh proyek terisi, lalu keluar")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_examples:
        return list_examples()

    if not (TEMPLATE_DIR / "docs").is_dir():
        print("Gagal: templates/docs/ tidak ditemukan. Jalankan skrip ini dari dalam repo "
              "Spec Blueprint.", file=sys.stderr)
        return 2

    args = prompt_if_missing(args)
    try:
        target = resolve_target(args)
    except ScaffoldError as exc:
        print(f"Gagal: {exc}", file=sys.stderr)
        return 2

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
    print(f"Kode    : {'disertakan (--with-code)' if args.with_code else 'tidak (dokumen saja)'}")
    print()

    if args.dry_run:
        print("=== RENCANA (dry-run, tidak ada yang ditulis) ===")
        plan = plan_files(target, args.with_code)
        for action, desc in plan:
            print(f"  [{action}] {desc}")
        print(f"\nTotal berkas: {len(plan)}")
        return 0

    try:
        target.mkdir(parents=True, exist_ok=True)
        stats = process_files(target, values, args.strip_examples, args.with_code, dry_run=False)
        write_readme(target, args, args.with_code, dry_run=False)
    except ScaffoldError as exc:
        print(f"Gagal: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Gagal menulis berkas: {exc}", file=sys.stderr)
        return 1

    print(f"Berkas dokumen disalin : {stats['disalin']} (+1 README.md proyek)")
    print(f"Nilai placeholder diisi: {stats['placeholder_diganti']} kemunculan")
    if args.strip_examples:
        print(f"Blok contoh dibuang    : {stats['blok_contoh_dibuang']}")
    if args.with_code:
        print(f"Berkas kode disalin    : {stats['kode_disalin']}")

    if not args.no_git:
        print(git_init(target))

    leftovers = check_unreplaced(target)
    noise, todo = check_ui_noise(target)
    print()
    if leftovers:
        print("PERINGATAN — placeholder masih tersisa:")
        for line in leftovers:
            print(f"  {line}")
    else:
        print("Tidak ada placeholder tersisa.")
    if noise:
        print("PERINGATAN — blok contoh tidak terbuang:")
        for line in noise:
            print(f"  {line}")
    print(f"Bagian yang masih harus kamu isi: {todo} penanda [isi] di {target.name}/docs/")

    print(f"""
Selesai. Langkah berikutnya:
  cd "{target}"
  1. Baca contoh terisi: python "{(REPO_ROOT / 'scripts' / 'new_project.py').as_posix()}" --list-examples
  2. Isi docs/00-discovery.md   (masalah, stakeholder, proses sekarang)
  3. Isi docs/01-prd.md         (tujuan, fitur, scope)
  4. Jalankan checklists/gate-1-sebelum-coding.md sebelum minta AI menulis kode
  5. Jalankan prompts/02-implement-feature.md satu fitur per sesi
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())