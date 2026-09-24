---
title: "stacks 5.15.0"
tags: [stacks]
---

# stacks 5.15.0

**Released:** 2025-09-16
**Repository:** apppack-backend

## Changed

- Extend Athena query date range for load balancer logs from 60 days to full history (starting 2022/01/01)

## Fixed

- Update load balancer logs Athena query to include new `conn_trace_id` field
- Ensure all IAM policy statements include a proper `Sid` field
- Remove redundant port specifications in SecurityGroupEgress rules

---

[← Back to Changelog](../index.md)
