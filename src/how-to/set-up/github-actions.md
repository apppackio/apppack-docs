# Using GitHub Actions with AppPack (Advanced)

AppPack comes with a full continuous integration pipeline for your app on AWS out-of-the-box. This is the recommended approach, however in some scenarios an application may require more flexibility than what is built-in.

AppPack maintains a GitHub Action that can be used to let you build a custom application pipeline using [GitHub Actions](https://github.com/features/actions).

## Prerequisites

It's possible to do this with an IAM user and access keys, but it's more secure to use OIDC. Here are the steps to set up an AWS Role for use with GitHub Actions:

1. [Add GitHub as an Identity Provider](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services#adding-the-identity-provider-to-aws) in your AWS account
2. Create a role in your AWS account here, [https://console.aws.amazon.com/iamv2/home#/roles/create](https://console.aws.amazon.com/iamv2/home?region=us-east-1#/roles/create)
    1. Select "Web Identity" as the entity type
    2. Select the Identity Provider and audience you created in step 1
    3. Click `Next`
    4. Select the Codebuild policy for your app. It will be named `apppack-app-{yourappname}-CodebuildPolicy-{randomstring}`
    5. Click `Next`
    6. Provide the role name and description
    7. Update the "Selected trusted entities" to limit the trust to the specific GitHub repository you want to use. For example, if your repository is `myorg/my-app-repo`, the trust policy should look like this:
        ```json
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": "sts:AssumeRoleWithWebIdentity",
              "Principal": {
                "Federated": "arn:aws:iam::135549385118:oidc-provider/token.actions.githubusercontent.com"
              },
              "Condition": {
                "StringEquals": {
                  "token.actions.githubusercontent.com:aud": [
                    "sts.amazonaws.com"
                  ]
                },
                "StringLike": {
                  "token.actions.githubusercontent.com:sub": "repo:myorg/my-app-repo:*"
                }
              }
            }
          ]
        }
        ```
      8. Click `Create role`
3. Use the `--disable-build-webhook` flag when [creating the app](https://docs.apppack.io/command-line-reference/apppack_create_app/) to make sure the default AppPack build pipeline is disabled.

## Available Actions

* [AppPack Deploy](https://github.com/marketplace/actions/apppack-deploy) `apppackio/deploy-action`
  Uploads an image and metadata, then triggers an AppPack deploy
* [Setup AppPack CLI](https://github.com/apppackio/setup-apppack-cli) `apppackio/setup-apppack-cli`
  Installs the latest version of the AppPack CLI
  
## Using the Actions in a Workflow

Here is an example workflow which deploys an AppPack app in GitHub Actions. _Note: your repo will need to include an `apppack.toml` file to describe your app's services._

!!! example
    {% raw %}
    ```yaml
    ---
    name: AppPack Deploy
    on: [push]
    
    jobs:
    build:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    env:
      # replace this with your AppPack app name
      APPNAME: your-app-image
      BUILDX_CACHE_DIR: /tmp/.buildx-cache
      # replace these with the AWS role you create and the region your app is in
      AWS_ROLE_ARN: arn:aws:iam::123456789012:role/github-actions
      AWS_REGION: us-east-2
    steps:
      - uses: actions/checkout@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      - uses: actions/cache@v3
        with:
          path: ${{ env.BUILDX_CACHE_DIR }}
          key: ${{ runner.os }}-buildx-${{ github.ref }}-${{ github.sha }}
          restore-keys: |
              ${{ runner.os }}-buildx-${{ github.ref }}-
              ${{ runner.os }}-buildx-
      - name: Build Docker Image
        shell: bash  # adds pipefail
        run: |
          docker buildx build \
            --tag $APPNAME:${{ github.run_id }} \
            --progress plain \
            --cache-to type=local,dest=${{ env.BUILDX_CACHE_DIR }} \
            --cache-from type=local,src=${{ env.BUILDX_CACHE_DIR }} \
            --file Dockerfile \
            --load \
            . 2>&1 | tee /tmp/build.log  # avoid part of build.log ending up in the image
          mv /tmp/build.log .
      - name: Test
        shell: bash  # adds pipefail
        run: |
          # replace this with your own test command
          docker run --rm -e SECRET_KEY=1 $APPNAME:${{ github.run_id }} pytest | tee test.log
      - uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: ${{ env.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
      - uses: apppackio/deploy-action@v2
        with:
          appname: ${{ env.APPNAME }}
          image: ${{ env.APPNAME }}:${{ github.run_id }}
    ```
    {% endraw %}
