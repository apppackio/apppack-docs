# Database Add-on

## Prerequisites

Prior to creating an app with a database add-on, a database must be setup in AppPack with [`apppack create database`](/command-line-reference/apppack_create_database/). This creates a managed RDS database cluster/instance at AWS. Both Postgres and MySQL are supported in Aurora or the standard variants.

## Overview

Enabling the database add-on will create a dedicated database and user within the RDS cluster/instance for the app.

Destroying the application will also destroy the database associated with it.

## Config Variables

* `DATABASE_URL` the credentials for connecting to the cluster
