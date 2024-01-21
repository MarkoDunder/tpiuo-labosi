import json
from time import sleep
from azure.eventhub import EventHubProducerClient, EventData
import requests

event_hub_connection_string = 'Endpoint=sb://markodeventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Wgr4VUaaDccVICrXWOQRTo2Bz+Yq+FjdG+AEhPGcaNQ='
event_hub_name = 'mdreddithub'

producer = EventHubProducerClient.from_connection_string(conn_str=event_hub_connection_string, eventhub_name=event_hub_name)

def send_to_event_hub(data):
    with producer:
        batch = producer.create_batch()
        batch.add(EventData(body=json.dumps(data)))
        producer.send_batch(batch)

def main():
    while True:
        try:
            subreddit_url = 'https://www.reddit.com/r/dataengineering/top/.json?t=all&limit=1'
            response = requests.get(subreddit_url)
            responseData = response.json()
            print('Raw API Response:', responseData)

            posts = responseData.get('data', {}).get('children', [])
            print('Extracted Posts:', posts)

            for post in posts:
                post_data = post['data']
                image_url = post_data.get('url_overridden_by_dest', '')
                post_data['image_url'] = image_url
                send_to_event_hub(post_data)
            print('Data sent to Event Hub:', posts)
        except Exception as error:
            print('Error fetching or sending data:', str(error))
        sleep(20000)  # 20 seconds

if __name__ == "__main__":
    main()