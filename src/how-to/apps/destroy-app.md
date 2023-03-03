# Destroying an app

If you are no longer using an application, it should be destroyed to avoid paying for unused resources.

!!! danger
    Destroying an application destroys _everything_ related to the application. If you've configured add-ons which are storing data (database, Redis, S3, etc.), all data in those stores will be erased. Be sure to back up any data to a separate location before destroying the application.

When you're ready to destroy your application, you can use the [`apppack destroy app`](/command-line-reference/apppack_destroy_app/) command. Only administrators can perform this action.

!!! example
    ```
    apppack destroy app my-app
    ```
