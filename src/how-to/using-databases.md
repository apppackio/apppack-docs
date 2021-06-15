# Using Databases

Postgres and MySQL databases are available as an add-on and are backed by [AWS RDS](https://aws.amazon.com/rds/). Database instances are designed to be shared across multiple apps in a cluster, but a cluster may have multiple database instances. If you wish to isolate a single app to a single database instance, you can do that too.

## Creating a Database cluster

First you must setup the database in your AppPack Cluster. This can be done with [`apppack create database`](/command-line-reference/apppack_create_database/).

!!! example
    ```
    apppack create database my-database
    ```

If you'd like to use [AWS Aurora](https://aws.amazon.com/rds/aurora/), pass in the `--aurora` flag. This command requires manually configured AWS credentials.

## Enabling the Database add-on for your application

During app creation, you'll be asked if you'd like to enable the database add-on and if so, which database cluster to use. Only database instances within the app's AppPack cluster will be available as options.

Enabling the database add-on will create a dedicated database user within the database cluster and assign permissions to a specific database.

!!! warning
    Destroying the application will also destroy the application's database. Be sure to download a backup first!

### Config Variables

The following config variable will be provided to your application to connect:

* `DATABASE_URL` the credentials for connecting to the cluster
