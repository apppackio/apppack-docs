from datetime import datetime
from pathlib import Path

import pytest
from aggregate_changelogs import ChangelogEntry, prune_stale_version_pages


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
