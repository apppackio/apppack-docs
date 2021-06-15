# Overview

What is AppPack doing under-the-hood to make this all happen?

With AppPack applications run in your AWS account. The data, secrets, and application code never leave your account. Everything is setup in AWS managed services. It is designed to be secure, resilient, auto-scaling, and self-healing. It should require little to no effort to maintain these systems (because Amazon is doing the heavy lifting for you).

During set up, a handful of [EventBridge](https://aws.amazon.com/eventbridge/) Rules are set up to send changes in your application state to our control plane. These events only contain basic information about things like a Codebuild build starting or a release task finishing. Our control plane will then determine what needs to happen in response to the event and make the necessary API calls to continue. For example, after a release task is successful, any services that need to be started will be updated or created as needed so ECS can update the application.

Our control plane uses a locked down IAM role to communicate to AWS in your account. This role only has access to do things like update services and task definitions in ECS, read Codebuild metadata, etc. It has been designed with the least necessary privileges to accomplish these tasks. 

## The Stacks

During setup, you'll create multiple Cloudformation Stacks for different resources.

### Account

At the account level we setup:

* An [IAM OIDC provider](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html) which will allow users to login to AppPack and exchange those credentials for limited time tokens to manage the application.
* [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) values for your Docker Hub credentials. These are created directly via the CLI [because `SecureString` credentials cannot be created by Cloudformation](https://github.com/aws-cloudformation/aws-cloudformation-coverage-roadmap/issues/82).
* An EventBridge rule to monitor changes to the Parameter Store. These events only include the name of the Parameter, not the value and any value that doesn't match AppPack's prefix is ignored.
* An IAM Role that is used by AppPack to collect further data on events that do not include enough information to know what app they belong to. These include:
  * [ECS Task state change](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwe_events.html#ecs_task_events) events
  * [ECS Service action](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwe_events.html#ecs_service_events) events
 
### Cluster

At the cluster-level, we setup:

* A [VPC](https://aws.amazon.com/vpc/) in three availability zones with public and private subnets, an [S3 gateway endpoint](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints-s3.html), an internet gateway, and flow logs.
* An [ECS](https://aws.amazon.com/ecs/) Cluster
* _[Optional[^*]]_ An [EC2](https://aws.amazon.com/ec2/) auto-scaling group to run the container instances.
* _[Optional[^*]]_ A [Capacity Provider](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html) to ensure there are always enough EC2 instance to cover the resources needed by the ECS tasks.
* An [Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/application-load-balancer/) to route traffic to the application(s) in the cluster.
* An HTTP listener to redirect all insecure traffic to HTTPS.
* A [Route53](https://aws.amazon.com/route53/) wildcard DNS entry to point a domain to the load balancer.
* An [ACM certificate](https://aws.amazon.com/certificate-manager/) for the wildcard domain, connected to an HTTPS listener on the load balancer.
* All the necessary [security groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) to allow internet traffic to the load balancer and route traffic from the load balancer into the applications.

_Note: to avoid the need for (expensive) [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html), the ECS cluster runs on the VPC's public subnet. Security groups are in place to block all incoming traffic from outside the VPC._

[^*]: The default cluster setup uses [Fargate](https://aws.amazon.com/fargate/) which does not require any self-managed EC2 instances.
### App

The app stack creates:

* A [Codebuild](https://aws.amazon.com/codebuild/) project connected to the code repository for continuous building and testing.
* A private [S3](https://aws.amazon.com/s3/) bucket for storing build metadata and artifacts.
* An [Elastic Container Repository (ECR)](https://aws.amazon.com/ecr/) for storing container images
* A listener rule and target group to route traffic to the application from the load balancer.
* A [Cloudwatch](https://aws.amazon.com/cloudwatch/) Log Group for storing application logs. Another Log Group is used for storing Paaws activity related to the application.
* A security group to allow the application to make outbound network calls
* [IAM Roles](https://aws.amazon.com/iam/features/manage-roles/) for:
    * ECS Execution
    * ECS Tasks
    * Events (for scheduled tasks)
    * AppPack management
    * User operations

### Database

The database stack creates:

* An [Aurora Postgres RDS](https://aws.amazon.com/rds/aurora/) Cluster
* Database subnet groups in the private subnets of the VPC
* One or two (if multi-az) DB Instances in the cluster
* A Lambda function used to manage the database cluster. It can perform 3 tasks:
    1. create/destroy Postgres databases within the cluster
    2. enable IAM authentication on the admin database user
    3. executing one-off custom SQL as the admin user (useful for installing extensions which cannot be done by the application users)


## Authentication

Authentication is handled via [Auth0](https://auth0.com/). After successfully logging in with an account with a verified email, the CLI or web interface will exchange your login token for AWS keys for an IAM Role specific to the application that is being managed. This is done via the [`WebIdentityCredentials` API](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/WebIdentityCredentials.html) either in your web browser or via your terminal. It will verify the token and also confirm the user is authorized to access the app. AppPack never has access to these keys or the traffic between your device and AWS.

## Web Interface

The web interface at [https://dashboard.apppack.io](https://dashboard.apppack.io) uses the AWS JavaScript SDK to make calls directly to AWS from your computer. This allows us to make the website a completely static site (it is served from S3) without any backend that could access your data. After the initial login, all network traffic is direct to AWS.

## CLI

The CLI works the same as the web interface. Logging in requires using a web browser to login with a custom code which identifies your device. Once logged in, a token is stored in your user's cache directory to allow continued access.
