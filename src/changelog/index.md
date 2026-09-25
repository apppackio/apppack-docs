---
title: "AppPack Changelog"
# Keeps the per-release change sections out of the right rail.
toc_flat: true
---

# AppPack Changelog

This page aggregates changelogs from all AppPack repositories, showing the most recent changes first.

## [cli v4.8.4](versions/cli-v4.8.4.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2026-09-24**

### Changed

- Upgraded the AWS SDK.

---

## [cli v4.8.3](versions/cli-v4.8.3.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2026-09-22**

### Fixed

- Interactive prompts no longer hide the options listed above the default. Any select whose default wasn't the first option rendered only from the default down, so `create app`'s "Public S3 Bucket" prompt defaulting to `no` showed no `yes` at all, and the instance-class pickers hid every class above the default. Pressing an arrow key revealed the missing options. Affects the yes/no addon prompts (private/public S3, SQS, database, Redis, Aurora, multi-AZ), the database and Redis instance-class pickers, and the database/Redis instance selectors.
- `config list -j` works again. `-j` was a shorthand for `--json` on `config list` before 4.7.0 promoted `--json` to a global flag, and removing the global shorthand in 4.8.2 took `config list -j` with it. The shorthand is registered on `config list` again; `--json` continues to work everywhere.
- The CLI now exits non-zero when it panics. A recovered panic was reported to Sentry and printed a message, but the process still exited 0, so CI jobs and scripts treated a crashed command as a success. The panic message now goes to stderr.

---

## [cli v4.8.2](versions/cli-v4.8.2.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2026-08-10**

### Fixed

- `db load` no longer fails with a shorthand collision error. Its `--jobs`/`-j` flag was clashing with the global `--json`/`-j` flag added in 4.7.0, breaking every `db load` invocation. `--json` no longer has a shorthand; `db load -j <n>` is unchanged.

---

## [cli v4.8.1](versions/cli-v4.8.1.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2026-08-07**

### Fixed

- `create database` now honors flags like `--engine` instead of re-prompting for them. Any flag you set explicitly (`--engine`, `--instance-class`, `--multi-az`, etc.) is used directly and its interactive prompt is skipped. `--engine` accepts the fully-qualified engine name (`mysql`, `postgres`, `aurora-mysql`, `aurora-postgresql`) and is validated so a typo fails fast.
- `create app`/`create pipeline` now respect the `--addon-database` and `--addon-redis` flags, which were previously accepted but ignored. Interactively they preselect the addon; non-interactively they auto-select when the cluster has a single database/redis instance, and otherwise list the choices (use `--addon-database-name`/`--addon-redis-name` to pick one).

---

## [cli v4.8.0](versions/cli-v4.8.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2026-07-24**

### Added

- `ps restart` command to restart your app's processes. By default it does a graceful, zero-downtime rolling restart (spins up replacement containers before stopping the old ones); add `--force` to immediately stop the running containers and let them relaunch.
- `version check` command to check if a newer CLI version is available.
- `version update` command to download and install the latest CLI version from GitHub releases.
- `shell --live`/`ps exec --live` now show each process's size (CPU/memory) in the selector, and print an advisory naming the process and its size after connecting.

### Fixed

- `ps resize` no longer fails on apps that have never had a successful release.
- `shell` now only uses a login shell (`bash -l`) for buildpack apps, avoiding cases where it clobbered a `PATH` set by a Dockerfile-based app's image.
- `selfupdate` now errors clearly when a downloaded binary exceeds the size limit, instead of silently truncating it to a confusing checksum mismatch.
- Commands other than `auth` no longer fail with a raw SDK error when the local `~/.aws` config has a partial/incomplete `default` profile.

---

## [ci-builder v2.7.0](versions/ci-builder-v2.7.0.md)

