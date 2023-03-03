# Install the Command Line Interface (CLI)

The latest version of `apppack` is `{{ apppack_version() }}` and is available on the [GitHub Release page](https://github.com/apppackio/apppack/releases/tag/v{{ apppack_version() }}).

## Homebrew

If you're a homebrew user, you can install the latest version via:

```bash
brew tap apppackio/apppack
brew install apppack
```

## Manual installation

1. Visit the [GitHub Release page](https://github.com/apppackio/apppack/releases/tag/v{{ apppack_version() }})
2. Download the correct archive for your platform and unpack it
3. Make the binary executable (`chmod +x apppack` on MacOS or Linux)
4. Save it somewhere on your `$PATH`, e.g. `/usr/local/bin`

!!! warning
    The MacOS binary is not currently signed. You'll get an error that it cannot be verified when you open it. To work around this, right-click the file and select "Open", then click "Open" in the dialog box. Alternatively, you can run `sudo xattr -rd com.apple.quarantine path/to/apppack` to bypass the verification.


## Authentication

Once you've installed the CLI, authenticate with AppPack via:

```
apppack auth login
```
