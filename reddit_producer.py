"""
Module: RedditProducer.py

This module contains the implementation of a Reddit producer.

Author: Marko Dundjer
"""

import json
from time import sleep
from azure.eventhub import EventHubProducerClient, EventData
import requests

EVENT_HUB_CONNECTION_STRING = (
    'Endpoint=sb://markodeventhub.servicebus.windows.net/;'
    'SharedAccessKeyName=RootManageSharedAccessKey;'
    'SharedAccessKey=Wgr4VUaaDccVICrXWOQRTo2Bz+Yq+FjdG+AEhPGcaNQ='
)
EVENT_HUB_NAME = 'mdreddithub'

PRODUCER = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STRING,
    eventhub_name=EVENT_HUB_NAME
)

def send_to_event_hub(data):
    """Adds a batch of event data"""
    with PRODUCER:
        batch = PRODUCER.create_batch()
        batch.add(EventData(body=json.dumps(data)))
        PRODUCER.send_batch(batch)

def main():
    """Sends data to event hub after parsing from reddit API"""
    while True:
        try:
            subreddit_url = 'https://www.reddit.com/r/dataengineering/top/.json?t=all&limit=1'
            response = requests.get(subreddit_url, timeout = 10)
            response_data = response.json()
            print('Raw API Response:', response_data)

            posts = response_data.get('data', {}).get('children', [])
            print('Extracted Posts:', posts)

            for post in posts:
                post_data = post['data']
                image_url = post_data.get('url_overridden_by_dest', '')
                post_data['image_url'] = image_url
                send_to_event_hub(post_data)
            print('Data sent to Event Hub:', posts)
        except requests.RequestException as error:
            print('Error fetching or sending data:', str(error))
        sleep(20000)  # 20 seconds

if __name__ == "__main__":
    main()
