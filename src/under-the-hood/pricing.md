# Pricing

You will incur standard AWS charges for some resources created and used by AppPack in your account.
    
Some resources are such as [EventBridge Events](https://aws.amazon.com/eventbridge/pricing/), [SSM Parameters](https://aws.amazon.com/systems-manager/pricing/#Parameter_Store), and [Lambda Functions](https://aws.amazon.com/lambda/pricing/) are priced so low (fractions of a cent/month) or have such generous free tiers that they are essentially free. Others will not be and are noted below.

To track the cost of your AppPack resources, we recommend setting up [User-Defined Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html). All AppPack resources will get an `apppack:*` (e.g. `apppack:cluster`, `apppack:appName`, `apppack:database`) tag you can use for fine-grained tracking.

Also don't forget about the [Free Tier](https://aws.amazon.com/free/), [Reserved](https://aws.amazon.com/rds/reserved-instances/) [Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/), [Savings Plans](https://aws.amazon.com/savingsplans/pricing/) and [AWS Activate Startup Credits](https://aws.amazon.com/activate/)!

## Account

Account-level resources are created during the initial setup and do not incur any AWS charges.

## Region

Region-level resources are created during the initial setup and do not incur any AWS charges.

## Cluster

Cluster-level resources are created during the initial setup (or using `apppack create cluster`). They include the following resources which may incur AWS charges:

* an [Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/pricing/)
* [Custom Cloudwatch Metrics](https://aws.amazon.com/cloudwatch/pricing/) used by [ECS Container Insights](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cloudwatch-container-insights.html)

## Application/Pipeline

Applications include the following resources which may incur AWS charges

* [Fargate Tasks](https://aws.amazon.com/fargate/pricing/) as defined by the application
* [CodeBuild](https://aws.amazon.com/codebuild/pricing/) minutes used during the automated build/test process
* [Cloudwatch Logs](https://aws.amazon.com/ecr/pricing/) for storing application and build logs
* [Elastic Container Registry](https://aws.amazon.com/ecr/pricing/) costs to store app images
* [S3](https://aws.amazon.com/s3/pricing/) usage pricing if the add-on is enabled
* [SQS](https://aws.amazon.com/sqs/pricing/) usage pricing if the add-on is enabled
* [SES](https://aws.amazon.com/ses/pricing/) usage pricing if the add-on is enabled

## Database

Databases include the following resources which may incur AWS charges:

* RDS Instance(s) ([Aurora](https://aws.amazon.com/rds/aurora/pricing/), [Standard MySQL](https://aws.amazon.com/rds/mysql/pricing/), or [Standard Postgres](https://aws.amazon.com/rds/postgresql/pricing/))

!!! pricing
    The `--multi-az` flag will create two database instances, doubling the cost of the database stack. This is recommended for production instances for maximum uptime, but not necessary for development apps or places where cost optimization is more important than uptime.

## Redis

Redis includes the following resources which may incur AWS charges:

* [Elasticache Node(s)](https://aws.amazon.com/elasticache/pricing/)

!!! pricing
    The `--multi-az` flag will create two Redis instances, doubling the cost of the Redis stack. This is recommended for production instances for maximum uptime, but not necessary for development apps or places where cost optimization is more important than uptime.


