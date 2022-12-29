import boto3
import logging
import os
import json


LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

def handler(event, context):
    bucket = os.environ.get('bucket')
    LOG.info("Event received: " + json.dumps(event))

    try:
        sns = boto3.client('sns')
        s3 = boto3.client('s3')
        
        for record in event["Records"]:
            s3record = record["s3"]
            key = s3record['object']['key']

            public_url = '%s/%s/%s' % (s3.meta.endpoint_url, bucket, key)

            sns.publish(
                PhoneNumber = os.environ.get('notification_phone_number'),
                Message=f"Yeni evler: {public_url}",
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': "YortucEmlak"
                    }}
            )

    except Exception as ex:
        LOG.error("Error sending sms")