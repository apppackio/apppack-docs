# Custom Domains

For production apps, you'll usually want to setup a friendlier user-facing domain as well. This is called a "custom domain" in AppPack. Getting a custom domain setup is a two step process.

## Routing

During the app creation process, you can enter your custom domain name at the prompt "custom domain to route to app". That will create a rule which routes traffic on that domain from the load balancer. At this point, your application is ready to accept traffic from the custom domain, but the domain is not yet pointing at the load balancer.

## DNS & TLS

To serve traffic from your domain, the following needs to happen:

1. Create ACM Certificate and attach it to the Application Load Balancer listener
2. Create a DNS record which points the domain to the Application Load Balancer

This can be done automatically for domains which are already setup as a Route53 Hosted Zone in your AWS account or manually for domains which are managed externally.

### Automatic Setup

The CLI includes an [`apppack create custom-domain`](/command-line-reference/apppack_create_custom-domain/) command for domains which already have a Route53 Hosted Zone in your AWS account. It will handle certificate creation/validation, attaching the certificate to the load balancer, and creating `ALIAS` records which point the domain(s) to the load balancer.

### Manual Setup

If your domain is managed outside of AWS, a few manual steps are required.

1. [Request a public certificate via ACM](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)
2. [Add the certificate to the load balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-update-certificates.html#add-certificates) (note: the load balancer will have the same name as the AppPack cluster where your app is installed)
3. Setup a `CNAME` DNS record which points to your internal AppPack domain name (`<app_name>.<cluster_domain>`)

!!! warning
    `CNAME` records shouldn't be used on an apex (aka root or naked) domain [^1] and AWS Load Balancers do not provide static IPs. If you need to point an apex domain to your application, check if your provider offers a solution such as [Cloudflare's CNAME flattening](https://blog.cloudflare.com/introducing-cname-flattening-rfc-compliant-cnames-at-a-domains-root/). If not, they may be able to redirect the apex domain to a subdomain that can use a `CNAME`, e.g. `example.com` to `www.example.com`.


[^1]: [A thorough explination of why `CNAME`'s on apex domains are bad](https://serverfault.com/a/613830/50450)
