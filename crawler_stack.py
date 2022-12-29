from aws_cdk import (
    aws_lambda,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    aws_s3,
    aws_iam,

    BundlingOptions, RemovalPolicy,
    Stack, Duration
)

from aws_cdk.aws_lambda_event_sources import (
    DynamoEventSource,
    S3EventSource
)


class CrawlerStack(Stack):
    def __init__(self, scope, id: str, notification_phone_number: str, bucket: str):
        super().__init__(scope, id)

        # Lambda func to crawl realtor.ca
        lambda_crawler = aws_lambda.Function(self, "re-crawler-lambda", 
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            timeout=Duration.minutes(10),
            code=aws_lambda.Code.from_asset(
                "./crawler",
                bundling=BundlingOptions(
                    image=aws_lambda.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash", "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ],
                ),
            ),
            environment={
                'bucket': bucket
            }
        )

        lambda_report_creator = aws_lambda.Function(self, "re-report-creator-lambda", 
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            timeout=Duration.minutes(10),
            code=aws_lambda.Code.from_asset("./report_creator"),
            environment={
                'bucket': bucket
            }
        )

        lambda_sms_sender = aws_lambda.Function(self, "re-sms-sender-lambda", 
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            timeout=Duration.minutes(10),
            code=aws_lambda.Code.from_asset("./sms_sender"),
            environment={
                'bucket': bucket,
                'notification_phone_number': notification_phone_number,
            }
        )

        # allow lambda func to publish sms
        sns_publish_policy = aws_iam.PolicyStatement(
            actions=["sns:Publish"],
            resources=["*"]
        )
        lambda_sms_sender.add_to_role_policy(sns_publish_policy)

        # dynamodb table
        table = aws_dynamodb.Table(self, "re-crawler-links", 
            table_name=bucket,
            partition_key=aws_dynamodb.Attribute(name="createTime", type=aws_dynamodb.AttributeType.NUMBER),
            # sort_key=aws_dynamodb.Attribute(name="createTime", type=aws_dynamodb.AttributeType.NUMBER),
            removal_policy=RemovalPolicy.DESTROY,
            stream=aws_dynamodb.StreamViewType.NEW_IMAGE
        )
        # let lambda_crawler write to the dynamodb table
        table.grant_read_write_data(lambda_crawler)

        # add dynamodb trigger to report_creator
        lambda_report_creator.add_event_source(DynamoEventSource(table, 
            starting_position=aws_lambda.StartingPosition.LATEST,
            batch_size=5,
            retry_attempts=2
        ))

        # s3 bucket to store html summaries
        bucket = aws_s3.Bucket(self, "re-crawler-bucket", 
            auto_delete_objects=True, # bucket can be deleted properly when we run "cdk destroy"
            bucket_name=bucket,
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=aws_s3.BlockPublicAccess(block_public_policy=False),
            access_control=aws_s3.BucketAccessControl.PUBLIC_READ,
        )
        bucket.grant_read_write(lambda_report_creator)
        bucket.grant_public_access()

        # trigger sms_sender once the report is created on S3
        s3_event_source = S3EventSource(bucket, events=[
            aws_s3.EventType.OBJECT_CREATED_PUT
        ])
        lambda_sms_sender.add_event_source(s3_event_source)

        # run the crawler every day/hour
        rule = aws_events.Rule(self, "re-crawler-scheduler",
            schedule=aws_events.Schedule.rate(Duration.days(1)),
            targets=[aws_events_targets.LambdaFunction(lambda_crawler)]
        )
