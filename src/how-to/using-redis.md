# Using Redis

Redis is available as an add-on and is backed by [AWS Elasticache](https://aws.amazon.com/elasticache/). Redis instances are designed to be shared across multiple apps in a cluster, but a cluster may have multiple Redis instances. If you wish to isolate a single app to a single Redis instance, you can do that too.

## Creating a Redis cluster

First you must setup Redis in your AppPack Cluster. This can be done with [`apppack create redis`](/command-line-reference/apppack_create_redis/).

!!! example
    ```
    apppack create redis my-redis
    ```

<script id="asciicast-79qIkn14fXw0jCAPbKNHlBsrD" src="https://asciinema.org/a/79qIkn14fXw0jCAPbKNHlBsrD.js" data-rows="20" data-theme="monokai" async></script>

This command requires administrator access.

## Enabling the Redis add-on for your application

During app creation, you'll be asked if you'd like to enable the Redis add-on and if so, which Redis cluster to use. Only Redis instances within the app's AppPack cluster will be available as options.

Enabling the Redis add-on will create a dedicated Redis user within the Redis instance and assign permissions to a specific namespace within Redis.

!!! tip
    Destroying the application does not currently destroy any data in Redis. It is setup as a least recently used (LRU) cache, so unused keys will expire as needed. If data security or privacy is an issue, you should manually delete any keys that might be left over.

### Config Variables

The following config variables will be provided to your application to connect:

* `REDIS_URL` the credentials for connecting to the cluster
* `REDIS_PREFIX` the key prefix accessible to the app
