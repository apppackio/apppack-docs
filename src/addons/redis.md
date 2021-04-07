# Redis Add-on

## Prerequisites

Prior to creating an app with a Redis add-on, a Redis cluster must be setup in AppPack with [`apppack create redis`](/command-line-reference/apppack_create_database/). This creates a managed Elasticache cluster at AWS.

## Overview

Enabling the Redis add-on will create a dedicated Redis user within the Elasticache cluster and assign permissions to a specific namespace within Redis. The permissions are handled via the following [Redis ACL](https://redis.io/topics/acl):

```
on ~appname/* +@all -@admin -@dangerous
```

Destroying the application does not currently destroy any data in Redis. It is setup as a least recently used (LRU) cache, so unused keys will expire as needed. If data security or privacy is an issue, you should manually delete any keys that might be left over.

## Config Variables

* `REDIS_URL` the credentials for connecting to the cluster
* `REDIS_PREFIX` the key prefix accessible to the app
