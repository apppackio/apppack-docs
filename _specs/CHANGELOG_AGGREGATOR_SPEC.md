# Changelog Aggregation Feature Specification

## Overview

This feature will aggregate CHANGELOG.md files from multiple AppPack repositories, parse them using the `keepachangelog` library, merge them chronologically, and generate individual MkDocs pages for each version entry with a combined index page.

## Objectives

1. **Fetch** CHANGELOG.md from multiple repositories (public and private)
2. **Parse** changelogs using the keepachangelog format
3. **Merge** entries in date descending order
4. **Generate** individual pages for each version with repository tags
5. **Create** a list page showing all versions and their changelog entries
6. **Support** local execution and scheduled GitHub Actions runs (3x daily)
7. **Plan** for extensibility to add more repositories

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                  Changelog Aggregator                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Fetcher    │  │    Parser    │  │   Generator  │      │
│  │              │  │              │  │              │      │
│  │ • Git clone  │─▶│ keepachange  │─▶│ MkDocs pages │      │
│  │ • GH API     │  │ log library  │  │ generation   │      │
│  │ • Auth       │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
          │                                         │
          ▼                                         ▼
    Local Execution                        GitHub Actions
    (CLI script)                          (scheduled workflow)
```

### Directory Structure

```
/workspace/
├── scripts/
│   └── aggregate_changelogs.py        # Main aggregation script
├── changelog_config.yml               # Repository configuration
├── src/
│   └── changelog/
│       ├── index.md                   # Combined changelog list page
│       └── versions/
│           ├── cli-v1.2.3.md         # Individual version pages
│           ├── stacks-v2.0.1.md
│           └── ci-builder-v0.5.0.md
└── .github/
    └── workflows/
        └── changelog_aggregation.yml  # GHA workflow (3x daily)
```

## Data Structures

### Repository Configuration (`changelog_config.yml`)

```yaml
repositories:
  - name: apppack
    alias: cli
    url: https://github.com/apppackio/apppack
    changelog_path: CHANGELOG.md
    public: true

  - name: apppack-codebuild-image
    alias: ci-builder
    url: https://github.com/apppackio/apppack-codebuild-image
    changelog_path: CHANGELOG.md
    public: false

  - name: apppack-backend
    alias: stacks
    url: https://github.com/apppackio/apppack-backend
    changelog_path: formations/CHANGELOG.md  # Monorepo subdirectory
    public: false

# Future repositories can be added here
# - name: future-repo
#   alias: feature-x
#   url: https://github.com/apppackio/future-repo
#   changelog_path: CHANGELOG.md
#   public: false
```

### Parsed Changelog Entry Structure

```python
@dataclass
class ChangelogEntry:
    """Represents a single version entry from a changelog"""
    version: str              # e.g., "1.2.3"
    date: datetime            # Release date
    repository: str           # Repository name
    alias: str               # Short alias (cli, stacks, ci-builder)
    sections: dict[str, list[str]]  # {Added: [...], Fixed: [...], ...}

    @property
    def version_id(self) -> str:
        """Unique identifier: 'cli-v1.2.3'"""
        return f"{self.alias}-v{self.version}"

    @property
    def page_path(self) -> str:
        """Path to generated page: 'changelog/versions/cli-v1.2.3.md'"""
        return f"changelog/versions/{self.version_id}.md"
```

## Component Details

### 1. Fetcher (`scripts/aggregate_changelogs.py` - FetcherModule)

**Responsibilities:**
- Read configuration from `changelog_config.yml`
- Clone/fetch repositories to temporary directory
- Handle authentication for private repositories
- Extract CHANGELOG.md from correct path (including monorepo subdirs)

**Authentication Strategy:**

**Local execution:**
- Automatically uses `gh auth token` if GitHub CLI is installed and authenticated
- Falls back to `GITHUB_TOKEN` environment variable
- Can be explicitly set with `--token` flag

**GitHub Actions:**
- Use `GITHUB_TOKEN` with appropriate permissions
- Requires token with `repo` scope for private repositories
- Token passed as environment variable

**Implementation approach:**
```python
def fetch_changelog(repo_config: dict, auth_token: Optional[str] = None) -> str:
    """Fetch CHANGELOG.md content from a repository"""
    if repo_config['public']:
        # Use GitHub raw content API (no auth needed)
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{changelog_path}"
        return requests.get(url).text
    else:
        # Use authenticated API
        headers = {"Authorization": f"token {auth_token}"}
        # GitHub Contents API
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{changelog_path}"
        response = requests.get(url, headers=headers)
        # Decode base64 content
        return base64.b64decode(response.json()['content']).decode('utf-8')
```

### 2. Parser (`scripts/aggregate_changelogs.py` - ParserModule)

**Responsibilities:**
- Parse CHANGELOG.md using `keepachangelog` library
- Extract version, date, and change sections
- Handle malformed or missing dates gracefully
- Normalize data into `ChangelogEntry` objects

**Implementation:**
```python
from keepachangelog import to_dict

