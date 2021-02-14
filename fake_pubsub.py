from google.cloud import pubsub
from time import sleep
from random import randint
import json
from datetime import datetime


publisher = pubsub.PublisherClient()

topic = "projects/gold-braid-297420/topics/gateway-telemetry"

while True:

    payload = json.dumps({"timestamp": datetime.now().isoformat(), "temperatura": randint(0, 10), "humedad": randint(
        0, 10), "mq7": randint(0, 10), "mq2": randint(0, 10), "llama": randint(0, 10), "tsl": randint(0, 10)}).encode("utf-8")

    print("""
    ------------------
    Publicando mensaje
    ------------------
    """, payload)

    publisher.publish(topic, payload)
    sleep(4)
