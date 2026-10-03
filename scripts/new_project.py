#!/usr/bin/env python3
"""Copy the template docs into a new project folder.

Examples:
    python scripts/new_project.py --target ~/projects/my-app
    python scripts/new_project.py --target ./my-app --force

What gets copied: docs/ (nine empty documents) + AGENTS.md (the contract for AI agents).
Everything is still empty and is meant for you to fill in yourself.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
# The source file is deliberately NOT named AGENTS.md inside this repo: a file with that name
# would be read as the contract for THIS repo by most AI agents, and the kit would be mistaken
# for an application project. It is renamed on the way out.
AGENTS_SRC = REPO_ROOT / "AGENT-RULES.md"
AGENTS_NAME = "AGENTS.md"


class CopyError(Exception):
    """An error that can be explained to the user without a stack trace."""


def normalize_target(raw: str) -> str:
    """Turn an MSYS-style path (/c/Users/...) into a Windows-style one (C:/Users/...).

    Under Git Bash, automatic path conversion is sometimes disabled, so /c/Users/x is passed
    through unchanged and read as C:\\c\\Users\\x.
    """
    if sys.platform.startswith("win") and re.match(r"^/[a-zA-Z]/", raw):
        return f"{raw[1].upper()}:{raw[2:]}"
    return raw


def source_files() -> list[tuple[Path, Path]]:
    """Pairs of (source, destination-relative) that will be copied."""
    if not DOCS_DIR.is_dir():
        raise CopyError(f"docs/ not found in {REPO_ROOT}")
    if not AGENTS_SRC.is_file():
        raise CopyError(f"{AGENTS_SRC.relative_to(REPO_ROOT)} not found in {REPO_ROOT}")

    pairs: list[tuple[Path, Path]] = []
    for f in sorted(DOCS_DIR.glob("*.md")):
        pairs.append((f, Path("docs") / f.name))
    pairs.append((AGENTS_SRC, Path(AGENTS_NAME)))
    return pairs


def run(args: argparse.Namespace) -> int:
    target = Path(normalize_target(args.target)).expanduser().resolve()

    if target == REPO_ROOT:
        print("Error: target is the template repo itself. Point --target at your project folder.",
              file=sys.stderr)
        return 2

    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"Error: {target} already exists and is not empty.\n"
              f"Use --force if you really want to write there.", file=sys.stderr)
        return 2

    pairs = source_files()

    if args.dry_run:
        print(f"Target : {target}")
        print(f"Files  : {len(pairs)}")
        for source, rel in pairs:
            print(f"  {rel}   (from {source.relative_to(REPO_ROOT)})")
        return 0

    try:
        for source, rel in pairs:
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, out)
    except OSError as exc:
        print(f"Error writing files: {exc}", file=sys.stderr)
        return 1

    doc_count = len(pairs) - 1
    print(f"Target : {target}")
    print(f"Copied : {len(pairs)} files ({doc_count} documents + {AGENTS_NAME})")
    print(f"""
Done. Next steps:
  cd "{target}"
  1. Fill in docs/00-problem.md      (problem, root cause, solution alternatives)
  2. Fill in docs/01-requirements.md (features, requirements with IDs, acceptance criteria)
  3. Continue with docs/02-design.md and the rest, in the order listed in docs/README.md
  4. Fill in the header of {AGENTS_NAME} before asking an AI agent to write code
""")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="new_project.py",
        description="Copy the template docs (docs/ + AGENTS.md) into a new project folder.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--target", required=True,
                   help="New project folder. Required — the script never guesses a target.")
    p.add_argument("--force", action="store_true",
                   help="Allow writing into a folder that already contains files")
    p.add_argument("--dry-run", action="store_true",
                   help="Show the plan without writing anything")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except CopyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
