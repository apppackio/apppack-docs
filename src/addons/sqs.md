# SQS (Queue) Add-on

## Prerequisites

None

## Overview

The SQS Add-on creates a [FIFO queue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html) and gives the app access to it via its task role.

Destroying the application will destroy the queue and all messages left in it

## Config Variables

* `QUEUE_URL` the name of the queue as `sqs://{name}`
