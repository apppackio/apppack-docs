# Using databases

Postgres and MySQL databases are available as an add-on and are backed by [AWS RDS](https://aws.amazon.com/rds/). Database instances are designed to be shared across multiple apps in a cluster, but a cluster may have multiple database instances. If you wish to isolate a single app to a single database instance, you can do that too.

## Creating a database cluster

First you must setup the database in your AppPack Cluster. This can be done with [`apppack create database`](/command-line-reference/apppack_create_database.md).

!!! example
    ```
    apppack create database my-database
    ```

<script id="asciicast-uMdIlLyyuvsiNubMF23LZRW1M" src="https://asciinema.org/a/uMdIlLyyuvsiNubMF23LZRW1M.js" data-rows="20" data-theme="monokai" async></script>

This command requires administrator access.

## Enabling the database add-on for your application

During app creation, you'll be asked if you'd like to enable the database add-on and if so, which database cluster to use. Only database instances within the app's AppPack cluster will be available as options.

Enabling the database add-on will create a dedicated database user within the database cluster and assign permissions to a specific database.

!!! warning
    Destroying the application will also destroy the application's database. Be sure to download a backup first!

### Config variables

The following config variable will be provided to your application to connect:

* `DATABASE_URL` the credentials for connecting to the cluster
