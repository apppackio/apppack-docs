---
title: "cli 4.6.0"
tags: [cli]
---

# cli 4.6.0

**Released:** 2024-08-28

## Changed

- Limits the number of custom domains to 4.
- `ps resize` raises a warning for non-existent service.
- `reviewapps` cmd optionally accepts `-c`/ `account` flag.
- Implemented a check that throws an error if neither the `-c` flag nor the `APPPACK_ACCOUNT` environment variable is set and the user has multiple accounts. This ensures that users specify an account explicitly to avoid ambiguity.

## Fixed

- Prevent `Ctrl+C` from exiting the remote shell session prematurely.

---

[← Back to Changelog](../index.md)
