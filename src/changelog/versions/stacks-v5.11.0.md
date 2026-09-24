---
title: "stacks 5.11.0"
tags: [stacks]
---

# stacks 5.11.0

**Released:** 2024-09-03

## Changed

- Increase timeout limit from 90 sec to 360 sec on DB manager lambda to allow for retries.

## Fixed

- Catch all Postgres errors for retrying DB Manger lambda operations.
- Ensure `IamAuthCustomResource` deletes prior to deletion of `Egress` in the security groups.

---

[← Back to Changelog](../index.md)
