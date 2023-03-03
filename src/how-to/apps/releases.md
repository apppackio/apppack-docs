# Running a release task

A release task is a command that must run once before a new version of your app is deployed. It's commonly used for:

* database schema migrations
* uploading static assets to S3
* clearing CDN or internal Redis caches

## Defining a release task

To define a release task, add the command to your `Procfile` under the key, `release`. For example, to apply database schema migrations for a Django application, you might add the following line:

```yaml
release: python manage.py migrate --noinput
```

Unlike other commands in your `Procfile`, the `release` command will not create a new always-running service. It is a special task that only runs once during the deployment process.

## Release task pipeline

```
Build → Test (optional) → Finalize → Release → Deploy
```

If the release task completes successfully, AppPack will update the `web` service and any others defined in your `Procfile`.

If the release task fails, the deployment pipeline will stop and no services will be updated.

## A Note on backwards compatibility

The previous version of your app will be running at the same time as your release task runs. To prevent downtime or unexpected errors, your release task should never break compatibility with the currently running version. The best practice for deploying breaking changes is to use a [two-phase deployment technique](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/).