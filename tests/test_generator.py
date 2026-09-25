from datetime import datetime
from pathlib import Path

import pytest
from aggregate_changelogs import (
    ChangelogEntry,
    generate_index_page,
    generate_version_page,
    prune_stale_version_pages,
)


def entry(alias: str, version: str) -> ChangelogEntry:
    return ChangelogEntry(
        version=version,
        date=datetime.fromisoformat("2024-01-01"),
        repository=f"repo-{alias}",
        alias=alias,
        sections={"Added": ["something"]},
    )


@pytest.fixture
def versions_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "versions"
    directory.mkdir()
    return directory


def test_pages_for_versions_that_no_longer_exist_are_removed(
    versions_dir: Path,
) -> None:
    (versions_dir / "cli-v1.0.0.md").write_text("current")
    (versions_dir / "cli-v0.9.0.md").write_text("yanked upstream")
    (versions_dir / "oldalias-v3.0.0.md").write_text("repo dropped from config")

    prune_stale_version_pages(versions_dir, [entry("cli", "1.0.0")])

    assert {p.name for p in versions_dir.iterdir()} == {"cli-v1.0.0.md"}


def test_files_outside_the_versions_directory_are_untouched(
    versions_dir: Path,
) -> None:
    """index.md is a sibling of versions/ and must survive the prune."""
    index = versions_dir.parent / "index.md"
    index.write_text("the aggregated index")

    prune_stale_version_pages(versions_dir, [])

    assert index.read_text() == "the aggregated index"


def test_non_markdown_files_are_left_alone(versions_dir: Path) -> None:
    keep = versions_dir / ".gitkeep"
    keep.write_text("")

    prune_stale_version_pages(versions_dir, [])

    assert keep.exists()


def test_pruning_an_already_clean_directory_removes_nothing(
    versions_dir: Path,
) -> None:
    (versions_dir / "cli-v1.0.0.md").write_text("current")

    prune_stale_version_pages(versions_dir, [entry("cli", "1.0.0")])

    assert {p.name for p in versions_dir.iterdir()} == {"cli-v1.0.0.md"}


def test_index_date_subheading_names_the_alias_not_the_repository(
    tmp_path: Path,
) -> None:
    """The heading above it already says "cli", so the repo name read oddly."""
    index = tmp_path / "index.md"

    generate_index_page([entry("cli", "4.8.3")], index)

    assert "#tag:cli" in index.read_text()
    assert "repo-cli" not in index.read_text()


def test_version_page_shows_the_release_date_without_a_repository_line(
    tmp_path: Path,
) -> None:
    page = tmp_path / "cli-v4.8.3.md"

    generate_version_page(entry("cli", "4.8.3"), page)

    text = page.read_text()
    assert "**Released:** 2024-01-01\n\n" in text
    assert "Repository:" not in text
    assert "repo-cli" not in text


# These two lock the exact markdown the generators emit. They are
# characterization tests: they pass before and after the move to templates,
# which is the point -- the generated pages are committed, so a stray newline
# would churn 66 files.
VERSION_PAGE = """---
title: "cli - v4.8.3"
tags: [cli]
---

# Version 4.8.3

**Released:** 2024-01-01

## Added

- something

---

[← Back to Changelog](../index.md)
"""

INDEX_PAGE = """---
title: "AppPack Changelog"
# Keeps the per-release change sections out of the right rail.
toc_flat: true
---

# AppPack Changelog

This page aggregates changelogs from all AppPack repositories, showing the most recent changes first.

## [cli v4.8.3](versions/cli-v4.8.3.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**Release date:** 2024-01-01

### Added

- something

---

"""


def test_version_page_markdown_is_exactly_as_expected(tmp_path: Path) -> None:
    page = tmp_path / "cli-v4.8.3.md"

    generate_version_page(entry("cli", "4.8.3"), page)

    assert page.read_text() == VERSION_PAGE


def test_index_page_markdown_is_exactly_as_expected(tmp_path: Path) -> None:
    index = tmp_path / "index.md"

    generate_index_page([entry("cli", "4.8.3")], index)

    assert index.read_text() == INDEX_PAGE


def test_dollar_signs_in_changelog_content_are_not_treated_as_placeholders(
    tmp_path: Path,
) -> None:
    """`string.Template` does not rescan substituted values -- keep it that way.

    Changelog entries quote shell, so `$PATH` and `${HOME}` will turn up
    eventually. They are content, not template syntax.
    """
    item = "Honour $PATH and ${HOME} when they are set"
    release = ChangelogEntry(
        version="1.0.0",
        date=datetime.fromisoformat("2024-01-01"),
        repository="repo-cli",
        alias="cli",
        sections={"Fixed": [item]},
    )
    page = tmp_path / "cli-v1.0.0.md"

    generate_version_page(release, page)

    assert f"- {item}\n" in page.read_text()
