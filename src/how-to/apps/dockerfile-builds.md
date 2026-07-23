# Dockerfile builds

Dockerfile builds allow you to build your application using a Dockerfile instead of the default Buildpacks. This is useful if you have a complex build process, or if you are already using Docker locally and want better parity between environments.

## Requirements

### Configuration with `apppack.toml`

At a minimum, you need to define your build system and services in [`apppack.toml`](./apppack_toml.md). Here is an example of a simple `apppack.toml` file that uses Dockerfile builds and defines a single web service:

```toml
[build]
system = "dockerfile"

[services.web]
command = "npm start"
```

See the [apppack.toml reference](./apppack_toml.md) for more information.

### Installed packages

Your final container must include the following commands so AppPack can run tools like `shell`:

* `bash`
* `date`
* `sh`
* `sleep`
* `pgrep`
* `test`

These are typically included in the base image you are using, but if you are using a minimal image, you may need to install them. How you install them depends on your base image, but usually they will come as part of `bash`, `coreutils`, and `procps`. To test if your image has these commands, you can run the following command:

```bash
# replace $YOUR_IMAGE with the name of your image
docker run --rm -it $YOUR_IMAGE /bin/sh -c 'for c in bash date sleep pgrep test; do command -v $c || echo ✘ $c MISSING; done'
```

If you see any commands flagged as `MISSING`, you'll need to install them to take full advantage of AppPack.

Here are some examples of installing the necessary commands for some common minimal images:

=== "Debian Slim"
    ```Dockerfile
    RUN apt-get update && apt-get install -y --no-install-recommends procps
    ```
=== "Alpine"
    ```Dockerfile
    RUN apk add --no-cache bash
    ```

## Build-time CI variables

AppPack passes a set of neutral, industry-standard CI variables into your build. For Dockerfile builds they are provided as `--build-arg` values; for Buildpack builds they are available as environment variables during the build. The names mirror the conventions used by GitLab CI and other systems, so they are portable across build environments.

| Variable | Description |
| --- | --- |
| `CI_COMMIT_REF` | The source ref being built (branch or tag). Falls back to the ref the build pulled from for manual builds. |
| `CI_COMMIT_SHA` | The resolved commit SHA. |
| `CI_BUILD_STARTED_AT` | The time the build started. |
| `CI_REPOSITORY_URL` | The repository clone URL. |

Each variable is only set when a value is available, so a manual build or a non-CodeBuild environment will simply leave it unset.

To use a variable in a Dockerfile build, declare it with `ARG` before you reference it. Providing a default keeps local `docker build` runs working when the variable is absent:

```Dockerfile
ARG CI_COMMIT_SHA=unknown
ENV APP_VERSION=$CI_COMMIT_SHA
```
