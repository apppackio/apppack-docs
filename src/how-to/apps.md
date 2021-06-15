# Prepping Your App

AppPack apps are built using Heroku's open source [Cloud Native Buildpacks](https://buildpacks.io/) and are largely compatible with apps built for the Heroku platform.

## Buildpacks

At the core of AppPack are buildpacks. Buildpacks are used to create container images from your code without the need to maintain a `Dockerfile`. [Heroku's official buildpacks](https://devcenter.heroku.com/articles/buildpacks#officially-supported-buildpacks) support most popular languages. If you need something that isn't supported by an official buildpack, it's likely there is [a third-party buildpack](https://elements.heroku.com/buildpacks) which does.

!!! warning
    Heroku's official buildpacks are all compatible with Cloud Native Buildpacks. Third-party buildpacks however must be "shimmed" for compatibilty. This can be done by specifying the URL as `https://cnb-shim.herokuapp.com/v1/<namespace>/<name>`. See [this blog post](https://jkutner.github.io/2020/05/26/cloud-native-buildpacks-shim.html) for more details.

Multiple buildpacks can be used for more complex environments. For example, if you wanted to deploy a Python web service which required Node.js to compile files for the frontend, you can use both `heroku/nodejs` and `heroku/python`.

## `Procfile`

Every app must have a file named `Procfile` in the root of the repository. It is a yaml formatted file which defines the services that make up your application. An example `Procfile` might look like this:

!!! example
    ```yaml
    web: gunicorn --bind=0.0.0.0:$PORT myapp:application
    worker: celery --app myapp.celery.app worker
    ```

This would create two services during deployment:

1. The `web` service which will execute the command `gunicorn --bind=0.0.0.0:$PORT myapp:application`
2. The `worker` service which will execute the command `celery --app myapp.celery.app worker`

Each service must have a unique name and will run as an independent container in AWS. Services can be scaled independently of each other.

The `web` service is required and is special in that it will be connect to the load balancer to serve HTTP traffic. The `PORT` environment variable will be provided to tell the container what port it should listen on.

## `app.json`

AppPack provides some compatibility with [Heroku's `app.json`](https://devcenter.heroku.com/articles/app-json-schema) file. It can be used to define specific Buildpack's to run and test environment details among other things. The following keys are supported:

* [`buildpacks`](https://devcenter.heroku.com/articles/app-json-schema#buildpacks)
* [`environments.test`](https://devcenter.heroku.com/articles/app-json-schema#environments)
* [`scripts`](https://devcenter.heroku.com/articles/app-json-schema#scripts)
* [`stack`](https://devcenter.heroku.com/articles/app-json-schema#stack)

## Config/Environment Variables

Any configuration you store for your app will be available as an environment variable when your application runs on AWS. Use them to store secrets or environment-specific information for your application. [Read more about config variables here](./config-variables.md).

## Add-ons (database, Redis, S3, etc.)

During app creation you'll be prompted to setup any backing services for your app. The connection details for each one will be added to the app's config during creation.

## Example

See [apppackio/apppack-demo-python](https://github.com/apppackio/apppack-demo-python) for a simple example of an AppPack-ready app.
