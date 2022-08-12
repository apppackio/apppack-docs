# Deploying a Django app

If your app has a `requirements.txt` or `Pipfile` in the root directory, it will be identified as a Python app automatically. If you prefer to explicity define the buildpack you want to use, make sure your `app.json` file looks something like this:

```json
{
  "buildpacks": [{"url": "heroku/python"}]
}
```

If the settings file you want to use is not already the default for your `manage.py` and `wsgi.py`, add a config var to specify it:

```shell
apppack -a myapp config set DJANGO_SETTINGS_MODULE=myapp.settings  # replace with dotted path to your settings module
```

## Define your web service

Your `web` service should listen on the port defined in the environment variable `$PORT`. Any Python web server will work, but we'll use `gunicorn` for this example.

1. Make sure `gunicorn` is included in your requirements.
2. Define the `web` service in your `Procfile` (replace the last argument with the import path to your projects `wsgi.py`):
    ```yaml
    web: gunicorn --access-logfile=- --bind=0.0.0.0:$PORT --forwarded-allow-ips='*' myproject.wsgi:application
    ```

!!! tip
   For some applications, [the `gevent` worker class](https://docs.gunicorn.org/en/stable/settings.html?highlight=gevent#worker-class) may provide better performance for concurrent request processing. When using it, be sure to limit [the worker connections](https://docs.gunicorn.org/en/stable/settings.html?highlight=gevent#worker-connections) to a reasonable number to avoid overwhelming your database.

## Add a healthcheck endpoint

The load balancer will poll your application to make sure it is alive/healthy. It will make periodic requests to the healthcheck URL you defined when setting up the AppPack app. If it does not get a `200` status code response from that URL, it will mark the task as unhealthy and kill it. While you might be able to point it to `/`, it's recommended you use a dedicated endpoint instead. Potential issues include:

* sites that redirect all requests to a login page
* sites that redirect all HTTP requests to HTTPS
* the load balancer makes requests directly to the IP which can result in a `400` status code for sites with a restrictive `ALLOWED_HOSTS` setting
* creating unnecessary load by repeatedly generating dynamic content for the page

[`django-alive`](https://pypi.org/project/django-alive/) is an easy way to setup a dedicated healthcheck endpoint. You can follow the docs in the `README`, but the quick setup instructions are:

1. Make sure `django-alive` is included in your requirements.
2. Add `path("-/", include("django_alive.urls"))` to your `urls.py`.
3. Add this at the beginning of your `MIDDLEWARE` list: `"django_alive.middleware.healthcheck_bypass_host_check",`
4. Add `SECURE_REDIRECT_EXEMPT = [r"^-/"]` to your settings if you have `SECURE_SSL_REDIRECT = True`.

## Configuring environment-specific settings

AppPack follows the standard [12 Factor standard for configuration](https://12factor.net/config). Settings like `SECRET_KEY` should be set via configuration variables and read from the environment by the application. After creating your application, add them via the CLI:

```
apppack -a my-app config set SECRET_KEY=your-long-random-string
```

In your settings, you can read them from the environment:

```python
import os

SECRET_KEY = os.environ["SECRET_KEY"]

ANOTHER_SETTING = os.environ.get("ANOTHER_SETTING", "default-value-for-another-setting")
```

For more advanced environment variable tooling, check out [`goodconf`](https://pypi.org/project/goodconf/) or [`django-environ`](https://pypi.org/project/django-environ/).

## Optional Configuration

### Connecting to a database

If you're using the AppPack [database add-on](using-databases.md), you will have a `DATABASE_URL` environment variable available to the app that can be converted in your settings with [`dj-database-url`](https://pypi.org/project/dj-database-url/). First, add `dj-database-url` to your requirements and then add the following lines to your settings:

```python
import dj_database_url

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}
```

### Collectstatic

By default, the Heroku buildpack will attempt to run `collectstatic` at the end of the build process. This should collect the files to the local file system where they will be a part of the final image. The easiest way to serve them is directly from your app server with [`whitenoise`](https://pypi.org/project/whitenoise/). For detailed instructions, [see their docs](http://whitenoise.evans.io/en/stable/django.html).

!!! warning
   The build happens in an isolated environment without access to backing resources like your database or Redis. If your application tries to access the database during initialization, the `collectstatic` command will fail. Make sure any calls to backing resources happen inside function calls, not when the files are imported.

#### Node.js

If you need to build static files using Node.js before running `collectstatic`, you'll want to add the [`heroku/nodejs` buildpack](https://devcenter.heroku.com/articles/nodejs-support) to your list of buildpacks. In your [`app.json`](apps.md#appjson) file, make sure you have something like this:

```json
{
  "buildpacks": [{"url": "heroku/nodejs"}, {"url": "heroku/python"}]
}
```

Make sure your `package.json` and `package-lock.json` are in the root of your repo and you've defined a [build script](https://devcenter.heroku.com/articles/nodejs-support#customizing-the-build-process) which will be responsible for assembling the production-ready assets.

### Connecting to Redis

If you're using the AppPack [Redis add-on](using-redis.md), you will have `REDIS_URL` and `REDIS_PREFIX` environment variables available to the app. AppPack uses both a username _and_ password to connect to Redis. Some older redis libraries do not support this functionality. As of Django 4.0, [a Redis cache is included with Django](https://docs.djangoproject.com/en/4.0/topics/cache/). Just make sure `redis` is in your requirements and add this to your settings:

```python
# built-in redis cache with Django >= 4.0
import os

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"),
        "KEY_PREFIX": os.environ.get("REDIS_PREFIX", ""),
    }
}
```

For versions before 4.0, you can add the `django-redis` package to your requirements and use the following settings:

```python
# django-redis cache before Django 4.0
import os

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379") + "/0",
        "KEY_PREFIX": os.environ.get("REDIS_PREFIX", ""),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
}
```

### File storage

The local filesystem for the application is _ephemeral_. Any files that need to be accessible across versions or services should be stored in S3. An [S3 add-on](using-s3.md) is available for both publicly accessible files and private files. Add the [`django-s3-storage`](https://github.com/etianen/django-s3-storage) package to your requirements and use the following settings:

```python
import os

# Replace 'PRIVATE' with 'PUBLIC' for the public S3 add-on
if "PRIVATE_S3_BUCKET_NAME" in os.environ:
    DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"
    AWS_S3_BUCKET_NAME = os.environ["PRIVATE_S3_BUCKET_NAME"]
    AWS_S3_KEY_PREFIX = os.environ.get("PRIVATE_S3_BUCKET_PREFIX", "")
    # AWS_S3_BUCKET_AUTH = False  # Default to public files when using a public bucket
```

It is important that you only use the [Django file storage API](https://docs.djangoproject.com/en/dev/ref/files/storage/) in your application. It closely mirrors the Python API, but will seamlessly switch to using S3 when using the settings above.

### Outbound email

You can send email using any email provider, but [AppPack has an SES add-on](sending-email.md) available which integrates with AWS' service and has a generous free tier. To send mail with the SES add-on, add [`django-ses`](https://pypi.org/project/django-ses/) to your requirements and add the following settings:

```python
EMAIL_BACKEND = "django_ses.SESBackend"
DEFAULT_FROM_EMAIL = "noreply@example.com"  # Replace with a domain you've enabled in SES
SERVER_EMAIL = DEFAULT_FROM_EMAIL
AWS_SES_AUTO_THROTTLE = 0
AWS_SES_REGION_NAME = "us-west-2"  # Replace with the region your app is deployed to
AWS_SES_REGION_ENDPOINT = f"email.{AWS_SES_REGION_NAME}.amazonaws.com"
```

### Background tasks

Any background task manager will work on AppPack. For smaller sites, we recommend one that uses the database as its queue such as [Django Q](https://django-q.readthedocs.io/en/latest/index.html). This reduces the need for additional services which add complexity and cost. If you prefer to use Redis as your queue, make sure username and password authentication is supported and that you can define a key prefix for the queue. See [Connecting to Redis](#connecting-to-redis) for more details.

To run your background worker as a service, add it to the `Procfile` with something like this:

```yaml
worker: python manage.py qcluster  # replace with command to start the worker
```

If you're using the [SQS Add-on](using-sqs.md), you can use [`celery`](https://pypi.org/project/celery/) by adding `celery[sqs]` to your requirements. In your settings, you can use the following snippet to define the broker:

```python
import os

QUEUE_URL = os.environ.get("QUEUE_URL", "")
if QUEUE_URL.startswith("sqs://"):
    CELERY_TASK_DEFAULT_QUEUE = QUEUE_URL.split("/")[-1]
    CELERY_BROKER_URL = "sqs://"
```