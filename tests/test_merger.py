from datetime import datetime

from aggregate_changelogs import ChangelogEntry, ChangelogMerger


def entry(alias: str, version: str, date: str) -> ChangelogEntry:
    return ChangelogEntry(
        version=version,
        date=datetime.fromisoformat(date),
        repository=f"repo-{alias}",
        alias=alias,
        sections={"Added": ["something"]},
    )


def test_entries_from_all_repos_are_ordered_newest_first() -> None:
    cli = [entry("cli", "2.0.0", "2024-05-01"), entry("cli", "1.0.0", "2024-01-01")]
    stacks = [entry("stacks", "9.1.0", "2024-03-01")]

    merged = ChangelogMerger().merge_changelogs([cli, stacks])

    assert [e.version_id for e in merged] == [
        "cli-v2.0.0",
        "stacks-v9.1.0",
        "cli-v1.0.0",
    ]


def test_merging_keeps_every_entry() -> None:
    cli = [entry("cli", "2.0.0", "2024-05-01"), entry("cli", "1.0.0", "2024-01-01")]
    stacks = [entry("stacks", "9.1.0", "2024-03-01")]

    merged = ChangelogMerger().merge_changelogs([cli, stacks])

    assert len(merged) == 3
