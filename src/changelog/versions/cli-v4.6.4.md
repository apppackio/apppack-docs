---
title: "cli 4.6.4"
tags: [cli]
---

# cli 4.6.4

**Released:** 2025-03-05
**Repository:** apppack

## Removed

- Region creation no longer requires Docker Hub credentials. Existing apps must be upgraded for compatibility.

## Fixed

- Resizing a non-existent service in an undeployed app no longer causes an error.
- Network issues are now displayed separately from authentication errors. Previously, network failures during authentication token refresh were incorrectly shown as authentication errors.

---

[← Back to Changelog](../index.md)
