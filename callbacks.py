from app import app
from collections import deque
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
from helpers import get_events
import plotly.graph_objects as go
from helpers import colors


X = deque(maxlen=15)
T = deque(maxlen=15)
H = deque(maxlen=15)
MQ7 = deque(maxlen=15)
MQ2 = deque(maxlen=15)
FL = deque(maxlen=15)
TSL = deque(maxlen=15)


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

