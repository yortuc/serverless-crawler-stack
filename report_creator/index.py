import boto3
import logging
import os
import json

from render_html import render_html


LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

def dynamo_to_list(item):
    return {
        'address': item['M']['address']['S'],
        'link': item['M']['link']['S'],
        'rent': item['M']['rent']['S']
    }

def handler(event, context):
    bucket = os.environ.get('bucket')

    LOG.info("Event received: " + json.dumps(event))

    try:
        s3 = boto3.client("s3")
        
        # get new listings from the event
        for record in event["Records"]:
            LOG.info("Record: " + json.dumps(record))

            listings = map(dynamo_to_list, record['dynamodb']['NewImage']['listings']['L'])
            create_date = record['dynamodb']['NewImage']['createDate']['S']

            s3.put_object(
                Body=render_html(listings),
                Bucket=bucket,
                Key=create_date + ".html",
                ContentType='text/html'
            )
            
    except Exception as ex:
        LOG.error("Error creating report: " + str(ex))
