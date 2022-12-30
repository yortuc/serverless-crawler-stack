import time
from datetime import date


def crawler_factory(table, log, get_listings):
    # 
    # create the lambda function with given dependencies
    # not using boto3 directly to separate test code and production code
    # 

    def handler(event, context):
        try:
            listings = get_listings(log)

            table.put_item(Item={
                'createTime': time.time_ns(),
                'createDate': f'{date.today().strftime("%b-%d-%Y")}',
                'listings': listings
            })

        except Exception as ex:
            log.error("Error writing to DynamoDB: " + str(ex))

    return handler