# Working with Review Apps

Review Apps are a concept pioneered by [Fourchette](https://github.com/rainforestapp/fourchette) and adopted officially by Heroku. They are a great way to quickly spin up temporary isolated app instances from a GitHub Pull Request.

## Overview

All Review Apps belong to a special class of application called a Pipeline. A Pipeline is associated with a single git repository, but unlike a standard application, it is not linked to a specific branch in that repository. The Pipeline does not run any of its own services, but sets up a number of resources (CodeBuild Project, Configuration, IAM Roles, etc.) that are shared with each of its associated Review Apps. 

Review apps are different from "standard" apps in AppPack in a few ways:

* They can be created/destroyed without administrator access (any AppPack user with access to the Pipeline can create/destroy its review apps)
* Add-ons are defined by the underlying Pipeline
* They do not support custom domains or auto-scaling
* They share a base configuration with the underlying Pipeline (but can also have their own custom configuration)

## Creation

A Review App can be created by running:

```
apppack reviewapps create <pipeline>:<pr_number>
```

If you had a Pipeline named `my-app-pipeline` and a Pull Request `#221` then you would run:

!!! example
    ```
    apppack reviewapps create my-app-pipeline:221
    ```

It should take ~30 seconds to create the AWS resources for the Review App. Then a build is triggered to create an image from the branch in the Pull Request. If the build (and optionally tests) are successful, that branch is then deployed the same as a standard application. Your app would then be accessible at `https://pr<pr_number>-<pipeline>.<cluster_domain>`.

## Using the CLI

Most AppPack commands you use for standard apps will also work with Review Apps. You can use the same `<pipeline>:<pr_number>` format to define the app name in the command. Given our example above, opening a shell would be:

!!! example
    ```
    apppack -a my-app-pipeline:221 shell
    ```

You can open your review app in the browser with:

!!! example
    ```
    apppack -a my-app-pipeline:221 open
    ```

## Add-Ons

Review Apps always setup the same set of add-ons defined on the parent Pipeline. If the Pipeline has a Postgres database and Redis Add-on defined, each Review App will get an isolated Postgres database and Redis namespace to work within. Similarly, the SQS and SES Add-ons work just like they do on a standard application.

S3 Buckets work slightly differently than a standard application. The Pipeline will create an S3 Bucket and Review Apps will each be assigned a prefix within the bucket they can access. Your code should be able to handle the presence of a `PUBLIC_S3_BUCKET_PREFIX` or `PRIVATE_S3_BUCKET_PREFIX` environment variable that defines the prefix all generated objects must use. For example, if your standard app expects to store a file at `s3://{PRIVATE_S3_BUCKET}/my_file.txt` the Review App would need to store it at `s3://{PRIVATE_S3_BUCKET}/{PRIVATE_S3_BUCKET_PREFIX}my_file.txt` (the prefix will contain a trailing slash, but not a preceeding one).

## Handling Initial Data

Quickly spinning up a Review App is great, but often our apps are useless without some initial data. For this, you can define a "post-deploy" task which can be used to populate data after the Review App is created. This is run just once on initial creation (after the Release task runs) and only for Review Apps. It is defined in your `app.json` file as `scripts.postdeploy`. Likewise, a `scripts.pre-destroy` script can be defined for any cleanup tasks that may be necessary. An `app.json` that defines a post-deploy task might look like this:

!!! example
    ```json
    {
      "scripts": {
        "postdeploy": "./bin/post_deploy.py"
      }
    }
    ```

!!! note
    Databases and S3 objects will be cleaned up as part of AppPack's destroy process.

## Deletion

Once you're done with a Review App, it can be deleted via:

```
apppack reviewapps destroy <pipeline>:<pr_number>
```
