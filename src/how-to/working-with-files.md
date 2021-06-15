# Working with files

AppPack apps are stateless and do not provide persistent file storage. If you require persistent file storage, you'll want to use the [S3 add-on](./using-s3.md) and make sure your app is capable of reading/writing to S3. Once you're using the add-on, you'll have a number of ways to upload files to your bucket(s).

## Uploading files to S3

### Directly from your application

Once your application is capable of reading/writing to S3, usually your application code will be used to write files (either via user uploads or dynamically generated) to S3.

### Direct uploads

You may not want file uploads to go through your app server. In that scenario, your users can upload directly to S3 from their browser and your app server is only responsible for generating a short-lived token to authenticate the request on behalf of your user. If you are expecting exceedingly large files, this is a great alternative to blocking your app server with file uploads.

Amazon's documentation covers [browser-based uploads using HTTP POST](https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-authentication-HTTPPOST.html) and many JavaScript libraries exist to facilitate this functionality in the browser.

### Manual uploads

You can also upload files using the AWS CLI. If you don't already have it installed, follow [Amazon's installation instructions for your platform](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

The AppPack CLI can be used to generate temporary access keys for use with the CLI. Let's say you have an app named `my-app` and it has an S3 bucket named `apppack-app-my-app-privates3bucket-1197pfxl0pxsv` (you can get this name from `apppack -a <appname> config list`). To copy a local file named `myfile.txt` to that bucket, you could run:

!!! example
    ```
    apppack -a my-app aws-exec -- aws s3 cp myfile.txt s3://apppack-app-my-app-privates3bucket-1197pfxl0pxsv
    ```

Everything after the `--` in that command is part of the AWS CLI. [See their docs for more info](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html).


## Downloading files from S3

### Direct from S3

For public S3 buckets, [files can be downloaded directly via HTTPS from the bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html).

### Via the AWS SDK

Private files may be downloaded by your app via the AWS SDK for your language. Many open source libraries exist to make this an even easier process. From the application, credentials will automatically be available. Locally, you'll want to use the [`apppack aws-exec`](https://docs.apppack.io/command-line-reference/apppack_aws-exec/) command to generate temporary credentials for your program (or the AWS CLI).

### Direct from S3 via presigned URLs

You can generate short-lived presigned URLs for files in a private bucket which allow you download directly from S3 using a browser or any other HTTP client. This is often used when your application needs to verify who a user is before giving it permission to access a file. It can verify the user and then pass the presigned URL back to it.

[Generating a presigned URL can be done via the AWS CLI or any of its SDKs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html).

If you wanted to generate a presigned URL with the CLI from your local machine, you could run:

!!!example
    ```
    apppack -a my-app aws-exec -- aws s3 presign --expires-in 600 s3://apppack-app-my-app-privates3bucket-1197pfxl0pxsv/myfile.txt
    ```

This would generate a presigned URL that expires in 10 minutes (600 seconds) for the file we uploaded in the previous example.
