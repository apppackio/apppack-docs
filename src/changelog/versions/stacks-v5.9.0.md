---
title: "stacks 5.9.0"
tags: [stacks]
---

# stacks 5.9.0

**Released:** 2024-04-26

## Added

- Added support for Redis 7.1 and made it default for all new clusters
- Additional outputs on stackApp: `TargetGroupArnSuffix`

## Changed

- Docker Hub credentials are no longer used or required when creating a region.
- Delete extraneous lambda for db resource ID in favor of native debresourceid.

## Fixed

- Allow Multi-AZ parameter to be toggled after Redis cluster creation.

---

[← Back to Changelog](../index.md)
