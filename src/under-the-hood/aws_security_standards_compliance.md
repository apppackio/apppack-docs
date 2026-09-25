# AWS Security Standards Compliance

AppPack makes every effort to be compliant with [CIS AWS Foundations Benchmark v1.2.0](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-cis.html) and [AWS Foundational Security Best Practices v1.0.0](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp.html). These controls are not black-and-white rules, but general guidelines for securing AWS resources. The following is the set of controls AppPack does not satisfy.

## AWS Foundational Security Best Practices v1.0.0

### [CodeBuild.5] CodeBuild project environments should not have privileged mode enabled

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-codebuild-5)

As noted in the description of the control, "This parameter should only be set to true if the build project is used to build Docker images." AppPack uses CodeBuild to build Docker images, so privileged mode must be enabled.

### [EC2.10] Amazon EC2 should be configured to use VPC endpoints that are created for the Amazon EC2 service

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-ec2-10)

AppPack configures an endpoint for the S3 service (which is free), but enabling the EC2 endpoint incurs additional cost and is not used by AppPack. 

### [EC2.15] EC2 subnets should not automatically assign public IP addresses

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-ec2-15)

AppPack creates public and private subnets in the VPC. Anything launched into the public subnet is expected to have outbound access to the internet (hence the public IP). The security groups are always locked down so no inbound traffic from the internet is allowed on anything but the load balancer. For services that don't require internet access, the private subnets can be used (which don't assign a public IP).

### [ECR.2] ECR private repositories should have tag immutability configured

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-ecr-2)

AppPack tags images based on their commit hash. In some scenarios, it may be necessary for a user to rebuild an image for a given commit hash. One example might be changing a configuration variable which the build depends on. AppPack also follows the common pattern of retagging a `latest` image on new builds, although the images used are always referenced by the commit hash.

### [ECS.2] ECS services should not have public IP addresses assigned to them automatically

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-ecs-2)

Most applications need access to the internet to communicate with third-party APIs. Without a public IP, [Managed NAT Gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) are required to access the internet. To provide resilience against availability zone outages, multiple NAT Gateways are preferred. To avoid a significant increase in the cost to run an AppPack cluster, ECS tasks are assigned a public IP instead. AppPack uses locked-down security groups to prevent any inbound public access to ECS services on public IPs. Only the load balancer is exposed to the internet.

### [ECS.5] ECS containers should be limited to read-only access to root filesystems

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-ecs-5)

Many applications require some sort of ephemeral file system access for temporary files and caches.

### [S3.9] S3 bucket server access logging should be enabled

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-s3-3-9)



### [RDS.5] RDS DB instances should be configured with multiple Availability Zones

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-rds-5)

Multi-AZ databases are double the cost of a single-AZ database. In some scenarios (non-production environments) the additional resiliency may not be required. When creating an AppPack database, you have the option to choose a multiple or single AZ deployment.

### [RDS.23] RDS instances should not use a database engine default port

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-rds-23)

[Security through obscurity](https://en.wikipedia.org/wiki/Security_through_obscurity) is a heavily debated topic with many industry leaders arguing against its value. In order to improve usability, AppPack creates databases on their default ports.

### [S3.2] S3 buckets should prohibit public read access & [S3.8] S3 Block Public Access setting should be enabled at the bucket-level

[link S3.2](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-s3-2)
[link S3.8](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-s3-8)

All S3 buckets created by AppPack prohibit public access with the exception of the optional "Public S3 Bucket" app add-on. In many deployment scenarios, S3 is used to serve publicly accessible static files. If this is not desired, AppPack also provides a "Private S3 Bucket" app add-on.

### [S3.11] S3 buckets should have event notifications enabled

[link](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-s3-11)

Files being added or removed from a bucket is standard operating procedure. If additional auditing is required, this can be added independent of AppPack.