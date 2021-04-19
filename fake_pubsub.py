from google.cloud import pubsub
from time import sleep
from random import randint
import json
from datetime import datetime


publisher = pubsub.PublisherClient()

topic = "projects/gold-braid-297420/topics/gateway-telemetry"

while True:

    payload = json.dumps({"timestamp": datetime.now().isoformat(), "temp": randint(0, 10), "hum": randint(
        0, 10), "gas": randint(0, 10), "luz": randint(0, 10), "rinf": randint(0, 10), "flame": randint(0, 10)}).encode("utf-8")

    print("""
    ------------------
    Publicando mensaje
    ------------------
    """, payload)

    publisher.publish(topic, payload)
    sleep(4)
