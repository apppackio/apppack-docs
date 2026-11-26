---
title: "stacks - v5.18.1"
tags: [stacks]
---

# Version 5.18.1

**Released:** 2026-11-25

## Changed

- **Larger database dumps and restores.** The task behind `apppack db dump` and
    `apppack db load` now has 120 GiB of temporary disk space, up from the 20 GiB
    default, so larger databases can be exported and imported.
- **Updated Python runtime.** The helper functions AppPack runs inside your
    stacks now use Python 3.13. No action is needed.

## Fixed

- Fixed stack updates that could delete or tear down resources that were still
    in use. In rare cases, changing certain settings could remove the GitHub OIDC
    provider (breaking GitHub Actions access) or run app teardown steps against a
    live app. Supporting resources now keep a stable identity across updates.
- Database log groups created by new database stacks now keep logs for 30 days
    as intended, instead of never expiring. Existing log groups are not changed.

---

[← Back to Changelog](../index.md)
