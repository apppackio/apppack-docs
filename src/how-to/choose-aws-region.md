# Choose an AWS Region

AWS operates in many regions throughout the world. AppPack can run in multiple regions, but each cluster you create will be in a specific region of your choosing.

Generally, you want to run your application in a region closest to where the majority of your users are. The farther away your users are, the higher latency they will experience loading your application. If you're unsure, `us-east-2` and `us-west-2` are generally the least expensive, best supported (in terms of features/functionality), and most stable regions. If the majority of your users are outside the United States, you may want to select a different region. You can find the [full list here](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/).

AppPack is currently available in:

* US East (N. Virginia) `us-east-1`
* US East (Ohio) `us-east-2`
* US West (Oregon) `us-west-2`
* Asia Pacific (Seoul) `ap-northeast-2`
* Asia Pacific (Mumbai) `ap-south-1`
* EU (Stockholm) `eu-north-1`
* EU (London) `eu-west-2`

If you would like to use AppPack in a different region, send a request to support@apppack.io.
