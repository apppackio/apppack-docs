# Dockerfile builds

!!! warning
    Dockerfile builds are not yet generally available. If you'd like to try them out, please [contact us](https://apppack.io/suppport).

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
    RUN apt-get update && apt install -y --no-install-recommends procps
    ```
=== "Alpine"
    ```Dockerfile
    RUN apk add --no-cache bash
    ```
