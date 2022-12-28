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

## Architecture

1. An EventBridge rule trigers the crawler lambda function at specified intervals (once a day by default). Crawler lambda function crawls the page, extracts the listing links, addresses and prices and inserts into dynamodb table. 

2. Dynamodb event stream triggers report creator lambda function. 
