# Initial setup

This tutorial will walk you through the initial AppPack setup in your AWS account. You will connect your AWS account to AppPack and setup your initial cluster for installing apps. This process should take about 25 minutes to complete, with the majority of waiting for AWS to spin up resources and setup a domain.

## 📝 Prerequisites

You'll need a few things ready to go to complete this tutorial. Make sure you've taken the following steps before getting started.

1. Installed **the `apppack` CLI** (see _[Install the CLI](../how-to/set-up/install.md)_)
2. Setup **an AWS account** with access to an admin user or role.
3. Create a [free Docker Hub account and generate an access token](../how-to/set-up/create-docker-hub-access-token.md).


## 🏗 Setting up AWS resources

⏳ _Estimated Time: 3 minutes_

AppPack is currently available in a number of AWS Regions. Let's get started by 
clicking the "Launch Stack" button for your nearest region[^1] below. This will 
open the AWS Console to begin creating a resource Stack using AWS CloudFormation.
We will use a pre-defined JSON template, so we can start using AppPack.

| Stack                                                                                                                                                                                                                                                                                                                                              | Region                                    |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| [![Create AppPack Stack in us-east-2](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://us-east-2.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank}           | US East (Ohio) `us-east-2`                |
| [![Create AppPack Stack in us-west-2](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://us-west-2.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank}           | US West (Oregon) `us-west-2`              |
| [![Create AppPack Stack in us-east-1](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://us-east-1.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank}           | US East (N. Virginia) `us-east-1`         |
| [![Create AppPack Stack in ap-northeast-2](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://ap-northeast-2.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank} | Asia Pacific (Seoul) `ap-northeast-2`     |
| [![Create AppPack Stack in ap-south-1](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://ap-south-1.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank}         | Asia Pacific (Mumbai) `ap-south-1`        |
| [![Create AppPack Stack in ap-southeast-1](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://ap-southeast-1.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank} | Asia Pacific (Singapore) `ap-southeast-1` |
| [![Create AppPack Stack in ap-southeast-2](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://ap-southeast-2.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank} | Asia Pacific (Sydney) `ap-southeast-2`    |
| [![Create AppPack Stack in eu-north-1](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://eu-north-1.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank}         | Europe (Stockholm) `eu-north-1`           |
| [![Create AppPack Stack in eu-west-2](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://eu-west-2.console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=apppack-account&templateURL=https%3A%2F%2Fs3.amazonaws.com%2Fapppack-cloudformations%2Flatest%2Faccount.json){target=_blank}           | Europe (London) `eu-west-2`               |

The process of creating an AWS CloudFormation Stack is divided into four steps:

**1\. Specify template**

The first step is selecting the template to use. Since that was defined in the link,
we can skip this step:

* Click `Next`

**2\. Specify stack details**

1. In the `Administrators` field, enter your email address and the email addresses 
   of anyone else you'd like to grant full admin access to your account.
   ![create administrators screenshot](./../assets/create-administrators.png)

2. Click `Next`

**3\. Configure stack options**

1. In the `Capabilities` section, at the bottom of the screen, check the box titled   
   _I acknowledge that AWS CloudFormation might create IAM resources._   
2. Click `Next`  

**4\. Review and create**

* Click `Submit`

[^1]: See [Choose an AWS Region](../how-to/set-up/choose-aws-region.md) for more info

## 🔐 Authenticate AppPack CLI

⏳ _Estimated time: 1 minutes_

Next, run:

```shell
apppack auth login
```

<script id="asciicast-BkCDHIskycHdYNt3e8rMjbUAt" src="https://asciinema.org/a/BkCDHIskycHdYNt3e8rMjbUAt.js" data-rows="8" async></script>

You'll be able to login or create a new account if you don't have one already. If you login with an email address and password, be sure to verify your email address before continuing.

Verify you are setup as an administrator:

```shell
apppack auth accounts
```

<script id="asciicast-oX0JCUxQVWytfqVXNaKaqE6eg" src="https://asciinema.org/a/oX0JCUxQVWytfqVXNaKaqE6eg.js" data-rows="10" async></script>

You should see your AWS account listed in the output.

## 🌐 Setup a domain

⏳ _Estimated time: 15 minutes_

You'll need to assign a domain to your cluster. If you used `example.com` for your cluster, apps you create on the cluster will be available at `https://{appname}.example.com`. You can use a custom domain for production apps, so this domain is typically just used internally.

The easiest option here is to [register a new domain in your AWS console](https://console.aws.amazon.com/route53/home#DomainRegistration:). Depending on the TLD you choose, they can be had for as little as $3/year (looking at you `.click` 👀).

!!! warning
      ⏳ This isn't an instant process, so be prepared to wait at least a few minutes for your domain to move from [Pending](https://console.aws.amazon.com/route53/home#DomainRequests:) to [Registered](https://console.aws.amazon.com/route53/home#DomainListing:). Also make sure you've [entered your billing info](https://console.aws.amazon.com/billing/home#/paymentmethods) in the AWS console to avoid any extra delay.

!!! info
    If you'd rather use a domain you already own, see the [Bring Your Own Cluster Domain](../how-to/domains/bring-your-own-cluster-domain.md) how-to.

## 👷‍♀️ Create your cluster

⏳ _Estimated time: 7 minutes_

Now you're ready to create the cluster for your apps. To do this, run:

```shell
apppack create cluster
```
<script id="asciicast-9MQqww0ej7qAMhLjvM708mh00" src="https://asciinema.org/a/9MQqww0ej7qAMhLjvM708mh00.js" data-rows="20" data-theme="monokai" async></script>

You'll get a confirmation prompt about the region where the cluster will be installed. Type `yes` and you'll be prompted for:

1. Your Docker Hub username and access token
2. Your domain you created above

This should run for about 10 minutes while AWS creates all the necessary resources.

!!! pricing
    Some resources created during this process may incur monthly AWS charges. Read [Under the Hood: Pricing](../under-the-hood/pricing.md) for more information.

## 🏁 Next step

Congrats! Now that your account has been approved, you're ready to deploying apps. Continue on to the [Deploy Your First App](../tutorials/deploy-first-app.md) tutorial
