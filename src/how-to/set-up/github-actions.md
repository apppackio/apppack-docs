# Using GitHub Actions with AppPack (Advanced)

AppPack will setup a full continuous integration pipeline for your app on AWS. This is the recommended approach, however in some scenarios an application may require more flexibility than what is built-in.

AppPack maintains a few GitHub Actions that can be used to let you build a custom application pipeline using [GitHub Actions](https://github.com/features/actions).

## Prerequisites

1. [Create an IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)
2. [Attach a prebuilt IAM Policy to the user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html). It will be named `apppack-app-{appname}-CodebuildPolicy-{random}`. For example, a policy for the app `my-app` might be named `apppack-app-my-app-CodebuildPolicy-RMSWNYR4ZW6W`.
3. [Create access keys for the user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
4. [Add those as encrypted secrets in your GitHub Repository](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`)

!!! tip
    In general, it is best practice _not_ to generate static access keys for your AWS environment, but when performing actions outside AWS in an automated environment, it is more-or-less unavoidable. Treat these as you would any other account password and consider rotating them periodically to reduce risk in the event of a leak.

## Available Actions

* [AppPack Metadata](https://github.com/marketplace/actions/apppack-metadata) `apppackio/metadata-action`
  Fetch AppPack build metadata
* [AppPack Build](https://github.com/marketplace/actions/apppack-build) `apppackio/build-action`
  Trigger an AppPack deploy
* [AppPack Upload Artifacts](https://github.com/marketplace/actions/apppack-upload-artifacts) `apppackio/upload-artifacts-action`
  Upload build artifacts to S3
* [AppPack Deploy](https://github.com/marketplace/actions/apppack-deploy) `apppackio/deploy-action`
  Trigger an AppPack deploy
  
## Using the Actions in a Workflow

Here is an example workflow which uses a custom test process with AppPack in GitHub Actions:

!!! example
    {% raw %}
    ```yaml
    name: apppack-build
    
    on: [push]
    
    jobs:
      pipeline:
        runs-on: ubuntu-20.04
        env:
          AWS_DEFAULT_REGION: us-east-1
        steps:
          - uses: actions/checkout@v2
          - name: Build
            id: build
            uses: apppackio/build-action@v1
            with:
              appname: my-app
            env:
              AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
              AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          - name: Test
            run: |
              set -euf -o pipefail
              docker run --rm \
                 --entrypoint /cnb/lifecycle/launcher \
                 ${{ steps.build.outputs.docker_image }} \
                 my-test-script | tee test.log
          - name: Upload Artifacts
            uses: apppackio/upload-artifacts-action@v1
            with:
              appname: my-app
            env:
              AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
              AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          - name: Deploy
            uses: apppackio/deploy-action@v1
            with:
              appname: my-app
            env:
              AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
              AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    ```
    {% endraw %}
