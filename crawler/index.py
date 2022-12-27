import time
import boto3
import requests
import json
import logging
from datetime import date
import os


LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

def get_linstings():
    # Chrome dev-tools, copy as curl
    # Convert curl to python using https://curlconverter.com/

    cookies = {
        'visid_incap_2269415': 'LcnofuD5S9eqfKkjb3ezKZIdpGMAAAAAQUIPAAAAAABcYK8lS17cOYeVpZQIwCqf',
        'nlbi_2269415': 'Ol29BWgZwmQD9r8uzBLR3QAAAADL0H5S31Qfzv7C9u8hEBWh',
        '_gcl_au': '1.1.1134938651.1671699861',
        '_gid': 'GA1.2.5995056.1671699861',
        'ASP.NET_SessionId': 'asjnxpq1dqowglg43uvrckrm',
        'visid_incap_2271082': '4Omt0GzIQpCcJ+A1xxbyeJQdpGMAAAAAQUIPAAAAAACwIx84Ga4AzSW9shuioHUx',
        'nlbi_2271082': 'iOP/ZEAz3Gi5BfZHVPrQ3QAAAAAGS9UkCRK/7Ttw8Ep20aDG',
        'gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko': 'gigya-pr_ver4',
        'nlbi_2271082_2147483392': 'yRVHBWIzpS6fLqgfVPrQ3QAAAACX6qPRHLi4yzbpIkJ5A87U',
        'reese84': '3:g8eXs6IY/EiUHUKmUD3qNg==:KkB6/GbmFOEJZhMRkhvr7iekr8ck1E0K/Ddq/r7PYkHLJM4bFRZri8pyxA5wsKp3TotS3kxoYRTvLDq4oNA7GKs66kX8p7E7kXSpaTVPiJT6hr9RaW923bHAKAXnyUub0hnYXA8VTI1ROVu5xGYP0Cuj22rceAj09AjBkb4UtCFcU2x8kSrhz8cw+qvVb9jvCwBZAmy+k0iIbddbiCAhkCfxzXfXcUzeywc0gDBfiIWQpqhC1Bpr+EgGvYGuvWxIoCa2i2jPbjGPwwnKfZi0WQnWs2M0wwUCwB5/iFfVzCQjd6O2rNvdMBQ4slq1Stp7+IYKc2DyX4FHhIP6jYyUmsV9zOTEnbzW8vhBH8wlUew6qvsMvxe3hduc5o4IykBqyO+eEjbOreWx50MpxaPXKgLWNWK25HxDiVkunhA/J3xZeOgQsb3V5sj34INhZ00FKQ8Z+n0lXt0pE0kJFHrUHLr4w0M0gxXakSz/qRtrsGE=:AHzWwJznbixqctghyz20PIRJZBorKzA8FPfEqaGZDMY=',
        'incap_ses_1193_2269415': '6uAUCwOsfBmWJUUs6GOOEKI0pGMAAAAACOlHNeYN7e5RYlzW9KkTDw==',
        'reese84': '3:BCB5kKvdoKYTkXr2ItrgEg==:Imlew4rN+eS40cj5DSnLz5DkvjZDkANLWYrGwaE+mKI3WpHoHNz9pcyHtT2FZYxH1zLZOlKRaW6bt9VqnhPY5ook11s8KLJieumoQOj0/g+2LtmVxGzoT4wAZI9lWR1/jyDH1v7mSea2CxZmByc+ppqThwAHsSkhXKNEZgdSgHuUJY0FscciCVBFI3d5w/BenipXhCf1lGbc64lV9sxJkuLkoBq/DvOu4zulB+GxOsndY+kcVEDuvyWCenKScmjHFVlpvhLlIaGL6YkfUEy4IO+znrfzlV5wBSU4gHtvfQ3y8nJ0GQ6HG53yPUTQ4hHk9AG78YQ4KzR4ef1dGRdhj+U8luMTZM4tdJ60x3alMt+/C59Q2fw4zpCmw1YNYygxnhuL/IdSXNjM0cD/jWn+z32cNPRxeNoDoEZugC8mxBTnoNm1a8eMDB0Uz7lJSWXMeHqT+vb6iFqVtfEQVUWCvxbaLmOkfZju3Vfo6gem25U=:257M9saOx+ynZ+yu9sjKT2JLUtgBaDO2gwxg/JARowA=',
        'nlbi_2269415_2147483392': 'B3P9P1Xw0ANDPueIzBLR3QAAAAABEqSGZ8Zwt0/bAVenmn67',
        '_dc_gtm_UA-12908513-11': '1',
        '_ga': 'GA1.1.1584617771.1671699861',
        'incap_ses_1193_2271082': '5T9bUepvUTy9X0Ys6GOOECI8pGMAAAAAMEMOOe76M5YfsDLZ8efNkA==',
        '_4c_': '%7B%22_4c_s_%22%3A%22lZLNrpswEIVfJfIaR3YwNs6uSqXqSq1UVe06AnsAKwQj44TeRrx7x9yk6c%2BqLGD8eebYzJkbmTsYyJ5LxRVTUnNVioyc4HUi%2BxsJzqbPlexJYa0o9K6mLGecCtVYqplmVBUGbF5yZXhOMvJ91dJCFaXkSqglI2a8a9yI8RZQi%2BstF1vOaDNhSfyRUMkwHIO3FxOP8XVMeTPUm8mecMPC1Rk4zs7GLmULxZ60A9d2EbEuZKJjwHiH0ewG6%2Be%2Fq%2B70V5USAmkd%2FDxBqjx0wZ9hw1mJ2GMfyKfKYBiggRDWFFxNLqYrBqj66MPWVHeGrXtiuuKP1dBeqnb987T0bQt284JtJ03VT4Dsc%2FBXNxh40z74yxBD0vl6CUkwI19gchaG6Kreh4M%2FnyE4U%2FW%2FSYzJpWRB73EjKaGxGb4SH4PF%2BMO747eX9%2BkaRSnQHqX4NjkvtUa3yPKwj6OBDDMEjkKMeEgpBUvP8nbM6mb%2BZ3Yu8%2FzfbAvTKfqRPvoBw%2F%2FVX91j%2FkoNIKvGUABbUyGtoBWrG7qrayiN5btCMvKUZFokSXWXxPFaFZflJw%3D%3D%22%7D',
        '_ga_Y07J3B53QP': 'GS1.1.1671707416.2.1.1671707692.47.0.0',
    }

    headers = {
        'authority': 'api2.realtor.ca',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,id;q=0.6,ru;q=0.5,et;q=0.4,de;q=0.3,es;q=0.2',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'visid_incap_2269415=LcnofuD5S9eqfKkjb3ezKZIdpGMAAAAAQUIPAAAAAABcYK8lS17cOYeVpZQIwCqf; nlbi_2269415=Ol29BWgZwmQD9r8uzBLR3QAAAADL0H5S31Qfzv7C9u8hEBWh; _gcl_au=1.1.1134938651.1671699861; _gid=GA1.2.5995056.1671699861; ASP.NET_SessionId=asjnxpq1dqowglg43uvrckrm; visid_incap_2271082=4Omt0GzIQpCcJ+A1xxbyeJQdpGMAAAAAQUIPAAAAAACwIx84Ga4AzSW9shuioHUx; nlbi_2271082=iOP/ZEAz3Gi5BfZHVPrQ3QAAAAAGS9UkCRK/7Ttw8Ep20aDG; gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko=gigya-pr_ver4; nlbi_2271082_2147483392=yRVHBWIzpS6fLqgfVPrQ3QAAAACX6qPRHLi4yzbpIkJ5A87U; reese84=3:g8eXs6IY/EiUHUKmUD3qNg==:KkB6/GbmFOEJZhMRkhvr7iekr8ck1E0K/Ddq/r7PYkHLJM4bFRZri8pyxA5wsKp3TotS3kxoYRTvLDq4oNA7GKs66kX8p7E7kXSpaTVPiJT6hr9RaW923bHAKAXnyUub0hnYXA8VTI1ROVu5xGYP0Cuj22rceAj09AjBkb4UtCFcU2x8kSrhz8cw+qvVb9jvCwBZAmy+k0iIbddbiCAhkCfxzXfXcUzeywc0gDBfiIWQpqhC1Bpr+EgGvYGuvWxIoCa2i2jPbjGPwwnKfZi0WQnWs2M0wwUCwB5/iFfVzCQjd6O2rNvdMBQ4slq1Stp7+IYKc2DyX4FHhIP6jYyUmsV9zOTEnbzW8vhBH8wlUew6qvsMvxe3hduc5o4IykBqyO+eEjbOreWx50MpxaPXKgLWNWK25HxDiVkunhA/J3xZeOgQsb3V5sj34INhZ00FKQ8Z+n0lXt0pE0kJFHrUHLr4w0M0gxXakSz/qRtrsGE=:AHzWwJznbixqctghyz20PIRJZBorKzA8FPfEqaGZDMY=; incap_ses_1193_2269415=6uAUCwOsfBmWJUUs6GOOEKI0pGMAAAAACOlHNeYN7e5RYlzW9KkTDw==; reese84=3:BCB5kKvdoKYTkXr2ItrgEg==:Imlew4rN+eS40cj5DSnLz5DkvjZDkANLWYrGwaE+mKI3WpHoHNz9pcyHtT2FZYxH1zLZOlKRaW6bt9VqnhPY5ook11s8KLJieumoQOj0/g+2LtmVxGzoT4wAZI9lWR1/jyDH1v7mSea2CxZmByc+ppqThwAHsSkhXKNEZgdSgHuUJY0FscciCVBFI3d5w/BenipXhCf1lGbc64lV9sxJkuLkoBq/DvOu4zulB+GxOsndY+kcVEDuvyWCenKScmjHFVlpvhLlIaGL6YkfUEy4IO+znrfzlV5wBSU4gHtvfQ3y8nJ0GQ6HG53yPUTQ4hHk9AG78YQ4KzR4ef1dGRdhj+U8luMTZM4tdJ60x3alMt+/C59Q2fw4zpCmw1YNYygxnhuL/IdSXNjM0cD/jWn+z32cNPRxeNoDoEZugC8mxBTnoNm1a8eMDB0Uz7lJSWXMeHqT+vb6iFqVtfEQVUWCvxbaLmOkfZju3Vfo6gem25U=:257M9saOx+ynZ+yu9sjKT2JLUtgBaDO2gwxg/JARowA=; nlbi_2269415_2147483392=B3P9P1Xw0ANDPueIzBLR3QAAAAABEqSGZ8Zwt0/bAVenmn67; _dc_gtm_UA-12908513-11=1; _ga=GA1.1.1584617771.1671699861; incap_ses_1193_2271082=5T9bUepvUTy9X0Ys6GOOECI8pGMAAAAAMEMOOe76M5YfsDLZ8efNkA==; _4c_=%7B%22_4c_s_%22%3A%22lZLNrpswEIVfJfIaR3YwNs6uSqXqSq1UVe06AnsAKwQj44TeRrx7x9yk6c%2BqLGD8eebYzJkbmTsYyJ5LxRVTUnNVioyc4HUi%2BxsJzqbPlexJYa0o9K6mLGecCtVYqplmVBUGbF5yZXhOMvJ91dJCFaXkSqglI2a8a9yI8RZQi%2BstF1vOaDNhSfyRUMkwHIO3FxOP8XVMeTPUm8mecMPC1Rk4zs7GLmULxZ60A9d2EbEuZKJjwHiH0ewG6%2Be%2Fq%2B70V5USAmkd%2FDxBqjx0wZ9hw1mJ2GMfyKfKYBiggRDWFFxNLqYrBqj66MPWVHeGrXtiuuKP1dBeqnb987T0bQt284JtJ03VT4Dsc%2FBXNxh40z74yxBD0vl6CUkwI19gchaG6Kreh4M%2FnyE4U%2FW%2FSYzJpWRB73EjKaGxGb4SH4PF%2BMO747eX9%2BkaRSnQHqX4NjkvtUa3yPKwj6OBDDMEjkKMeEgpBUvP8nbM6mb%2BZ3Yu8%2FzfbAvTKfqRPvoBw%2F%2FVX91j%2FkoNIKvGUABbUyGtoBWrG7qrayiN5btCMvKUZFokSXWXxPFaFZflJw%3D%3D%22%7D; _ga_Y07J3B53QP=GS1.1.1671707416.2.1.1671707692.47.0.0',
        'origin': 'https://www.realtor.ca',
        'referer': 'https://www.realtor.ca/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    data = {
        'ZoomLevel': '14',
        'LatitudeMax': '49.30344',
        'LongitudeMax': '-123.07101',
        'LatitudeMin': '49.26968',
        'LongitudeMin': '-123.16980',
        'Sort': '6-D',
        'PropertyTypeGroupID': '1',
        'PropertySearchTypeId': '0',
        'TransactionTypeId': '3',
        'RentMin': '4000',
        'RentMax': '4600',
        'BedRange': '2-0',
        'Currency': 'CAD',
        'RecordsPerPage': '12',
        'ApplicationId': '1',
        'CultureId': '1',
        'Version': '7.0',
        'CurrentPage': '1',
    }

    response = requests.post('https://api2.realtor.ca/Listing.svc/PropertySearch_Post', cookies=cookies, headers=headers, data=data)
    results = json.loads(response.content)['Results']

    ret = []

    LOG.debug(results)

    for res in results:
        id = res["Id"]
        rent = res["Property"]["LeaseRent"]
        address = res["Property"]["Address"]["AddressText"]
        ret.append({ 
            'id': id,
            'address' : address,
            'rent': rent,
            'link': 'https://www.realtor.ca/' + res["RelativeURLEn"]
        })
    
    return ret