[ci-builder](tags.md#tag:ci-builder){ .md-tag .md-tag-icon .md-tag--ci-builder }

**2026-07-23**

### Added

- CodeBuild environment variables are now mapped to neutral, industry-standard CI
- variable names and made available to builds — as `--build-arg` values for Docker
- builds and as environment variables for buildpack builds:
- `CI_COMMIT_REF` — source ref (from `CODEBUILD_WEBHOOK_HEAD_REF`, falling back to
- `CODEBUILD_SOURCE_VERSION` for manual builds)
- `CI_COMMIT_SHA` — resolved commit SHA (from `CODEBUILD_RESOLVED_SOURCE_VERSION`)
- `CI_BUILD_STARTED_AT` — build start time (from `CODEBUILD_START_TIME`)
- `CI_REPOSITORY_URL` — repository clone URL (from `CODEBUILD_SOURCE_REPO_URL`)
- Each variable is only set when its source value is present, so Dockerfile `ARG`
- defaults are preserved on non-CodeBuild or manual runs.

---

## [ci-builder v2.6.0](versions/ci-builder-v2.6.0.md)

[ci-builder](tags.md#tag:ci-builder){ .md-tag .md-tag-icon .md-tag--ci-builder }

**2026-07-21**

### Changed

- Removed support for EOL `heroku-20` builds

### Fixed

- Builds that use an in-dyno test database or Redis add-on (`heroku-postgresql:in-dyno`,
- `heroku-redis:in-dyno`) could intermittently fail during the pre-build phase with an
- error like `The container name "/db" is already in use`. These add-on containers now
- start with unique names, so a build no longer collides with a leftover container from
- a previous run.

---

## [cli v4.7.0](versions/cli-v4.7.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2026-06-24**

### Added

- `--json` persistent flag for machine-readable CLI output.
- `modify app` command to update some parameters of application/pipeline stacks.
- `build start` command now accepts optional `--ref` flag to build from specific git references (branches, tags, or commit hashes).

### Changed

- `create app`/`create pipeline` now guide repository authentication through AWS Code Connections (GitHub App) instead of the deprecated CodeBuild OAuth flow.
- Migrated interactive prompts from survey to huh.
- Upgraded to AWS SDK for Go v2.
- Updated to Go 1.25.4, upgraded go-jose to v4, and refreshed dependencies.

### Fixed

- Fixed issue where a stack update could revert unexpected parameters to template defaults.
- `ps resize` no longer prints a misleading warning for release/scheduler processes.
- Fixed `destroy` retry exit code.
- Handle `LoadBalancerNotFound` during cluster deletion.
- Added DynamoDB attribute tags so the SDK v2 correctly unmarshals stack items.

---

## [stacks v5.17.3](versions/stacks-v5.17.3.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-11-04**

### Fixed

- Fixed errors during application tear down process

---

## [stacks v5.17.2](versions/stacks-v5.17.2.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-11-04**

### Fixed

- Fixed errors during application tear down process

---

## [stacks v5.17.1](versions/stacks-v5.17.1.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-11-04**

### Fixed

- Fixed errors during new account creation process

---

## [ci-builder v2.5.0](versions/ci-builder-v2.5.0.md)

[ci-builder](tags.md#tag:ci-builder){ .md-tag .md-tag-icon .md-tag--ci-builder }

**2025-10-21**

### Added

- Tear down review apps when a PULL_REQUEST_CLOSED event is received.

---

## [stacks v5.17.0](versions/stacks-v5.17.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-10-21**

### Added

- Automatically tear down review apps when a PR is closed. Previously, review apps were only removed when a PR was merged.

---

## [ci-builder v2.4.0](versions/ci-builder-v2.4.0.md)

[ci-builder](tags.md#tag:ci-builder){ .md-tag .md-tag-icon .md-tag--ci-builder }

**2025-09-22**

### Fixed

- Enable Codebuild to archive `apppack.toml` from non-standard locations

### Security

- Updated Go version and underlying dependencies

---

## [stacks v5.16.0](versions/stacks-v5.16.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-09-22**

### Added

- Clear app build cache directory every 60 days through a Cloudwatch event.

### Changed

- Consolidate duplicate empty_s3_bucket lambda implementations into single enhanced version

---

## [stacks v5.15.1](versions/stacks-v5.15.1.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-09-22**

### Fixed

- Avoid trying to replace existing load balancers when updating the stack.

---

## [ci-builder v2.3.0](versions/ci-builder-v2.3.0.md)

[ci-builder](tags.md#tag:ci-builder){ .md-tag .md-tag-icon .md-tag--ci-builder }

**2025-09-19**

### Added

- apppack.toml file is now accessible by APPPACK_TOML environment variable, allowing different services in different environments.

---

## [stacks v5.15.0](versions/stacks-v5.15.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-09-16**

### Changed

- Extend Athena query date range for load balancer logs from 60 days to full history (starting 2022/01/01)

### Fixed

- Update load balancer logs Athena query to include new `conn_trace_id` field
- Ensure all IAM policy statements include a proper `Sid` field
- Remove redundant port specifications in SecurityGroupEgress rules

---

## [cli v4.6.7](versions/cli-v4.6.7.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2025-08-14**

### Fixed

- Fix for a change in heroku/builder:24 causing HOME=/root resulting in various permissions errors.

---

## [ci-builder v2.2.0](versions/ci-builder-v2.2.0.md)

[ci-builder](tags.md#tag:ci-builder){ .md-tag .md-tag-icon .md-tag--ci-builder }

**2025-06-16**

### Changed

- Updated embedded version of `pack` for all but `heroku/buildpacks:20` builders

### Fixed

- `heroku/builder:24` can now be used as a builder

---

## [cli v4.6.6](versions/cli-v4.6.6.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2025-03-31**

### Fixed

- Handle and return a clear error for empty CloudFormation change sets instead of `ResourceNotReady` error.
- Raise an exception when no scheduled tasks are available for deletion.

---

## [cli v4.6.5](versions/cli-v4.6.5.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2025-03-06**

### Fixed

- Properly ignore errors on region deletion if the legacy `dockerhub-access-token` is not found.

---

## [cli v4.6.4](versions/cli-v4.6.4.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2025-03-05**

### Removed

- Region creation no longer requires Docker Hub credentials. Existing apps must be upgraded for compatibility.

### Fixed

- Resizing a non-existent service in an undeployed app no longer causes an error.
- Network issues are now displayed separately from authentication errors. Previously, network failures during authentication token refresh were incorrectly shown as authentication errors.

---

## [stacks v5.14.0](versions/stacks-v5.14.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2025-02-11**

---

## [ci-builder v2.1.0](versions/ci-builder-v2.1.0.md)

[ci-builder](tags.md#tag:ci-builder){ .md-tag .md-tag-icon .md-tag--ci-builder }

**2025-02-10**

### Fixed

- Release tasks work with latest metadata from Heroku Buildpacks

---

## [cli v4.6.3](versions/cli-v4.6.3.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2024-11-04**

### Fixed

- Excluded `limitless` suffix from Aurora PostgreSQL version selection to ensure compatibility with general-purpose instance types.
- Verify existence of review app before resizing process with `ps resize`.

---

## [stacks v5.13.0](versions/stacks-v5.13.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2024-10-14**

### Added

- Add `MultiAZEnabled` attribute to Redis cluster.

### Fixed

- Use `NumCacheClusters` for non-clustered Elasticache instance instead of `NumNodeGroups` & `ReplicasPerNodeGroup`

---

## [stacks v5.12.0](versions/stacks-v5.12.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2024-09-04**

### Fixed

- Give Codebuild role access to repo tokens stored in codeconnections.

---

## [cli v4.6.2](versions/cli-v4.6.2.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2024-09-03**

### Fixed

- Allow `apppack build` commands to work for non-pipeline apps.

---

## [stacks v5.11.0](versions/stacks-v5.11.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2024-09-03**

### Changed

- Increase timeout limit from 90 sec to 360 sec on DB manager lambda to allow for retries.

### Fixed

- Catch all Postgres errors for retrying DB Manger lambda operations.
- Ensure `IamAuthCustomResource` deletes prior to deletion of `Egress` in the security groups.

---

## [cli v4.6.1](versions/cli-v4.6.1.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2024-08-28**

### Fixed

- Revert the ability to provide `APPPACK_ACCOUNT` for multiple accounts.

---

## [cli v4.6.0](versions/cli-v4.6.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2024-08-28**

### Changed

- Limits the number of custom domains to 4.
- `ps resize` raises a warning for non-existent service.
- `reviewapps` cmd optionally accepts `-c`/ `account` flag.
- Implemented a check that throws an error if neither the `-c` flag nor the `APPPACK_ACCOUNT` environment variable is set and the user has multiple accounts. This ensures that users specify an account explicitly to avoid ambiguity.

### Fixed

- Prevent `Ctrl+C` from exiting the remote shell session prematurely.

---

## [stacks v5.10.0](versions/stacks-v5.10.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2024-08-27**

### Added

- Update legacy buckets to use new default ownership policy "bucket owner enforced"
- Allow Codebuild to fetch Codestar connections stored in Secrets Manager

---

## [cli v4.5.0](versions/cli-v4.5.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2024-05-16**

### Changed

- Integrates AWS Session manager directly.
- Updated dependencies.
- Improve error handling for user info API call.
- Improve error message when user needs admin access.

---

## [stacks v5.9.0](versions/stacks-v5.9.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2024-04-26**

### Added

- Added support for Redis 7.1 and made it default for all new clusters
- Additional outputs on stackApp: `TargetGroupArnSuffix`

### Changed

- Docker Hub credentials are no longer used or required when creating a region.
- Delete extraneous lambda for db resource ID in favor of native debresourceid.

### Fixed

- Allow Multi-AZ parameter to be toggled after Redis cluster creation.

---

## [stacks v5.8.0](versions/stacks-v5.8.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2024-04-24**

### Changed

- Update database manager Lambda to use Python 3.11

---

## [stacks v5.7.3](versions/stacks-v5.7.3.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2024-02-15**

### Added

- Additional outputs on stacks:
- App: `TaskRoleArn`, `TargetGroupArn`, and `TargetGroupSuffix`
- Database: `SecurityGroupId`

### Changed

- Removed ACL definition from utility buckets. ACLs are deprecated in favor of bucket policies.

---

## [stacks v5.7.2](versions/stacks-v5.7.2.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-10-13**

### Changed

- Remove restrictions on iam:GetRole for review apps to workaround Cloudformation issues

---

## [stacks v5.7.1](versions/stacks-v5.7.1.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-10-13**

### Fixed

- Removed tag condition from IAM role statement and ELBv2 target groups. Tags aren't applied atomically, so you can end up with resources that can't be udpated or destroyed because they didn't have a tag applied yet.

---

## [stacks v5.7.0](versions/stacks-v5.7.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-10-11**

### Changed

- Updated Lambdas from Python 3.7 to 3.11
- Increased timeout on database manager Lambdas to 90 seconds

---

## [stacks v5.6.0](versions/stacks-v5.6.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-09-12**

### Fixed

- Prevent review app deletion from removing all files from S3 bucket

---

## [stacks v5.5.2](versions/stacks-v5.5.2.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-09-08**

### Fixed

- Added additional IAM permission to handle undocumented AWS change

---

## [stacks v5.5.1](versions/stacks-v5.5.1.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-08-30**

### Changed

- Database Resource IDs now use native Cloudformation attributes instead of a custom resources

### Fixed

- Logic error around the creation of SQS config variable

---

## [stacks v5.5.0](versions/stacks-v5.5.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-07-21**

### Changed

- No longer explicitly creates ECS Service Linked Role. AWS now creates this role automatically.

---

## [stacks v5.4.0](versions/stacks-v5.4.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-05-03**

### Changed

- S3 buckets now set Ownership Controls to handle new AWS defaults

---

## [stacks v5.3.0](versions/stacks-v5.3.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-04-24**

### Changed

- Surface load balancer security group in cluster stack output

---

## [stacks v5.2.3](versions/stacks-v5.2.3.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-04-24**

### Fixed

- Updated instance type filter for RDS Performance Insights based on current instance classes

---

## [stacks v5.2.2](versions/stacks-v5.2.2.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-04-21**

### Fixed

- Scope ECS event delivery to the specific cluster

---

## [stacks v5.2.1](versions/stacks-v5.2.1.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-04-07**

### Fixed

- Make sure the ECS ServiceLinkedRole description matches the one created by AWS.

---

## [stacks v5.2.0](versions/stacks-v5.2.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-04-07**

### Changed

- Moved ECS ServiceLinkedRole creation from the cluster stack to the account stack. AWS made changes that prevent the role from being in multiple stacks.

---

## [cli v4.3.0](versions/cli-v4.3.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2023-03-27**

### Added

- CLI automatically checks for updates
- Report crashes to Sentry

### Changed

- `shell` command no longer requires `wc` in the remote container

### Fixed

- `upgrade region` now works as expected
- `create database` only shows valid instance sizes

---

## [stacks v5.1.0](versions/stacks-v5.1.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-03-27**

### Changed

- Use latest load balancer TLS Policy
- Updated Codebuild IAM Policy to allow it be used by external builds to start the Codebuild build

---

## [cli v4.4.0](versions/cli-v4.4.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2023-03-25**

### Changed

- Upgraded to Go 1.22 and updated dependencies

### Fixed

- Allow `ps` to work on clusters with large active task counts

---

## [stacks v5.0.0](versions/stacks-v5.0.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-03-21**

### Added

- Added an Athena Workgroup to the cluster stack which defines the results location and encryption configuration
- Update policies for changes at AWS
- Updated Cloudwatch log access policy with newly added permissions
- Explicity set the public access configuration on Public S3 buckets
- Explicity allow `ecs:TagResource` for AppPack and app users
- Added role for all cross-account event rules

### Changed

- Switched the build scripts from being delivered via the stack to being delivered via the build container
- Pipeline ECR repositories will now retain 200 images (instead of 50)

---

## [cli v4.2.0](versions/cli-v4.2.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2023-03-03**

### Added

- `shell` command now supports Dockerfile builds
- `ps resize` can now be run on a pipeline to apply to all review apps
- `create custom-domain` now supports wildcard domains
- `create redis` now lists available instance sizes

### Fixed

- `upgrade pipeline` works with latest changes to stack

---

## [stacks v4.4.0](versions/stacks-v4.4.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-03-03**

### Added

- Support wildcard custom domains

---

## [stacks v4.3.0](versions/stacks-v4.3.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-01-30**

### Added

- Added `SQSQueue` to app stack output

### Changed

- Allow `keys` and `info` commands for Redis users

---

## [cli v4.1.0](versions/cli-v4.1.0.md)

[cli](tags.md#tag:cli){ .md-tag .md-tag-icon .md-tag--cli }

**2023-01-10**

### Added

- Experimental `dash` command for viewing app metric graphs

### Changed

- Upgraded to Go 1.19 and updated dependencies

### Fixed

- Prevent using an invalid index when deleting scheduled tasks which led to panic

---

## [stacks v4.2.1](versions/stacks-v4.2.1.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-01-09**

### Fixed

- Prefetch pack images from mirror to avoid check during build

---

## [stacks v4.2.0](versions/stacks-v4.2.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2023-01-09**

### Added

- Requests to Docker Hub will now be proxied through AppPack's mirror to avoid rate limiting.
- Option to use embedded builder in app stack

---

## [stacks v4.1.3](versions/stacks-v4.1.3.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2022-11-18**

---

## [stacks v4.1.2](versions/stacks-v4.1.2.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2022-11-01**

### Fixed

- Permissions on review app public S3 buckets had a double `/` in the path, which  caused the prefix to be inaccessible without a double  `/`.

---

## [stacks v4.1.1](versions/stacks-v4.1.1.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2022-10-27**

### Fixed

- Show proper version in the stack output

---

## [stacks v4.1.0](versions/stacks-v4.1.0.md)

[stacks](tags.md#tag:stacks){ .md-tag .md-tag-icon .md-tag--stacks }

**2022-10-27**

### Added

- #### Account
- Added `glue:*` and `athena:*` permissions to the `admin` role.
- #### Cluster
- Glue database and table for querying load balancer logs

---

