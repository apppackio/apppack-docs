---
title: "ci-builder 2.6.0"
tags: [ci-builder]
---

# ci-builder 2.6.0

**Released:** 2026-07-21

## Changed

- Removed support for EOL `heroku-20` builds

## Fixed

- Builds that use an in-dyno test database or Redis add-on (`heroku-postgresql:in-dyno`,
- `heroku-redis:in-dyno`) could intermittently fail during the pre-build phase with an
- error like `The container name "/db" is already in use`. These add-on containers now
- start with unique names, so a build no longer collides with a leftover container from
- a previous run.

---

[← Back to Changelog](../index.md)
