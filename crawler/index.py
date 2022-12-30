import time
import boto3
import requests
import json
import logging
from datetime import date
import os
from crawler_factory import crawler_factory
from get_listings import get_linstings

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


handler = crawler_factory(
    table=boto3.resource("dynamodb").Table(os.environ.get('bucket')),
    log=LOG,
    get_listings=get_linstings
)