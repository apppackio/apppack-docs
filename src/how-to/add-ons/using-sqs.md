# Using SQS (Simple Queue Service)

By enabling the SQS add-on, you can enable your application to work with a queue backed by [Amazon's Simple Queue Service](https://aws.amazon.com/sqs/).

## Overview

The SQS Add-on creates a [FIFO queue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html) and gives the app access to it via its task role. No static access keys are necessary.

Destroying the application will destroy the queue and all messages left in it

## Config variables

* `QUEUE_URL` the name of the queue as `sqs://{name}`
