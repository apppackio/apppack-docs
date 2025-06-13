# apppack.toml

This file can be used to configure how your app is built, released, and the services it will run when deployed.

## TOML Syntax

TOML is a human-readable configuration format. It's similar to JSON or YAML, but with a different syntax. You can find a full reference of the syntax at [toml.io](https://toml.io).

You must store this file in the root of your repository and name it `apppack.toml` or set the environment variable `APPPACK_TOML` to be the filename for your environment. If it exists, [configuration via `app.json`](./apps.md#appjson) will be ignored.

## `[build]`

### `system`

The tooling used to build your app.

* Type: `string`
* Values: `dockerfile` or `buildpack`
* Default: `buildpack`
* Required: No

### `buildpacks`

The buildpacks used to build your app. Only used if `system` is set to `buildpack`.

* Type: `array` of `string`
* Values: A list of buildpacks, e.g. `["heroku/nodejs", "heroku/python"]`
* Default: `[]` (use auto-detection)
* Required: No

### `builder`

The buildpack builder used to build your app. Only used if `system` is set to `buildpack`.

* Type: `string`
* Values: A buildpack builder, e.g. `"heroku/builder-cnb:22"`. The aliases `heroku-20` (for `heroku/buildpacks:20`) and `heroku-22` (for `heroku/builder-classic:22`) are also supported.
* Default: `"heroku-20"`
* Required: No

### `dockerfile`

The path to the Dockerfile used to build your app. Only used if `system` is set to `dockerfile`.

* Type: `string`
* Values: A path to a Dockerfile, e.g. `"Dockerfile"`
* Default: `"Dockerfile"`
* Required: No

## `[test]`

### `command`

The command used to run your tests.

* Type: `string`
* Values: A command, e.g. `"npm test"`
* Default: `""`
* Required: No

### `env`

Environment variables to be used when building and testing your app.

* Type: `array` of `string`
* Values: A list of environment variables, e.g. `["FOO=bar", "BAZ=qux"]`
* Default: `[]`
* Required: No

## `[deploy]`

### `release_command`

The command used to release your app. Only used if `build.system` is set to `dockerfile`. Buildpack apps will use the `release` key in their `Procfile`.

* Type: `string`
* Values: A command, e.g. `"python manage.py migrate --noinput"`
* Default: `""`
* Required: No

## `[review_app]`

This section is only applicable for review apps. See [Review Apps](/how-to/apps/review-apps#handling-initial-data) for more information.

### `initialize_command`

The command used to perform a one-time initialize a review app. This is the equivalent of `postdeploy` on Heroku.

* Type: `string`
* Values: A command, e.g. `"python manage.py load_initial_data"`
* Default: `""`
* Required: No

### `pre_destroy_command`

The command used to perform a one-time cleanup before destroying a review app. This is the equivalent of `pr-predestroy` on Heroku.

* Type: `string`
* Values: A command, e.g. `"python manage.py teardown_review_app"`
* Default: `""`
* Required: No

## `[services.<name>]`

Only applicable if `build.system` is set to `dockerfile`. For buildpacks, the `Procfile` is used instead.
Each table defines a service your app will run.

* Type: `table`
* Values: Must have a `command` key
* Default: `{}`
* Required: `[services.web]` is required if `build.system` is set to `dockerfile`

### `command`

The command used to run the service.

* Type: `string`
* Values: A command, e.g. `"npm start"`
* Default: `""`
* Required: Yes