def render_html(listings):
    today = date.today().strftime("%B %d, %Y")

    str_listings = []
    for listing in listings:
        rend = f"""
            <div>
                <a href="{listing['link']}" target="_blank">[{listing['rent']}] - {listing['address']}</a>
            </div>
        """
        str_listings.append(rend)
    rend_listings = "".join(str_listings)

    html_output = f"""
        <html>
            <head><title>Evler</title></head>
            <body>
                <h3>Tarama Tarihi: {today}</h3>
                {rend_listings}
            </body>
        </html>
    """

    return html_output


def handler(event, context):
    bucket = os.environ.get('bucket')

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(bucket)

    try:
        listings = get_linstings()

        table.put_item(Item={
            'createTime': time.time_ns(),
            'listings': listings
        })

    except Exception as ex:
        LOG.error("Error writing to DynamoDB: " + str(ex))

    try:
        s3 = boto3.client("s3")
        key = f'{date.today().strftime("%b-%d-%Y")}.html'
        
        s3.put_object(
            Body=render_html(listings), 
            Bucket=bucket, 
            Key=key,
            ContentType='text/html'
        )
        public_url = '%s/%s/%s' % (s3.meta.endpoint_url, bucket, key)
        
    except Exception as ex:
        LOG.error("Error writing to S3")

    try:
        sns = boto3.client('sns')
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
