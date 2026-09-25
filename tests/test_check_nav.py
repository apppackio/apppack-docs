"""The nav check is a CI gate, and NOT_IN_NAV punches a hole in it.

These tests pin the hole to exactly the changelog pages the index links to, so
an ordinary orphaned page still fails the build.
"""

import check_nav_complete
import pytest


@pytest.mark.parametrize(
    "page",
    [
        "changelog/tags.md",
        "changelog/versions/cli-v4.8.3.md",
        "changelog/versions/stacks-v5.17.3.md",
    ],
)
def test_changelog_pages_are_allowed_to_be_absent_from_nav(page: str) -> None:
    assert check_nav_complete.is_unlisted_on_purpose(page)


@pytest.mark.parametrize(
    "page",
    [
        "changelog/index.md",
        "how-to/apps/releases.md",
        "tutorials/initial-setup.md",
        "index.md",
        "under-the-hood/domains.md",
        "how-to/apps/troubleshoot-deployment-failures.md",
    ],
)
def test_every_other_page_still_has_to_be_in_nav(page: str) -> None:
    assert not check_nav_complete.is_unlisted_on_purpose(page)


def test_the_changelog_index_itself_is_not_excused() -> None:
    """It is the one changelog page the sidebar must link to."""
    assert not check_nav_complete.is_unlisted_on_purpose("changelog/index.md")
