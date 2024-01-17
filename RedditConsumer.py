from azure.eventhub import EventHubConsumerClient
import json

event_hub_connection_string = 'Endpoint=sb://markodeventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Wgr4VUaaDccVICrXWOQRTo2Bz+Yq+FjdG+AEhPGcaNQ='
event_hub_name = 'mdreddithub'
consumer_group = '$Default'

def on_event(partition_context, event):
    try:
        # Handle the event
        body = json.loads(event.body_as_str())
        print("Received event from partition: {}".format(partition_context.partition_id))
        print("Data:", body)
    except Exception as e:
        print("Error processing event:", str(e))

consumer_client = EventHubConsumerClient.from_connection_string(
    conn_str=event_hub_connection_string,
    consumer_group=consumer_group,
    eventhub_name=event_hub_name
)

try:
    with consumer_client:
        consumer_client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )
except KeyboardInterrupt:
    print("Receiving has stopped.")