---
title: "ci-builder 2.7.0"
tags: [ci-builder]
---

# ci-builder 2.7.0

**Released:** 2026-07-23

## Added

- CodeBuild environment variables are now mapped to neutral, industry-standard CI
- variable names and made available to builds — as `--build-arg` values for Docker
- builds and as environment variables for buildpack builds:
- `CI_COMMIT_REF` — source ref (from `CODEBUILD_WEBHOOK_HEAD_REF`, falling back to
- `CODEBUILD_SOURCE_VERSION` for manual builds)
- `CI_COMMIT_SHA` — resolved commit SHA (from `CODEBUILD_RESOLVED_SOURCE_VERSION`)
- `CI_BUILD_STARTED_AT` — build start time (from `CODEBUILD_START_TIME`)
- `CI_REPOSITORY_URL` — repository clone URL (from `CODEBUILD_SOURCE_REPO_URL`)
- Each variable is only set when its source value is present, so Dockerfile `ARG`
- defaults are preserved on non-CodeBuild or manual runs.

---

[← Back to Changelog](../index.md)
