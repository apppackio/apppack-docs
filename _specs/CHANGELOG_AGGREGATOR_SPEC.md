# Changelog aggregation

Pulls `CHANGELOG.md` from several AppPack repositories, merges the releases by
date, and writes them into `src/changelog/` as pages this site builds.

This describes what was built. The original design predated the Zensical
migration and specified a separate `changelog_config.yml`, Material for MkDocs,
`_navigation.md`, and page generation in Python code. None of those survive.

## Moving parts

| Path | Role |
|------|------|
| `scripts/aggregate_changelogs.py` | Fetch, parse, merge, generate |
| `scripts/templates/*.md` | Page templates (`string.Template`) |
| `pyproject.toml` → `[[tool.changelog.repositories]]` | Which repositories to pull |
| `src/changelog/index.md` | Generated. Every release, newest first |
| `src/changelog/versions/<alias>-v<version>.md` | Generated. One page per release |
| `src/changelog/tags.md` | Hand-written. Holds the per-repository listing |
| `.github/workflows/changelog_aggregation.yml` | Runs it three times a day |

Run it with `make changelog`.

## Configuration

Each repository is an entry in `pyproject.toml`:

```toml
[[tool.changelog.repositories]]
name = "apppack"            # repository name, used in log and warning messages
alias = "cli"               # short name; the page title, tag, and URL stem
url = "https://github.com/apppackio/apppack"
changelog_path = "CHANGELOG.md"   # may point into a monorepo subdirectory
public = true               # public: raw.githubusercontent. private: Contents API
```

`alias` is the identifier everywhere user-facing: `cli-v4.8.3.md`, the `cli`
tag, the `cli v4.8.3` heading. Two entries may share a `name` when they are
different directories of one monorepo, as long as their aliases differ.

### Adding a repository

Three places, all in play:

1. `[[tool.changelog.repositories]]` in `pyproject.toml`
2. `extra.tags` in `mkdocs.yml` — maps the tag name to an icon identifier
3. `theme.icon.tag` in `mkdocs.yml` — the icon for that identifier

Both 2 and 3 are needed for the tag to carry its own icon. `partials/tags.html`
adds `md-tag-icon` only when `extra.tags` exists at all, and `md-tag--<id>` only
when the tag has an entry in it:

| `extra.tags` | Chip classes | Icon |
|---|---|---|
| block absent | `md-tag` | none, for every tag on the site |
| present, tag missing | `md-tag md-tag-icon` | the `default` one |
| present, tag listed | `md-tag md-tag-icon md-tag--<id>` | the configured one |

Beware that the index page will not show you this. Its pill is written by
`scripts/templates/index_entry.md`, which hardcodes the three classes, so it
renders the right icon whether or not the tag is configured. The release pages
are where the plugin actually generates the chip, so check one of those.

## Authentication

`--token`, else `GITHUB_TOKEN`, else `gh auth token`. Locally, an authenticated
`gh` is enough. In CI it is the `APPPACK_DOCS_TOKEN` secret, which needs read on
the private repositories and write on this one.

## Behaviour worth knowing

**Unreleased sections are skipped.** Deliberately, via `show_unreleased=False`.

**A version heading with no release date is warned about, not dropped.**
`keepachangelog` discards undated versions silently, so the parser compares the
version headings in the source against what came back and warns about the
difference. A version whose date will not parse is warned about and skipped
rather than aborting the run.

**Pages for versions that no longer exist are deleted.** Anything in
`versions/` that is not in the current merge gets removed, so a renamed alias
or a dropped repository does not leave orphans published.

**Fetch failures abort the run.** No partial output. Parse problems warn and
continue; network and auth problems stop everything.

## Navigation

Only `changelog/index.md` appears in `nav:`. The release pages and the listing
would add about 65 sidebar entries, and the index already links to all of them.

`scripts/check_nav_complete.py` fails the build over pages missing from `nav:`,
so it carries a `NOT_IN_NAV` allowlist for `changelog/tags.md` and
`changelog/versions/*.md`. It is deliberately narrow — `changelog/index.md` is
not excused — and `tests/test_check_nav.py` pins it that way.

## Tags

Zensical's `tags` plugin needs **>= 0.0.60**. Earlier versions accept the plugin
name and do nothing at all. `tags_file` is likewise accepted and silently
dropped, which is why the listing on `tags.md` uses the listings directive
instead.

Two forked partials in `theme_overrides/partials/`:

- `content.html` — moves the tag above the page title. Upstream renders it after
  the content, which put it below the release page's footer.
- `toc-item.html` — adds a `toc_flat` front matter flag, used by the index to
  keep per-release change sections out of the right rail.

Both are copies of files upstream marks "automatically generated".
`tests/test_theme_overrides.py` holds the upstream originals as fixtures and
fails when Zensical changes them, so a version bump cannot silently leave the
forks serving stale markup.

## Publishing

The workflow commits to `main`, then fast-forwards `deploy/prod`, which triggers
the build and deploy in `ci_cd.yml`. The push uses a PAT rather than
`GITHUB_TOKEN` for two reasons: the private repositories need it, and pushes
made with `GITHUB_TOKEN` do not trigger other workflows, so the deploy would
never fire.

The `deploy/prod` push is fast-forward only. If the branches have diverged the
job fails rather than overwriting what is deployed.

It does not run `make check-nav`. `src/command-line-reference` is gitignored, so
a fresh checkout has none of it and the nav's 84 entries all read as dead links;
the check belongs in `ci_cd.yml`, which generates those pages first.

## Known gaps

- **No retry.** A transient GitHub 5xx fails the run. The original design asked
  for three attempts with backoff; it was never built.
- **Fetch failures print a traceback.** The last line names the repository and
  the status code, but it should say which credential to check.
- **The default branch is hardcoded to `main`** for public repositories
  (`aggregate_changelogs.py`, `raw_url`). Private ones go through the Contents
  API, which resolves the default branch correctly.
- **Warnings identify a repository by `name`.** Two entries pointing at
  different directories of one monorepo produce warnings that cannot be told
  apart.
