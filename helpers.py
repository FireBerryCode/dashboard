from app import app
from google.cloud import pubsub
import json
from datetime import datetime
import pandas as pd

from google.cloud import ndb


def get_events():
    subscriber = pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        "gold-braid-297420", "temp_graph")

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 10
        }
    )

    data_list = []
    for msg in response.received_messages:
        print(msg.message.data)
        datos = json.loads(msg.message.data)
        datos["timestamp"] = datetime.strptime(
            datos["timestamp"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
        data_list.append(datos)

    ack_ids = [msg.ack_id for msg in response.received_messages]
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": ack_ids,
        }
    )
    return pd.DataFrame(data_list)


colors = {
    "background": "#FDFFFC",
    "text": "#2E6171",
    "other": "#DE6449"}


class Alertas(ndb.Model):
    usuario = ndb.StringProperty()
    id_dispositivo = ndb.IntegerProperty()
    temp = ndb.IntegerProperty()
    hum = ndb.IntegerProperty()
    gas = ndb.IntegerProperty()
    luz = ndb.IntegerProperty()
    rinf = ndb.IntegerProperty()
    flame = ndb.IntegerProperty()