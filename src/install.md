# Install the Command Line Interface (CLI)

The latest version of `apppack` is `{{ apppack_version() }}` and is available on the [GitHub Release page](https://github.com/apppackio/apppack/releases/tag/v{{ apppack_version() }}). Download the correct file for your platform, save it to your path, and make sure it is executable (`chmod +x apppack`).

## Homebrew

If you're a homebrew user, you can install the latest version via:

```bash
brew tap apppackio/apppack
brew install apppack
```

## Authentication

Once you've installed the CLI, authenticate with AppPack via:

```
apppack auth login
```
