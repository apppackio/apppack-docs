"""Detect upstream drift in the theme partials we have forked.

theme_overrides/partials/*.html are copies of Zensical's own partials with one
line changed each. Upstream marks those files "automatically generated", so
they can change under us on a version bump and our copies would silently keep
serving the old markup.

Each fixture here is the upstream file as it stood when we forked it. When one
of these fails, Zensical has changed the original: diff it against the fixture,
re-apply our change on top of the new version, and refresh the fixture.

This is a change detector on purpose -- the thing being guarded is that the
file changed at all. What the overrides actually render is covered by the
build, not here.
"""

from pathlib import Path

import pytest
import zensical

UPSTREAM = Path(zensical.__file__).parent / "templates" / "partials"
FIXTURES = Path(__file__).parent / "fixtures" / "upstream"
OVERRIDES = Path(__file__).parent.parent / "theme_overrides" / "partials"

FORKED = ["content.html", "toc-item.html"]


@pytest.mark.parametrize("name", FORKED)
def test_upstream_partial_has_not_changed_since_we_forked_it(name: str) -> None:
    upstream = UPSTREAM / name
    fixture = FIXTURES / name

    assert upstream.exists(), f"Zensical no longer ships partials/{name}"
    assert upstream.read_text(encoding="utf-8") == fixture.read_text(
        encoding="utf-8"
    ), (
        f"Zensical's partials/{name} has changed since we forked it.\n"
        f"Diff {fixture} against {upstream}, re-apply our change to "
        f"{OVERRIDES / name}, then update the fixture."
    )


@pytest.mark.parametrize("name", FORKED)
def test_we_still_override_the_partial(name: str) -> None:
    """A fixture with no override left would guard nothing."""
    assert (OVERRIDES / name).exists()
