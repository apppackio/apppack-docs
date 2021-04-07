# SES (Email) Add-on

## Prerequisites

* A [verified domain in SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domains.html)
* An account that has been [removed from the sandbox](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html)
* (Optional, but highly recommended) the provided [SPF](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/authenticate-domain.html) and [DKIM records](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-authentication-dkim-easy-setup-domain.html)

## Overview

This add-on provides the app access to send email from addresses in the given domain via its IAM task role.

## Config Variables

None.
