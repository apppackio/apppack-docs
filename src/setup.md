# Account Setup

## Prerequisites

1. **The `apppack` CLI** (see [install](install.md))
2. **An AWS account with [Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)** for an admin user or role.
3. **A [Ruote53 Hosted Zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html) setup in your AWS account** for a domain you'll use to route traffic to your applications. This can either be a top-level domain like `example.com` or a subdomain like `apppack.example.com`. If wish to use a subdomain and the top-level domain is hosted elsewhere, see [these instructions](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html). Make note of the Hosted Zone ID as you'll need it below.
4. **A free Docker Hub account and access token** (generated at [https://hub.docker.com/settings/security](https://hub.docker.com/settings/security)).
5. _[Optional]_ Add our [GitHub Application](https://github.com/apps/apppack-io) to your repo or organization to integrate deployment information.

## Setting up AWS

All commands in the setup process require AWS credentials, either via [environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) or a [credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html). Once an administrator has setup the resources, direct AWS credentials are no longer necessary to manage applications. AppPack handles user authentication while maintaining the use of AWS Identity Access Management (IAM) for authorization.

The `create` commands below all accept a `--check` flag which will allow you to audit the resources that will be created prior to making any changes in your AWS account.


### Creating the Account

Account creation will setup some top-level resources and output role information necessary to complete the AppPack account setup.

```bash
apppack create account --dockerhub-username <your_doockerhub_username>
```

Once complete, follow the instructions to activate your AppPack account.

### Creating a Cluster

Every app is deployed to a cluster. A cluster may contain multiple apps. The cluster consists of a load balancer, security groups, compute resources, etc.

```
apppack create cluster --domain <domain> --hosted-zone-id <hosted-zone-id>
```

The domain will serve as the parent domain for all apps in that cluster. If you use `cluster.example.com` as your domain, an app named `my-app` will be accessible at `my-app.cluster.example.com` in addition to any custom domains you setup for the app. The hosted zone ID comes from AWS Route 53 and is an alphanumeric string starting with `Z`.

## Creating your first App

AppPack apps are largely compatible with apps built for the Heroku platform. Leveraging a [`Procfile`](https://devcenter.heroku.com/articles/procfile) to define services and [`app.yml`](https://devcenter.heroku.com/articles/app-json-schema)[^1] to define buildpacks, test scripts, etc. See [lincolnloop/apppack-demo-python](https://github.com/lincolnloop/apppack-demo-python) for a simple example.

Once your app is ready, run:

```bash
apppack create app
```

If this is your first app, you'll be prompted to authorize Codebuild to pull from your repository and trigger new builds.

On completion, either push a new commit to the specified trigger branch or run `apppack -a <your-app> build start --wait` to trigger a build and wait for the deployment to complete.


[^1]: The [`buildpacks`](https://devcenter.heroku.com/articles/app-json-schema#buildpacks), [`stack`](https://devcenter.heroku.com/articles/app-json-schema#stack) and [`environments[test]`](https://devcenter.heroku.com/articles/app-json-schema#environments) portions of `app.json` are currently supported.