def parse_changelog(content: str, repo_name: str, alias: str) -> list[ChangelogEntry]:
    """Parse changelog content into structured entries"""
    # Parse with show_unreleased=False to exclude unreleased versions
    changelog_dict = to_dict(content, show_unreleased=False)
    entries = []

    for version, data in changelog_dict.items():
        if version == "metadata":
            continue

        entry = ChangelogEntry(
            version=version,
            date=parse_date(data.get('release_date')),
            repository=repo_name,
            alias=alias,
            sections={
                'Added': data.get('added', []),
                'Changed': data.get('changed', []),
                'Deprecated': data.get('deprecated', []),
                'Removed': data.get('removed', []),
                'Fixed': data.get('fixed', []),
                'Security': data.get('security', []),
            }
        )
        entries.append(entry)

    return entries
```

### 3. Generator (`scripts/aggregate_changelogs.py` - GeneratorModule)

**Responsibilities:**
- Sort all entries by date (descending)
- Generate individual markdown pages for each version
- Generate combined index page with all versions
- Format content with proper MkDocs metadata

**Individual Version Page Template:**

```markdown
---
title: "{alias} {version}"
---

# {alias} {version}

**Released:** {date}
**Repository:** {repository}

{for section, items in sections}
## {section}

{for item in items}
- {item}
{endfor}
{endfor}

---

[← Back to Changelog](/changelog/)
```

**Index Page Template:**

```markdown
---
title: "AppPack Changelog"
---

# AppPack Changelog

This page aggregates changelogs from all AppPack repositories, showing the most recent changes first.

{for entry in sorted_entries}
## [{entry.alias} {entry.version}](/changelog/versions/{entry.version_id}/) {:.changelog-entry}

**{entry.date}** • **{entry.repository}**

{for section, items in entry.sections if items}
### {section}
{for item in items}
- {item}
{endfor}
{endfor}

---

{endfor}
```

## Script Interface

### CLI Usage (Local Execution)

```bash
# Install dependencies
uv add keepachangelog pyyaml requests

# Run aggregator (automatically uses gh CLI if authenticated)
uv run python scripts/aggregate_changelogs.py

# Or with explicit token via environment variable
GITHUB_TOKEN=ghp_xxx uv run python scripts/aggregate_changelogs.py

# Or with explicit token via flag
uv run python scripts/aggregate_changelogs.py --token ghp_xxx
```

### Script Arguments

```python
parser = argparse.ArgumentParser(description='Aggregate AppPack changelogs')
parser.add_argument('--config', default='changelog_config.yml',
                    help='Path to repository configuration file')
parser.add_argument('--output', default='merged_changelog.md',
                    help='Output file for merged changelog')
parser.add_argument('--token', help='GitHub personal access token (auto-detects from gh CLI)')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='Enable verbose logging')
```

## GitHub Actions Integration

### Workflow File (`.github/workflows/changelog_aggregation.yml`)

```yaml
name: Aggregate Changelogs

on:
  schedule:
    # Run 3 times per day: 00:00, 08:00, 16:00 UTC
    - cron: '0 0,8,16 * * *'
  workflow_dispatch:  # Allow manual trigger

permissions:
  contents: write  # For committing generated files

jobs:
  aggregate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout docs repo
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.APPPACK_DOCS_TOKEN }}  # Personal access token

      - name: Set up uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: uv sync

      - name: Aggregate changelogs
        env:
          GITHUB_TOKEN: ${{ secrets.APPPACK_DOCS_TOKEN }}
        run: |
          uv run python scripts/aggregate_changelogs.py --verbose

      - name: Check for changes
        id: verify_diff
        run: |
          git diff --quiet src/changelog/ || echo "changed=true" >> $GITHUB_OUTPUT

      - name: Commit and push if changed
        if: steps.verify_diff.outputs.changed == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add src/changelog/
          git commit -m "Update aggregated changelogs"
          git push
```

### Authentication for Private Repos

**GitHub Token Requirements:**
- Needs `repo` scope to access private repositories
- Created as a Personal Access Token (Classic) or Fine-Grained Token
- Stored as repository secret: `APPPACK_DOCS_TOKEN`

**Token Setup:**
1. Create PAT at: https://github.com/settings/tokens
2. Grant scopes: `repo` (Full control of private repositories)
3. Add to repository secrets: Settings → Secrets → Actions → New secret
4. Name: `APPPACK_DOCS_TOKEN`

## Navigation Integration

### Update `src/_navigation.md`

```markdown
* [Home](index.md)
* [Why AppPack?](why-apppack.md)
* ...existing sections...
* [Changelog](changelog/index.md)
  * [All Versions](changelog/index.md)
* [Under the Hood](under-the-hood/index.md)
```

### Update `mkdocs.yml` (if needed)

No changes needed - MkDocs will automatically discover pages in `src/changelog/`.

## Error Handling

### Fail Fast Strategy

The script will fail immediately if any repository is unavailable or has errors. This ensures we don't generate partial/incomplete changelog data.

1. **Missing changelog:** Fail with error message indicating which repo failed
2. **Parse error:** Fail with error showing malformed changelog
3. **Auth failure:** Fail with clear error message about authentication
4. **Network timeout:** Retry with exponential backoff (3 attempts), then fail
5. **Malformed dates:** Fail with error showing which version has invalid date

All errors should be logged with clear messages to help debugging.

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('changelog_aggregator')
```

