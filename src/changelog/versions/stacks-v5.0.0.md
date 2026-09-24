---
title: "stacks 5.0.0"
tags: [stacks]
---

# stacks 5.0.0

**Released:** 2023-03-21

## Added

- Added an Athena Workgroup to the cluster stack which defines the results location and encryption configuration
- Update policies for changes at AWS
- Updated Cloudwatch log access policy with newly added permissions
- Explicity set the public access configuration on Public S3 buckets
- Explicity allow `ecs:TagResource` for AppPack and app users
- Added role for all cross-account event rules

## Changed

- Switched the build scripts from being delivered via the stack to being delivered via the build container
- Pipeline ECR repositories will now retain 200 images (instead of 50)

---

[← Back to Changelog](../index.md)
