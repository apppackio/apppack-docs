# Why AppPack?

## Current Solutions

There are a million ways to run code on the web, why does AppPack need to exist?

### :warning: Complexity/Cognitive Load

Most platforms require a massive amount of new knowledge just to get started. A developer shouldn't have to learn Systemd, Docker, Kubernetes, IAM, etc. to put a website on the internet. Kubernetes is designed for businesses that operate at _massive_ scale. AppPack is for the 99% of companies and developers that operate at a more _human_ scale.

For this group, platform-as-a-service (PaaS) is the right tool for the job. It requires very little specialized knowledge and offloads operational concerns. You can get very far on this model and avoid the need for a full-time ops/SRE team to monitor your platform.


### :warning: PaaS Limitations

But PaaS has its drawbacks too. You need to trust a third-party (probably running on top of AWS or GCP) with all your IP and data. Your app is likely running in a sandbox on a machine next to apps from other customers. Potentially The cost of everything is marked up over raw computing costs at AWS so it can get expensive quickly. Features can be limited and you may need to glue together services from multiple providers, increasing your risk of an outage or data breach. Building solutions that don't fit inside the PaaS box can be difficult.

## AppPack

AppPack gives you the benefits of a PaaS while removing many of the drawbacks. It leverages managed services on AWS to get you the same (or better) reliability and peace-of-mind.

### :white_check_mark: Cost

With AppPack, you can run a PaaS with compute resources from your AWS account. You pay a flat fee for AppPack (TBD) and can scale your application's resources at AWS' cost. You can even leverage savings plans and reserved instances for further savings.

### :white_check_mark: Privacy

Your infrastructure is fully isolated in your AWS account. All internal communication is performed in a virtual private network (VPC). Databases and caches live in a private subnet and are completely inaccessible to the public internet.

### :white_check_mark: Flexibility

Since your app and data reside in your AWS account, you have access to the AWS universe and all 175+ services within it. Need AI? Blockchain? a document DB? Serverless Functions? AWS has you covered. AppPack makes it easy to get started with the basics like relational databases, caches, email, file storage, and queueing. But when your app outgrows that, you can start leveraging the rest of AWS without needing to deal with giving access keys to third-parties or shipping sensitive data over the public internet.

### :white_check_mark: Visibilty

With traditional PaaS, you have very little insight into how your application is running. Usually it's not important information, but as your app starts to scale, having deep insight into the platform can be hugely beneficial. On AppPack, you are always able to pull away the curtain and see everything that makes up your application. Want to know the buffer cache hit ratio of your database? the active connections on your load balancer? how your services are distributed across the compute resources? All of it is just a few clicks away in the AWS console.
