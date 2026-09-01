#!/usr/bin/env python3
"""Verify every page under src/ is reachable from the nav in mkdocs.yml.

Zensical builds pages that are missing from `nav:` without complaining: they
get a URL and land in sitemap.xml and the search index, but nothing links to
them. Its config module is explicit that this will not be validated upstream
for now ("we only support validation of links right now, as navigation will
change significantly"), and the literate-nav directory globs that used to pick
up new pages automatically are gone, so we check it here instead.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONFIG = ROOT / "mkdocs.yml"
DOCS = ROOT / "src"

# mkdocs.yml carries `!!python/name:` tags, which a plain YAML safe-load
# rejects, so pull the nav block out textually instead of parsing the file.
NAV_START = re.compile(r"^nav:\s*$")
TOP_LEVEL_KEY = re.compile(r"^[^\s#]")
MD_PATH = re.compile(r"[\w./-]+\.md")


def nav_pages() -> set[str]:
    lines = CONFIG.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if NAV_START.match(line))
    except StopIteration:
        sys.exit(f"No `nav:` block found in {CONFIG}")

    pages = set()
    for line in lines[start + 1 :]:
        # The nav block runs until the next top-level key.
        if TOP_LEVEL_KEY.match(line):
            break
        pages.update(MD_PATH.findall(line))
    return pages


def main() -> int:
    referenced = nav_pages()
    if not referenced:
        print(f"No pages referenced in the `nav:` block of {CONFIG}", file=sys.stderr)
        return 1

    on_disk = {str(p.relative_to(DOCS)) for p in DOCS.rglob("*.md")}
    missing = sorted(on_disk - referenced)
    if missing:
        print(
            f"{len(missing)} page(s) exist under {DOCS.relative_to(ROOT)}/ but are "
            f"not in the `nav:` block of {CONFIG.name}, so nothing links to them:",
            file=sys.stderr,
        )
        for page in missing:
            print(f"  - {page}", file=sys.stderr)
        print(
            "\nAdd them to `nav:` in mkdocs.yml. Command line reference pages are "
            "generated -- run `make cli-docs` instead of adding them by hand.",
            file=sys.stderr,
        )
        return 1

    stale = sorted(referenced - on_disk)
    if stale:
        print(
            f"{len(stale)} page(s) are in the `nav:` block of {CONFIG.name} but do "
            f"not exist on disk, so the nav links to them are dead:",
            file=sys.stderr,
        )
        for page in stale:
            print(f"  - {page}", file=sys.stderr)
        print(
            "\nIf these are command line reference pages, run `make cli-docs`.",
            file=sys.stderr,
        )
        return 1

    print(f"All {len(on_disk)} pages under src/ are referenced in the nav.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
