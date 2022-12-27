import os

from crawler_stack import CrawlerStack
from aws_cdk import App

# check if notification_phone_number is provided with environment
if 'notification_phone_number' not in os.environ or 'bucket' not in os.environ:
    print("notification_phone_number and bucket must be provided in the environment")
    exit()


app = App()
crawler_stack = CrawlerStack(app, "re-crawler-stack", 
    notification_phone_number=os.environ.get('notification_phone_number'),
    bucket=os.environ.get('bucket')
)

app.synth()
