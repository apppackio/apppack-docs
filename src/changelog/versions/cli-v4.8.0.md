---
title: "cli - v4.8.0"
tags: [cli]
---

# Version 4.8.0

**Released:** 2026-07-24

## Added

- `ps restart` command to restart your app's processes. By default it does a graceful, zero-downtime rolling restart (spins up replacement containers before stopping the old ones); add `--force` to immediately stop the running containers and let them relaunch.
- `version check` command to check if a newer CLI version is available.
- `version update` command to download and install the latest CLI version from GitHub releases.
- `shell --live`/`ps exec --live` now show each process's size (CPU/memory) in the selector, and print an advisory naming the process and its size after connecting.

## Fixed

- `ps resize` no longer fails on apps that have never had a successful release.
- `shell` now only uses a login shell (`bash -l`) for buildpack apps, avoiding cases where it clobbered a `PATH` set by a Dockerfile-based app's image.
- `selfupdate` now errors clearly when a downloaded binary exceeds the size limit, instead of silently truncating it to a confusing checksum mismatch.
- Commands other than `auth` no longer fail with a raw SDK error when the local `~/.aws` config has a partial/incomplete `default` profile.

---

[← Back to Changelog](../index.md)
