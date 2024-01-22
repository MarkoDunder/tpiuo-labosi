"""
Module: RedditProducer.py

This module contains the implementation of a Reddit posts consumer.

Author: Marko Dundjer
"""

import json
from azure.eventhub import EventHubConsumerClient


EVENT_HUB_CONNECTION_STRING = (
    'Endpoint=sb://markodeventhub.servicebus.windows.net/;'
    'SharedAccessKeyName=RootManageSharedAccessKey;'
    'SharedAccessKey=Wgr4VUaaDccVICrXWOQRTo2Bz+Yq+FjdG+AEhPGcaNQ='
)
EVENT_HUB_NAME = 'mdreddithub'
CONSUMER_GROUP = '$Default'

def on_event(partition_context, event):
    """ Defines what happens when consumer receives posts"""
    try:
        # Handle the event
        body = json.loads(event.body_as_str())
        print("Received event from partition: {}".format(partition_context.partition_id))
        print(f"Data: {body}")
    except ValueError as value_error:
        print("Error processing Event Hubs event:", str(value_error))

consumer_client = EventHubConsumerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STRING,
    consumer_group=CONSUMER_GROUP,
    eventhub_name=EVENT_HUB_NAME
)

try:
    with consumer_client:
        consumer_client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )
except KeyboardInterrupt:
    print("Receiving has stopped.")
