from time import sleep
from azure.eventhub import EventHubProducerClient, EventData
import requests

event_hub_connection_string = 'Endpoint=sb://labos1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=DxdZ9yHe5YvHje8ZPVIfWiXYyLaqZ9df6+AEhLYgDCc='
event_hub_name = 'redditpostseventhub'

subreddit_url = 'https://www.reddit.com/r/dataengineering/top/.json?t=all&limit=10'
producer = EventHubProducerClient.from_connection_string(conn_str=event_hub_connection_string, eventhub_name=event_hub_name)

def send_to_event_hub(data):
    with producer:
        batch = producer.create_batch()
        batch.add(EventData(body=str(data)))
        producer.send_batch(batch)

def fetch_data():
    try:
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

def main():
    while True:
        fetch_data()
        sleep(20000)  # 5 seconds

if __name__ == "__main__":
    main()