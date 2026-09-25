---
title: "cli - v4.8.3"
tags: [cli]
---

# Version 4.8.3

**Released:** 2026-09-22

## Fixed

- Interactive prompts no longer hide the options listed above the default. Any select whose default wasn't the first option rendered only from the default down, so `create app`'s "Public S3 Bucket" prompt defaulting to `no` showed no `yes` at all, and the instance-class pickers hid every class above the default. Pressing an arrow key revealed the missing options. Affects the yes/no addon prompts (private/public S3, SQS, database, Redis, Aurora, multi-AZ), the database and Redis instance-class pickers, and the database/Redis instance selectors.
- `config list -j` works again. `-j` was a shorthand for `--json` on `config list` before 4.7.0 promoted `--json` to a global flag, and removing the global shorthand in 4.8.2 took `config list -j` with it. The shorthand is registered on `config list` again; `--json` continues to work everywhere.
- The CLI now exits non-zero when it panics. A recovered panic was reported to Sentry and printed a message, but the process still exited 0, so CI jobs and scripts treated a crashed command as a success. The panic message now goes to stderr.

---

[← Back to Changelog](../index.md)
