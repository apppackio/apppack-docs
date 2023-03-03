# Using S3 for file storage

Enabling the Private/Public S3 add-ons during app creation will create an S3 bucket and give the app full read/write permissions to it. This is done via an IAM role and does not require static AWS access keys. As you'd expect, a public bucket has files that are publicly accessible on the internet while the private bucket only allows authenticated access. Private files may still be served to end-users by generating [presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) within your application.

!!! note
    In the case of Review Apps, a single S3 bucket will be setup for the Pipeline and shared among all Review Apps. Each Review App will be given access to a unique prefix within the bucket.

!!! warning
    Public S3 buckets violate [control S3.2 of Amazon's Foundational Security Best Practices](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-s3-2). In some scenarios, this is not a problem, but be sure you understand the potential risk before enabling them.

!!! warning
    Destroying the application will permanently destroy the bucket(s) and all files in them. Be sure to make a backup first!

## Config variables

The following config variables will be provided to your application:

### Public S3 add-on

* `PUBLIC_S3_BUCKET_NAME` the name of the bucket created for the app
* `PUBLIC_S3_BUCKET_PREFIX` Review Apps only. The name of the S3 object prefix accessible to the application

### Private S3 add-on

* `PRIVATE_S3_BUCKET_NAME` the name of the bucket created for the app
* `PRIVATE_S3_BUCKET_PREFIX` Review Apps only. The name of the S3 object prefix accessible to the application
