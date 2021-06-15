# Domains

All applications automatically get assigned a subdomain on your AppPack cluster. When setting up your cluster, AppPack will create a wildcard DNS record which points all subdomains to the cluster's load balancer. A wildcard TLS certificate will also be created and attached to the load balancer.

For example, if you setup a cluster with the domain, `cluster.example.com`, any app you create in that cluster will be available via `<appname>.cluster.example.com`. So an app named `my-app` will get assigned the domain `my-app.cluster.example.com`.

It's also possible to setup [custom domains](../how-to/custom-domains.md) to attach a vanity domain to your application.
