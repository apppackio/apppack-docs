#!/usr/bin/env python3
"""
Aggregate changelogs from multiple AppPack repositories.

This script fetches CHANGELOG.md files from multiple repositories,
parses them using the keepachangelog format, and merges them
chronologically.
"""

import argparse
import base64
import logging
import os
import subprocess
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from keepachangelog import to_dict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("changelog_aggregator")

# Constants
REQUEST_TIMEOUT = 30  # seconds
MIN_URL_PATH_PARTS = 2


@dataclass
class ChangelogEntry:
    """Represents a single version entry from a changelog"""

    version: str
    date: datetime
    repository: str
    alias: str
    sections: dict[str, list[str]]

    @property
    def version_id(self) -> str:
        """Unique identifier: 'cli-v1.2.3'"""
        return f"{self.alias}-v{self.version}"


class ChangelogFetcher:
    """Fetches changelog content from GitHub repositories"""

    def __init__(self, auth_token: str | None = None) -> None:
        self.auth_token = auth_token

    def fetch_changelog(self, repo_config: dict) -> str:
        """
        Fetch CHANGELOG.md content from a repository.

        Args:
            repo_config: Repository configuration dict with url, changelog_path, etc.

        Returns:
            String content of the changelog

        Raises:
            ValueError: If URL is invalid or auth is missing for private repos
            requests.HTTPError: If the request fails
        """
        url = repo_config["url"]
        changelog_path = repo_config["changelog_path"]
        is_public = repo_config["public"]

        # Parse owner and repo from URL using urlparse
        # Format: https://github.com/owner/repo
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < MIN_URL_PATH_PARTS:
            msg = f"Invalid GitHub URL format: {url}"
            raise ValueError(msg)
        owner = path_parts[0]
        repo_name = path_parts[1]

        logger.info(
            "Fetching changelog from %s/%s at %s", owner, repo_name, changelog_path
        )

        if is_public:
            # Use raw content API (no auth needed)
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/main/{changelog_path}"
            logger.debug("Fetching from raw URL: %s", raw_url)

            response = requests.get(raw_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.text

        # Private repo - need authentication
        if not self.auth_token:
            msg = (
                f"Repository {owner}/{repo_name} is private but no auth token provided. "
                "Set GITHUB_TOKEN environment variable or use --token flag."
            )
            raise ValueError(msg)

        # Use GitHub Contents API
        api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{changelog_path}"
        headers = {
            "Authorization": f"token {self.auth_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        logger.debug("Fetching from API: %s", api_url)
        response = requests.get(api_url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        # GitHub API returns base64 encoded content
        content_b64 = response.json()["content"]
        return base64.b64decode(content_b64).decode("utf-8")


class ChangelogParser:
    """Parses changelog content using keepachangelog format"""

    def parse_changelog(
        self, content: str, repo_name: str, alias: str
    ) -> list[ChangelogEntry]:
        """
        Parse changelog content into structured entries.

        Args:
            content: Raw changelog markdown content
            repo_name: Repository name
            alias: Short alias for the repository

        Returns:
            List of ChangelogEntry objects
        """
        logger.info("Parsing changelog for %s (%s)", repo_name, alias)

        # Parse with show_unreleased=False to exclude unreleased versions
        # to_dict expects an iterable of lines or a file path
        changelog_dict = to_dict(content.splitlines(), show_unreleased=False)

        entries = []

        for version, data in changelog_dict.items():
            if version == "metadata":
                continue

            # Release date is in the metadata sub-dict
            metadata = data.get("metadata", {})
            release_date = metadata.get("release_date")

            date = datetime.fromisoformat(release_date)

            entry = ChangelogEntry(
                version=version,
                date=date,
                repository=repo_name,
                alias=alias,
                sections={
                    "Added": data.get("added", []),
                    "Changed": data.get("changed", []),
                    "Deprecated": data.get("deprecated", []),
                    "Removed": data.get("removed", []),
                    "Fixed": data.get("fixed", []),
                    "Security": data.get("security", []),
                },
            )
            entries.append(entry)
            logger.debug("  Parsed %s released on %s", entry.version_id, date.date())

        logger.info("Parsed %d versions from %s", len(entries), repo_name)
        return entries


class ChangelogMerger:
    """Merges multiple changelogs chronologically"""

    def merge_changelogs(
        self, all_entries: list[list[ChangelogEntry]]
    ) -> list[ChangelogEntry]:
        """
        Merge multiple changelog entry lists and sort by date (descending).

        Args:
            all_entries: List of lists of ChangelogEntry objects

        Returns:
            Single sorted list of all entries (newest first)
        """
        # Flatten the list of lists
        merged = []
        for entries in all_entries:
            merged.extend(entries)

        # Sort by date, newest first
        merged.sort(key=lambda e: e.date, reverse=True)

        logger.info("Merged %d total versions", len(merged))
        return merged


def load_config(config_path: str) -> dict:
    """Load repository configuration from pyproject.toml"""
    logger.info("Loading config from %s", config_path)

    config_file = Path(config_path)
    with config_file.open("rb") as f:
        pyproject = tomllib.load(f)

    if "tool" not in pyproject or "changelog" not in pyproject["tool"]:
        msg = "Config file must contain [tool.changelog] section"
        raise ValueError(msg)

    config = pyproject["tool"]["changelog"]
    logger.info("Loaded %d repositories", len(config["repositories"]))
    return config


def get_auth_token(args: argparse.Namespace) -> str | None:
    """Get GitHub authentication token from various sources"""
    # Priority: CLI arg > env var > gh CLI (automatic)
    if args.token:
        logger.info("Using token from --token argument")
        return args.token

    if "GITHUB_TOKEN" in os.environ:
        logger.info("Using token from GITHUB_TOKEN environment variable")
        return os.environ["GITHUB_TOKEN"]

    # Automatically try gh CLI if available
    logger.debug("Attempting to use gh CLI authentication")
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        token = result.stdout.strip()
        if token:
            logger.info("Using token from gh CLI")
            return token
    except FileNotFoundError:
        logger.debug("gh CLI not found")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        logger.debug("Failed to get token from gh CLI: %s", e)

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate changelogs from multiple AppPack repositories"
    )
    parser.add_argument(
        "--config",
        default="pyproject.toml",
        help="Path to pyproject.toml file",
    )
    parser.add_argument(
        "--output",
        default="merged_changelog.md",
        help="Output file for merged changelog",
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (auto-detects from gh CLI if not provided)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Load configuration
    config = load_config(args.config)

    # Get auth token
    auth_token = get_auth_token(args)
    if not auth_token:
        logger.warning(
            "No authentication token found - only public repos will be accessible. "
            "Authenticate with 'gh auth login' or set GITHUB_TOKEN environment variable."
        )

    # Initialize components
    fetcher = ChangelogFetcher(auth_token)
    parser_obj = ChangelogParser()
    merger = ChangelogMerger()

    # Fetch and parse all changelogs
    all_entries = []
    for repo_config in config["repositories"]:
        # Fetch
        content = fetcher.fetch_changelog(repo_config)

        # Parse
        entries = parser_obj.parse_changelog(
            content, repo_config["name"], repo_config["alias"]
        )
        all_entries.append(entries)

    # Merge all entries
    merged = merger.merge_changelogs(all_entries)

    # Output merged changelog
    logger.info("Writing merged changelog to %s", args.output)
    output_file = Path(args.output)
    with output_file.open("w") as f:
        f.write("# AppPack Merged Changelog\n\n")
        f.write(f"Total versions: {len(merged)}\n\n")
        f.write("---\n\n")

        for entry in merged:
            f.write(f"## {entry.alias} {entry.version}\n\n")
            f.write(f"**Released:** {entry.date.strftime('%Y-%m-%d')}\n")
            f.write(f"**Repository:** {entry.repository}\n\n")

            for section_name, items in entry.sections.items():
                if items:
                    f.write(f"### {section_name}\n\n")
                    f.writelines(f"- {item}\n" for item in items)
                    f.write("\n")

            f.write("---\n\n")

    logger.info("✓ Successfully aggregated changelogs!")
    logger.info("  Total versions: %d", len(merged))
    logger.info("  Output file: %s", args.output)


if __name__ == "__main__":
    main()
