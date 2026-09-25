import logging

import pytest
from aggregate_changelogs import ChangelogParser

VALID_CHANGELOG = """# Changelog

## [2.1.0] - 2024-03-15

### Added

- A new thing

### Fixed

- An old thing

## [2.0.0] - 2024-01-02

### Removed

- A stale thing
"""


@pytest.fixture
def parser() -> ChangelogParser:
    return ChangelogParser()


def warning_messages(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [r.getMessage() for r in caplog.records if r.levelno >= logging.WARNING]


def test_parses_every_version_in_a_valid_changelog(parser: ChangelogParser) -> None:
    entries = parser.parse_changelog(VALID_CHANGELOG, "apppack", "cli")

    assert [e.version for e in entries] == ["2.1.0", "2.0.0"]
    assert [e.date.date().isoformat() for e in entries] == ["2024-03-15", "2024-01-02"]
    assert entries[0].sections["Added"] == ["A new thing"]
    assert entries[0].sections["Fixed"] == ["An old thing"]
    assert entries[0].sections["Removed"] == []
    assert entries[0].version_id == "cli-v2.1.0"


def test_valid_changelog_produces_no_warnings(
    parser: ChangelogParser, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger="changelog_aggregator")

    parser.parse_changelog(VALID_CHANGELOG, "apppack", "cli")

    assert warning_messages(caplog) == []


def test_undated_version_is_warned_about_instead_of_vanishing(
    parser: ChangelogParser, caplog: pytest.LogCaptureFixture
) -> None:
    """keepachangelog silently drops versions with no release date."""
    caplog.set_level(logging.WARNING, logger="changelog_aggregator")
    content = "# Changelog\n\n## [1.5.0]\n\n### Added\n\n- Undated release\n"

    entries = parser.parse_changelog(content, "apppack", "cli")

    assert entries == []
    assert any("1.5.0" in m for m in warning_messages(caplog))


def test_undated_version_does_not_hide_its_dated_siblings(
    parser: ChangelogParser, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger="changelog_aggregator")
    content = VALID_CHANGELOG + "\n## [1.9.0]\n\n### Fixed\n\n- Undated\n"

    entries = parser.parse_changelog(content, "apppack", "cli")

    assert [e.version for e in entries] == ["2.1.0", "2.0.0"]
    assert any("1.9.0" in m for m in warning_messages(caplog))


def test_malformed_date_is_skipped_with_a_warning_not_an_exception(
    parser: ChangelogParser, caplog: pytest.LogCaptureFixture
) -> None:
    """A bad date used to raise ValueError and abort the whole run."""
    caplog.set_level(logging.WARNING, logger="changelog_aggregator")
    content = "# Changelog\n\n## [1.5.0] - not-a-date\n\n### Added\n\n- Thing\n"

    entries = parser.parse_changelog(content, "apppack", "cli")

    assert entries == []
    assert any("1.5.0" in m and "not-a-date" in m for m in warning_messages(caplog))


def test_changelog_with_no_versions_at_all_is_warned_about(
    parser: ChangelogParser, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger="changelog_aggregator")
    content = "# Changelog\n\nWe have not shipped anything yet.\n"

    entries = parser.parse_changelog(content, "apppack", "cli")

    assert entries == []
    assert any("apppack" in m for m in warning_messages(caplog))


def test_unreleased_section_is_skipped_without_warning(
    parser: ChangelogParser, caplog: pytest.LogCaptureFixture
) -> None:
    """Unreleased is excluded on purpose, so it must not look like a parse failure."""
    caplog.set_level(logging.WARNING, logger="changelog_aggregator")
    content = "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- WIP\n" + VALID_CHANGELOG

    entries = parser.parse_changelog(content, "apppack", "cli")

    assert [e.version for e in entries] == ["2.1.0", "2.0.0"]
    assert warning_messages(caplog) == []


def test_section_headings_are_not_mistaken_for_versions(
    parser: ChangelogParser, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger="changelog_aggregator")

    parser.parse_changelog(VALID_CHANGELOG, "apppack", "cli")

    assert not any("Added" in m or "Fixed" in m for m in warning_messages(caplog))
