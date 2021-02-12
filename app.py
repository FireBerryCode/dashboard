# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from google.cloud import pubsub
import json
from collections import deque
from datetime import datetime
import base64

X = deque(maxlen=15)
T = deque(maxlen=15)
H = deque(maxlen=15)
MQ7 = deque(maxlen=15)
MQ2 = deque(maxlen=15)
FL = deque(maxlen=15)
TSL = deque(maxlen=15)

coords = pd.DataFrame(data={"lat": [42.2512652], "lon": [-7.0271794]})

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

external_stylesheets = [dbc.themes.GRID]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


colors = {
    "background": "#FDFFFC",
    "text": "#2E6171",
    "other": "#DE6449"}

map = go.Figure(go.Scattermapbox(
    lat=["42.2512652"], lon=["-7.0271794"],
    marker={"size": 15, "color": colors["text"]})
)
map.update_layout(
    mapbox={"style": "stamen-terrain",
            "zoom": 12,
            "center": go.layout.mapbox.Center(
                lat=42.2512652,
                lon=-7.0271794)},
)

svg_logo = "/home/pablo/Documentos/Fireberry/code/logos/FIREBERRY_LOGO_AZUL_IMAGOTIPO.svg"
encoded = base64.b64encode(open(svg_logo, 'rb').read())
svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())

app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[
    html.Div(
        html.Img(src=svg, width="500"), style={"textAlign": "center"}),

    html.Div(
        children="Panel de monitorización",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),

    dcc.Graph(
        id="grafico-temperatura",
        animate=True
    ),
    html.Div(dbc.Row([
        dbc.Col(dcc.Graph(
            # px.scatter_mapbox(lat=["42.2512652"], lon=["-7.0271794"], zoom= 12,mapbox_style="stamen-terrain")
            figure=map
        )),
        dbc.Col([
            dbc.Row([
        dbc.Col(html.Div(children=[
            daq.Thermometer(
                id='termometro',
                value=0,
                min=0,
                max=100,
                style={
                    'margin-bottom': '5%',
                    "color": colors["text"]},
                color=colors["other"],
                label={"label": "Temperatura",
                       "style": {"color": colors["text"]}},
                showCurrentValue=True,
                units="C"
            ),
        ],
        )
        ),
        dbc.Col(html.Div(
            daq.Gauge(
                id="chamasensor",
                color={"gradient": True, "ranges": {
                    "green": [0, 600], "yellow":[600, 800], "red":[800, 1000]}},
                value=0,
                label={"label": "Chama", "style": {"color": colors["text"]}},
                max=1000,
                min=0
            ),
        )),

        dbc.Col(html.Div(
            daq.Tank(
                id="tslsensor",
                min=0,
                max=20000,
                value=0,
                color=colors["other"],
                label={"label": "Luminosidade",
                       "style": {"color": colors["text"]}},
            ),
        ))]),
        dbc.Row([
        dbc.Col(html.Div(
            daq.LEDDisplay(
                id="humsensor",
                value=0,
                color=colors["other"],
                label={"label": "Humidade", "style": {
                    "color": colors["text"]}},
            ),
        )),
        dbc.Col(html.Div(
            daq.LEDDisplay(
                id="mq7sensor",
                value=0,
                color=colors["other"],
                label={"label": "MQ-7", "style": {"color": colors["text"]}},
            ),
        )),
        dbc.Col(html.Div(
            daq.LEDDisplay(
                id="mq2sensor",
                value=0,
                color=colors["other"],
                label={"label": "MQ-2", "style": {"color": colors["text"]}},
            ),
        ))])]),
    ], justify="end")),



    dcc.Interval(
        id="interval-component",
        interval=10000,
        n_intervals=0
    ),
])


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


@app.callback(
    Output("grafico-temperatura", "figure"),
    Output("termometro", "value"),
    Output("chamasensor", "value"),
    Output("humsensor", "value"),
    Output("mq7sensor", "value"),
    Output("mq2sensor", "value"),
    Output("tslsensor", "value"),
    Input("interval-component", "n_intervals"))
def update_temp_graph(n):

    df = get_events()

    values = df.mean(0)

    X.extend(df["timestamp"].tolist())
    T.extend(df["temperatura"].tolist())
    H.extend(df["humedad"].tolist())
    MQ7.extend(df["mq7"].tolist())
    MQ2.extend(df["mq2"].tolist())
    FL.extend(df["llama"].tolist())
    TSL.extend(df["tsl"].tolist())

    temp = [t for _, t in sorted(zip(X, T))]
    hum = [t for _, t in sorted(zip(X, H))]
    mq7 = [t for _, t in sorted(zip(X, MQ7))]
    mq2 = [t for _, t in sorted(zip(X, MQ2))]
    fl = [t for _, t in sorted(zip(X, FL))]
    tsl = [t for _, t in sorted(zip(X, TSL))]
    ts = sorted(X)

    print("temp", temp)
    print("ts", ts)
    fig = make_subplots(
        rows=3, cols=2,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Temperatura", "MQ-7", "Humidade", "MQ-2", "Chama", "Luminosidade"))

    fig.add_trace(
        go.Scatter(x=ts, y=temp,
                   name="Temperatura"),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=ts, y=hum,
                   name="Humidade"),
        row=2, col=1)

    fig.add_trace(
        go.Scatter(x=ts, y=fl,
                   name="Chama"),
        row=3, col=1)

    fig.add_trace(
        go.Scatter(x=ts, y=mq7,
                   name="MQ-7"),
        row=1, col=2)

    fig.add_trace(
        go.Scatter(x=ts, y=mq2,
                   name="MQ-2"),
        row=2, col=2)

    fig.add_trace(
        go.Scatter(x=ts, y=tsl,
                   name="Luminosidade"),
        row=3, col=2)

    fig.update_xaxes(range=[min(ts), max(ts)], col=1)
    fig.update_xaxes(range=[min(ts), max(ts)], col=2)
    fig.update_yaxes(range=[min(temp) - 0.1 * (max(temp) - min(temp)),
                            max(temp) + 0.1 * (max(temp) - min(temp))], row=1, col=1)
    fig.update_yaxes(range=[min(mq7) - 0.1 * (max(mq7) - min(mq7)),
                            max(mq7) + 0.1 * (max(mq7) - min(mq7))], row=1, col=2)
    fig.update_yaxes(range=[min(hum) - 0.1 * (max(hum) - min(hum)),
                            max(hum) + 0.1 * (max(hum) - min(hum))], row=2, col=1)
    fig.update_yaxes(range=[min(mq2) - 0.1 * (max(mq2) - min(mq2)),
                            max(mq2) + 0.1 * (max(mq2) - min(mq2))], row=2, col=2)
    fig.update_yaxes(range=[min(fl) - 0.1 * (max(fl) - min(fl)),
                            max(fl) + 0.1 * (max(fl) - min(fl))], row=3, col=1)
    fig.update_yaxes(range=[min(tsl) - 0.1 * (max(tsl) - min(tsl)),
                            max(tsl) + 0.1 * (max(tsl) - min(tsl))], row=3, col=2)

    fig.update_layout(plot_bgcolor=colors["background"],
                      paper_bgcolor=colors['background'], font_color=colors['text'])

    return fig, values["temperatura"], values["llama"], round(values["humedad"], 2), round(values["mq7"], 2), round(values["mq2"], 2), values["tsl"]


if __name__ == '__main__':
    app.run_server(debug=True)
