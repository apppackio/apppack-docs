---
title: "cli - v4.7.0"
tags: [cli]
---

# Version 4.7.0

**Released:** 2026-06-24

## Added

- `--json` persistent flag for machine-readable CLI output.
- `modify app` command to update some parameters of application/pipeline stacks.
- `build start` command now accepts optional `--ref` flag to build from specific git references (branches, tags, or commit hashes).

## Changed

- `create app`/`create pipeline` now guide repository authentication through AWS Code Connections (GitHub App) instead of the deprecated CodeBuild OAuth flow.
- Migrated interactive prompts from survey to huh.
- Upgraded to AWS SDK for Go v2.
- Updated to Go 1.25.4, upgraded go-jose to v4, and refreshed dependencies.

## Fixed

- Fixed issue where a stack update could revert unexpected parameters to template defaults.
- `ps resize` no longer prints a misleading warning for release/scheduler processes.
- Fixed `destroy` retry exit code.
- Handle `LoadBalancerNotFound` during cluster deletion.
- Added DynamoDB attribute tags so the SDK v2 correctly unmarshals stack items.

---

[← Back to Changelog](../index.md)
