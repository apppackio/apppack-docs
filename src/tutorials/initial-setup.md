# Initial Setup

This tutorial will walk you through the initial AppPack setup in your AWS account. You will connect your AWS account to AppPack and setup your initial cluster for installing apps.

## 📝 Prerequisites

You'll need a few things ready to go to complete this tutorial. Make sure you've taken the following steps before getting started.

1. Installed **the `apppack` CLI** (see _[Install the CLI](../how-to/install.md)_)
2. Setup **an AWS account with [Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)** for an admin user or role.
3. Created **a [Route53 Hosted Zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html) setup in your AWS account** for a domain you'll use to route traffic to your applications. This can either be a top-level domain like `example.com` or a subdomain like `apppack.example.com`. If you wish to use a subdomain and the top-level domain is hosted elsewhere, see [these instructions](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html). If your using a registrar other than Route53, make sure your nameservers are setup for the Hosted Zone there.
4. Setup **a free Docker Hub account and access token** (generated at [https://hub.docker.com/settings/security](https://hub.docker.com/settings/security)). This is required to avoid the [anonymous IP rate limits](https://docs.docker.com/docker-hub/download-rate-limit/) for pulling base images.

## 🔐 Using AWS Credentials

The first steps of setting up your account require AWS credentials. If you don't already have a way of managing AWS credentials locally (e.g. [`aws-vault`](https://github.com/99designs/aws-vault) or a [shared credentials file](https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html#shared-credentials-file)), you can temporarily add them to your shell using environment variables with the following commands (replacing the values with your own credentials:

=== "MacOS/Linux"
    ```shell
    $ export AWS_ACCESS_KEY_ID=YOUR_AKID
    $ export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
    ```

=== "Windows"
    ```
    > set AWS_ACCESS_KEY_ID=YOUR_AKID
    > set AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
    ```

!!! note
    AWS credentials are only needed to create and destroy applications and other high-level resources at AWS. Once you create your application(s), AppPack will manage temporary AWS credentials scoped to the individual application. You can think of your AWS credentials like superuser/administrator functionality for your account.

## 👷 Setting up AWS Resources

The first command you run with the AppPack CLI will create everything necessary (account, region, and cluster-level resources) to start deploying apps to your AWS account.

!!! note
    We'll be using the `us-east-1` region in this tutorial. If you prefer a different region, you can change this or use the `AWS_REGION` environment variable. See [How to Choose an AWS Region](../how-to/choose-aws-region.md) for more details.

From your command line run:

```shell
apppack --region us-east-1 init
```

!!! tip
    If you see a `NoCredentialProviders` error, it means your AWS credentials are not setup properly. Revisit [Using AWS Credentials](#using-aws-credentials) to verify they are setup.

You'll be prompted for a few additional bits of information that were part of the prerequisites.

1. Your Docker Hub username and access token.
2. The domain in your Route53 Hosted Zone that will serve as the parent domain for your applications. Read more about [how domains are handled in AppPack here](../under-the-hood/domains.md).

This command should take about 6 minutes to complete. The output should contain some progress information as it completes the different steps. On completion, you should see:

```
✔ AppPack initialization complete
```

!!! pricing
    Some resources created during this process may incur monthly AWS charges. Read [Under the Hood: Pricing](../under-the-hood/pricing.md) for more information.

## ✅ Account Approval

During our private beta period, new AppPack accounts require manual approval. In the output from the `init` command, you should see:

> Send the following information to support@apppack.io for account approval:  
> ExternalId: ...  
> AppPackRoleArn: ...

Send that info to us via email (it does not contain any sensitive information) and wait for confirmation that your account has been approved.

!!! warning
    **Don't start creating apps until you've received confirmation that your account is ready.**

## 🏁 Next Step

Congrats! Now that your account has been approved, you're ready to deploying apps. Continue on to the [Deploy Your First App](../tutorials/deploy-first-app.md) tutorial
