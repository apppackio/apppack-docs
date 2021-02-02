# Initial Setup

## Prerequisites

1. **The `apppack` CLI** (see [install](install.md))
2. **An AWS account with [Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)** for an admin user or role.
3. **A [Ruote53 Hosted Zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html) setup in your AWS account** for a domain you'll use to route traffic to your applications. This can either be a top-level domain like `example.com` or a subdomain like `apppack.example.com`. If wish to use a subdomain and the top-level domain is hosted elsewhere, see [these instructions](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html). If your using a registrar other than Route53, make sure your nameservers are setup for the Hosted Zone there.
4. **A free Docker Hub account and access token** (generated at [https://hub.docker.com/settings/security](https://hub.docker.com/settings/security)). This is required to avoid the [anonymous IP rate limits](https://docs.docker.com/docker-hub/download-rate-limit/) for pulling base images.
5. _[Optional]_ Add our [GitHub Application](https://github.com/apps/apppack-io) to your repo or organization to integrate deployment information.

## Setting up AWS

All commands in the setup process require AWS credentials, either via [environment variables](https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html#environment-variables) or a [credentials file](https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html#shared-credentials-file).

!!! tip
    Be sure to specify the AWS region you want to deploy to. You can do this via `--region` flag or by using the `AWS_REGION` environment variable. For example, `AWS_REGION=us-east-1 apppack create ...` or `apppack create --region us-east-1 ...`. AppPack currently supports the following AWS regions: `us-east-1`, `us-east-2`, `us-west-1`, `us-west-2`.

Once an administrator sets up these initial resources, direct AWS credentials are no longer necessary to manage applications. AppPack handles user authentication while maintaining the use of AWS Identity Access Management (IAM) for authorization.

The `create` and `init` commands below all accept a `--check` flag which will allow you to audit the resources that will be created prior to making any changes in your AWS account.

!!! pricing
    You will incur AWS charges for some resources used by AppPack. We'll make a note of what to expect where applicable.
    
    Some resources are such as [EventBridge Events](https://aws.amazon.com/eventbridge/pricing/), [SSM Parameters](https://aws.amazon.com/systems-manager/pricing/#Parameter_Store), and [Lambda Functions](https://aws.amazon.com/lambda/pricing/) are priced so low (fractions of a cent/month) or have such generous free tiers that they are not included in the notes.

    To track the cost of your AppPack resources, we recommend setting up [User-Defined Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html). All AppPack resources will get an `apppack:*` tag you can use for fine-grained tracking.
    
    Also don't forget about the [Free Tier](https://aws.amazon.com/free/), [Reserved](https://aws.amazon.com/rds/reserved-instances/) [Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/), [Savings Plans](https://aws.amazon.com/savingsplans/pricing/) and [AWS Activate Startup Credits](https://aws.amazon.com/activate/)!


### `apppack init`

`apppack init` is the first thing you should run. It will create all the resources at AWS necessary to start deploying apps. The `init` command steps your through each of the following:

1. `apppack create account`
2. `apppack create region`
3. `apppack create cluster`

#### Account Creation

Account creation will set up the global resources for AppPack authentication and authorization. Once complete it will output role information necessary for us to setup your AppPack account.


!!! warning
    **Don't start creating apps until you've received confirmation that your account is ready.**

!!! pricing "Account Pricing"
    No resources in the account stack should incur AWS charges.

#### Region Creation

Region creation sets up some resources that are specific to the AWS region you're deploying to. You'll be prompted for the Docker Hub credentials noted in the Prerequisites above.

!!! pricing "Region Pricing"
    No resources in the account stack should incur AWS charges.

#### App Cluster Creation

Every app is deployed to a cluster. A cluster may contain multiple apps. The cluster consists of a load balancer, security groups, compute resources, etc. You'll be prompted for:

* The name to identify your cluster. The default is `apppack`.
* The domain to route to your cluster. This should be the same domain, or a subdomain of the domain you created a Hosted Zone for in the Prerequisites. This domain serves as the parent domain for all apps in the cluster. If you use `cluster.example.com` as your domain, an app named `my-app` will be accessible at `my-app.cluster.example.com` in addition to any custom domains you se tup for the app.
* The EC2 instance class that will make up the autoscaling group for your cluster.

!!! pricing "App Cluster Pricing"
    The cluster stack will create resources which incur AWS charges. These include:
    
    * an [Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/pricing/)
    * [EC2 Instances](https://aws.amazon.com/ec2/pricing/) created by the Autoscaling group. Control the instace class used with the `--instance-class` flag during creation.
    * [Custom Cloudwatch Metrics](https://aws.amazon.com/cloudwatch/pricing/) used by [ECS Container Insights](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cloudwatch-container-insights.html)

### Creating a Database Cluster (Optional)

If your applications require a supported RDMS (MySQL or Postgres), you can add a managed RDS database to your cluster. Database stacks are designed to be shared across multiple apps in a cluster, but a cluster may have multiple database stacks. If you wish to isolate a single app to a single database, you can do that too.

```
apppack create database <name>
```

!!! pricing "Database Pricing"
    The database stack will create resources which incur AWS charges. These include:

    * [RDS Instance(s)](https://aws.amazon.com/rds/aurora/pricing/). Control the instance class used with the `--instance-class` flag.

    _Note: The `--multi-az` flag will create two database instances, doubling the cost of the database stack. This is recommended for production instances for maximum uptime, but not necessary for development apps or places where cost optimization is more important than uptime._ 

### Creating a Redis Cluster (Optional)

If your applications require Redis, you can add managed Redis (via Elasticache) to your cluster. Redis stacks are designed to be shared across multiple apps in a cluster, but a cluster may have multiple Redis stacks. If you wish to isolate a single app to a single Redis stack, you can do that too.

```
apppack create redis <name>
```

!!! pricing "Redis Pricing"
    The Redis stack will create resources which incur AWS charges. These include:

    * [Elasticache Node(s)](https://aws.amazon.com/elasticache/pricing/). Control the instance class used with the `--instance-class` flag.

    _Note: The `--multi-az` flag will create two Redis instances, doubling the cost of the Redis stack. This is recommended for production instances for maximum uptime, but not necessary for development apps or places where cost optimization is more important than uptime._ 

## Creating your first App

AppPack apps are largely compatible with apps built for the Heroku platform. Leveraging a [`Procfile`](https://devcenter.heroku.com/articles/procfile) to define services and [`app.json`](https://devcenter.heroku.com/articles/app-json-schema)[^1] to define buildpacks, test scripts, etc. See [apppackio/apppack-demo-python](https://github.com/apppackio/apppack-demo-python) for a simple example.

Once your app is ready, run:

```bash
apppack create app <name>
```

If this is your first app, you'll be prompted to [authorize Codebuild to pull from your repository](https://docs.aws.amazon.com/codebuild/latest/userguide/access-tokens.html) and trigger new builds.

On completion, either push a new commit to the specified trigger branch or run `apppack -a <your-app> build start --wait` to trigger a build and wait for the deployment to complete. _Note, the first deployment of the first app to a cluster takes a minute or two longer while the first EC2 instance is created._

!!! pricing "App Pricing"
    The app stack will create resources which incur AWS charges. These include:

    * Any [EC2 Instances](https://aws.amazon.com/ec2/pricing/) necessary to increase the cluster capacity the demands of the app
    * [CodeBuild](https://aws.amazon.com/codebuild/pricing/) minutes used during the automated build/test process
    * [Cloudwatch Logs](https://aws.amazon.com/ecr/pricing/) for storing application and build logs
    * [Elastic Container Registry](https://aws.amazon.com/ecr/pricing/) costs to store app images
    * [S3](https://aws.amazon.com/s3/pricing/) usage pricing if the add-on is enabled
    * [SQS](https://aws.amazon.com/sqs/pricing/) usage pricing if the add-on is enabled
    * [SES](https://aws.amazon.com/ses/pricing/) usage pricing if the add-on is enabled
    


[^1]: The [`buildpacks`](https://devcenter.heroku.com/articles/app-json-schema#buildpacks), [`stack`](https://devcenter.heroku.com/articles/app-json-schema#stack) and [`environments[test]`](https://devcenter.heroku.com/articles/app-json-schema#environments) portions of `app.json` are currently supported.
