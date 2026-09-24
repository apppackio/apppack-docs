---
title: "cli 4.8.2"
tags: [cli]
---

# cli 4.8.2

**Released:** 2026-08-10

## Fixed

- `db load` no longer fails with a shorthand collision error. Its `--jobs`/`-j` flag was clashing with the global `--json`/`-j` flag added in 4.7.0, breaking every `db load` invocation. `--json` no longer has a shorthand; `db load -j <n>` is unchanged.

---

[← Back to Changelog](../index.md)
