# Sending email

By enabling the SES add-on, you can enable your application to send email from a specific domain. This is backed by AWS' [Simple Email Service](https://aws.amazon.com/ses/).

## Prerequisites

* A [verified domain in SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domains.html)
* An account that has been [removed from the sandbox](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html)
* (Optional, but highly recommended) the provided [SPF](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/authenticate-domain.html) and [DKIM records](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-authentication-dkim-easy-setup-domain.html)

## Overview

This add-on provides the app access to send email via the SES API from addresses in the given domain via its IAM task role. 

!!! tip
    Many open source libraries exist for simplifying sending email via SES. Look for one in your preferred language or framework if you don't want to work with the lower-level AWS SDK. 

## Config Variables

None.
