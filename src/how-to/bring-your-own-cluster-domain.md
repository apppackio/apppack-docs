# Bring Your Own Cluster Domain

When setting up a cluster, AppPack needs access to a domain which has a hosted zone in AWS Route53.

The easiest way to do this is to register a new domain in Route53. Amazon will create the hosted zone for you as part of the process.

## Whole Domain

If you have a domain you'd like to use and it is not managed via a Route53 Hosted Zone, you can create the hosted zone and then update the domain's name server (`NS`) records to allow it to be managed in AWS.

This process is outlined in Amazon's [_Creating a public hosted zone_](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html) document.

## Sub-domain

You can also use a subdomain of a domain you already own. If the domain is part of a Route53 Hosted Zone already, no further action is required. AppPack will find it and create the necessary records.

If your DNS is managed elsewhere, you can create a Hosted Zone for just the sub-domain you wish to use.

This process is outlined in Amazon's [_Creating a subdomain that uses Amazon Route 53 as the DNS service without migrating the parent domain_](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html) document.