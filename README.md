# Serverless crawler stack

This is a tiny experiment I am running to get myself familiar with the AWS CDK. Here is the naive workflow:

1. Crawl Realtor.ca and extract rental apartments in downtown Vancouver using a Lambda function.
2. Store the results in a DynamoDB table for future analytics queries
3. Produce an html report and store on S3
4. Notify provided mobile phone number via an SMS
5. Run the workflow with given intervals (default is 1 day)


## Deployment

Run `cdk bootstrap` if you're running CDK for the first time in your default region.

Bucket name (and also will be used for dynamodb table name) and phone number must be provided as env variables.

```bash
bucket=rental-listings notification_phone_number="+490177853...." cdk deploy
```

## Todo

Doing all these things in a lambda function at once, is not ideal. We can break the current lambda function into 3 independent pieces.

1. Lambda #1: crawl the page, insert listings into dynamodb. This will be triggered by EventBridge rule.
2. Lambda #2: read the latest listings from dynamodb, produce an html report and store on S3. This will be triggered by a dynamodb insert event.
3. Lambda #3: send the public url of the html report via a SMS message. This will be triggered by an S3 file created event.
