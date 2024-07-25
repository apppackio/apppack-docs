# Config variables

Config variables are used to store secrets and pass environment-specific information to your applications running on AWS. They are managed via the CLI and passed into the application via environment variables.

## Setting a config variable

[`apppack config set`](/command-line-reference/apppack_config_set/) is used to set a config variable. For example, if you wanted to store a config variable named `SECRET_KEY` with the value `this-is-a-secret` for your app `my-app`, you would run:

!!! example
    ```
    apppack -a my-app config set SECRET_KEY=this-is-a-secret
    ```

This command will store the value as an encrypted string in the [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html). It will also gracefully restart your application to add the environment variable immediately.

!!! note
    The `APPPACK_APPNAME` configuration is already set for each app. If neither `AWS_REGION` nor `AWS_DEFAULT_REGION` are configured, they will be automatically set to the app's deployed region. If either one is set, the other will not be set automatically.

## Modifying a config variable

Use the same process as above for setting a variable.

## Removing a config variable

If you want to remove a config variable completely, you can run:

!!! example
    ```
    apppack -a my-app config unset SECRET_KEY
    ```

This would remove the config variable `SECRET_KEY` from the app named `my-app`.

## Listing config variables

You can list all the config variables for an app by running:

!!! example
    ```
    apppack -a my-app config list
    ```
