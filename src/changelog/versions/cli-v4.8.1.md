---
title: "cli 4.8.1"
tags: [cli]
---

# cli 4.8.1

**Released:** 2026-08-07

## Fixed

- `create database` now honors flags like `--engine` instead of re-prompting for them. Any flag you set explicitly (`--engine`, `--instance-class`, `--multi-az`, etc.) is used directly and its interactive prompt is skipped. `--engine` accepts the fully-qualified engine name (`mysql`, `postgres`, `aurora-mysql`, `aurora-postgresql`) and is validated so a typo fails fast.
- `create app`/`create pipeline` now respect the `--addon-database` and `--addon-redis` flags, which were previously accepted but ignored. Interactively they preselect the addon; non-interactively they auto-select when the cluster has a single database/redis instance, and otherwise list the choices (use `--addon-database-name`/`--addon-redis-name` to pick one).

---

[← Back to Changelog](../index.md)
