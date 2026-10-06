---
title: "dashboard - v1.2.0"
tags: [dashboard]
---

# Version 1.2.0

**Released:** 2026-03-06

## Added

- Renovate configuration and workflow for automated dependency updates (pinning tailwindcss to v3, vue-router to v4)
- Pre-commit hooks: JSON/YAML validation, GitHub workflow and Renovate config schema checks, eslint, prettier
- Smoke tests with Vitest to catch dependency breakage

## Changed

- Updated dependencies to latest compatible versions

## Removed

- Storybook and related dependencies
- Unused dependencies

## Fixed

- Chart.js v4 compatibility for metrics charts
- Vega charts not rendering in production (blank white screen)

---

[← Back to Changelog](../index.md)
