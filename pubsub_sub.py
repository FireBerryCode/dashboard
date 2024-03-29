from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import json
import base64

# TODO(developer)
project_id = "gold-braid-297420"
subscription_id = "temp_graph"
# Number of seconds the subscriber should listen for messages
timeout = 10.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f"Received {message}.")
    request = json.loads(message.data)
    print("Tipo:", type(message.data))
    print("data", request)

    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        print("hola", streaming_pull_future.result(timeout=timeout))
    except TimeoutError:
        streaming_pull_future.cancel()

