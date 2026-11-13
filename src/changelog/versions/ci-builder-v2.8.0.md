---
title: "ci-builder - v2.8.0"
tags: [ci-builder]
---

# Version 2.8.0

**Released:** 2026-11-13

## Added

- After pushing the commit, `build-NNN` and `latest` tags, the builder invokes
- the app's SOCI index generator asynchronously when
- `SOCI_GENERATOR_FUNCTION_ARN` is set. It sends only the tag to convert; the
- generator reads the repository and registry from its environment. An empty
- variable is a no-op, so existing stacks are unchanged.

## Changed

- Updated the `pack` CLI to 0.40.10

## Fixed

- The deploy job constructs the GHCR image reference from the run id. It
- previously read an empty `build-image` job output and could not publish.

---

[← Back to Changelog](../index.md)
