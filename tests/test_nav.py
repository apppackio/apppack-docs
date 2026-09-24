from datetime import datetime
from pathlib import Path

import pytest
from aggregate_changelogs import ChangelogEntry, write_changelog_nav

CONFIG = """site_name: AppPack Docs
nav:
  - index.md
  - Changelog:
      - changelog/index.md
      - Versions:
          # BEGIN changelog-nav (generated)
          # END changelog-nav (generated)
  - why-apppack.md
"""


def entry(alias: str, version: str) -> ChangelogEntry:
    return ChangelogEntry(
        version=version,
        date=datetime.fromisoformat("2024-01-01"),
        repository=f"repo-{alias}",
        alias=alias,
        sections={"Added": ["something"]},
    )


@pytest.fixture
def config(tmp_path: Path) -> Path:
    path = tmp_path / "mkdocs.yml"
    path.write_text(CONFIG)
    return path


def test_one_nav_entry_is_written_per_version_in_order(config: Path) -> None:
    write_changelog_nav(config, [entry("cli", "2.0.0"), entry("stacks", "9.1.0")])

    assert config.read_text() == """site_name: AppPack Docs
nav:
  - index.md
  - Changelog:
      - changelog/index.md
      - Versions:
          # BEGIN changelog-nav (generated)
          - changelog/versions/cli-v2.0.0.md
          - changelog/versions/stacks-v9.1.0.md
          # END changelog-nav (generated)
  - why-apppack.md
"""


def test_regenerating_replaces_the_previous_entries(config: Path) -> None:
    """A version that disappears must not linger in the nav."""
    write_changelog_nav(config, [entry("cli", "1.0.0"), entry("cli", "0.9.0")])

    write_changelog_nav(config, [entry("cli", "1.0.0")])

    assert "changelog/versions/cli-v0.9.0.md" not in config.read_text()
    assert "changelog/versions/cli-v1.0.0.md" in config.read_text()


def test_content_outside_the_markers_is_preserved(config: Path) -> None:
    write_changelog_nav(config, [entry("cli", "2.0.0")])

    text = config.read_text()
    assert text.startswith("site_name: AppPack Docs\n")
    assert "  - why-apppack.md\n" in text
    assert "      - changelog/index.md\n" in text


def test_a_config_without_markers_is_an_error(tmp_path: Path) -> None:
    path = tmp_path / "mkdocs.yml"
    path.write_text("site_name: AppPack Docs\nnav:\n  - index.md\n")

    with pytest.raises(ValueError, match="changelog-nav markers"):
        write_changelog_nav(path, [entry("cli", "2.0.0")])


def test_writing_an_empty_version_list_clears_the_block(config: Path) -> None:
    write_changelog_nav(config, [entry("cli", "2.0.0")])

    write_changelog_nav(config, [])

    assert "changelog/versions/" not in config.read_text()
    assert "# BEGIN changelog-nav (generated)" in config.read_text()
