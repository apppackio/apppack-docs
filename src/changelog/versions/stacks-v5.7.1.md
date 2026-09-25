---
title: "stacks - v5.7.1"
tags: [stacks]
---

# Version 5.7.1

**Released:** 2023-10-13

## Fixed

- Removed tag condition from IAM role statement and ELBv2 target groups. Tags aren't applied atomically, so you can end up with resources that can't be udpated or destroyed because they didn't have a tag applied yet.

---

[← Back to Changelog](../index.md)