## Testing Strategy

### Unit Tests

```python
# tests/test_parser.py
def test_parse_keepachangelog_format():
    """Test parsing valid keepachangelog format"""

def test_handle_missing_dates():
    """Test graceful handling of missing dates"""

def test_merge_multiple_changelogs():
    """Test correct chronological ordering"""

# tests/test_fetcher.py
def test_fetch_public_repo():
    """Test fetching from public repository"""

def test_fetch_private_repo_with_auth():
    """Test fetching from private repository"""

def test_monorepo_subdirectory():
    """Test fetching from monorepo subdirectory"""
```

### Integration Tests

```python
# tests/test_integration.py
def test_full_aggregation_pipeline():
    """Test complete aggregation from fetch to generation"""
```

## CSS Styling

### Custom Styles (`src/stylesheets/extra.css`)

```css
/* Changelog entry styling */
.changelog-entry {
    color: var(--md-primary-fg-color);
    border-left: 4px solid var(--md-primary-fg-color);
    padding-left: 1rem;
    margin-left: -1rem;
}

/* Repository tags */
.repo-tag {
    display: inline-block;
    padding: 0.2em 0.6em;
    font-size: 0.875em;
    font-weight: 600;
    border-radius: 0.25rem;
    background-color: var(--md-primary-fg-color--light);
    color: white;
}

.repo-tag.cli { background-color: #7c3aed; }
.repo-tag.stacks { background-color: #2563eb; }
.repo-tag.ci-builder { background-color: #059669; }
```

## Implementation Phases

### Phase 1: Core Functionality
- [ ] Create `scripts/aggregate_changelogs.py`
- [ ] Implement fetcher for public repos
- [ ] Implement parser using keepachangelog
- [ ] Implement basic generator
- [ ] Create `changelog_config.yml`
- [ ] Test locally with CLI repo

### Phase 2: Authentication & Private Repos
- [ ] Add authentication support (GitHub token)
- [ ] Test with private repos (ci-builder, stacks)
- [ ] Handle monorepo subdirectories
- [ ] Add error handling and logging

### Phase 3: Page Generation
- [ ] Design page templates
- [ ] Generate individual version pages
- [ ] Generate combined index page
- [ ] Add CSS styling
- [ ] Update navigation

### Phase 4: GitHub Actions
- [ ] Create workflow file
- [ ] Set up secrets (APPPACK_DOCS_TOKEN)
- [ ] Test manual workflow dispatch
- [ ] Enable scheduled runs (3x daily)
- [ ] Add commit automation

### Phase 5: Polish & Documentation
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Write README for the script
- [ ] Add error notifications (optional)
- [ ] Performance optimization (caching)

## Future Enhancements

1. **Caching:** Cache fetched changelogs to avoid rate limits
2. **Diff detection:** Only regenerate pages if changelog changed
3. **RSS feed:** Generate RSS feed for changelog updates
4. **Search integration:** Ensure changelog entries are searchable
5. **Version filtering:** Add UI to filter by repository or date range
6. **Breaking changes:** Highlight breaking changes prominently

## Dependencies

Add to `pyproject.toml`:

```toml
[project]
dependencies = [
    # ...existing dependencies...
    "keepachangelog>=2.0.0",
    "pyyaml>=6.0",
    "requests>=2.31.0",
]
```

## Security Considerations

1. **Token scope:** Use minimal required permissions
2. **Token rotation:** Rotate PAT regularly
3. **Secret management:** Never commit tokens to repository
4. **Rate limiting:** Respect GitHub API rate limits (5000 req/hour with auth)
5. **Input validation:** Validate repository configuration
6. **Output sanitization:** Escape markdown content to prevent XSS

## Success Criteria

- ✅ Changelog pages are generated successfully
- ✅ All 3 repositories are aggregated correctly
- ✅ Pages are sorted by date (newest first)
- ✅ Each version has its own page with correct repository tag
- ✅ Index page displays all versions with summaries
- ✅ Script runs successfully in local environment
- ✅ GitHub Actions runs 3x daily without errors
- ✅ Authentication works for private repositories
- ✅ Monorepo subdirectory (formations/) is handled correctly
- ✅ New repositories can be added easily via config file

## Questions & Decisions

### Resolved:
- **Format:** keepachangelog (specified by user)
- **Frequency:** 3x daily (specified by user)
- **Repos:** 3 initial repos with specific aliases

### Confirmed Decisions:
- ✅ **No unreleased changes** - Skip any "Unreleased" entries
- ✅ **Fail fast** - If any repo is unavailable, fail the entire script (don't generate partial data)
- ✅ **No notifications** - No email/Slack alerts
- ✅ **No external links** - Don't link to GitHub releases, just show changelog content
