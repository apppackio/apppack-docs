---
title: "ci-builder - v2.9.0"
tags: [ci-builder]
---

# Version 2.9.0

**Released:** 2026-11-24

## Added

- Config vars listed under `[build] secrets` in `apppack.toml` are passed to
    Dockerfile builds as BuildKit secrets instead of build args, keeping them out
    of the image history and provenance attestations:

    ```toml
    [build]
    system = "dockerfile"
    secrets = ["NPM_TOKEN"]
    ```

    Read them in the Dockerfile with
    `RUN --mount=type=secret,id=NPM_TOKEN,env=NPM_TOKEN`. Buildpack builds reject
    `secrets`.

## Changed

- Updated the `pack` CLI to 0.40.11

## Fixed

- Buildpack builds no longer download the builder and stack images twice.
- A `[build] builder` hosted outside Docker Hub now works, such as one on
    `gcr.io`, `ghcr.io` or `public.ecr.aws`.

---

[← Back to Changelog](../index.md)
