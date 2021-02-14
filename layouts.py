from app import app
import base64
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from helpers import colors


svg_logo = "../logos/FIREBERRY_LOGO_AZUL_IMAGOTIPO.svg"
encoded = base64.b64encode(open(svg_logo, 'rb').read())
svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())


svg_mini_logo = "../logos/FIREBERRY_LOGO_AZUL.svg"
encoded_mini = base64.b64encode(open(svg_mini_logo, 'rb').read())
svg_mini = 'data:image/svg+xml;base64,{}'.format(encoded_mini.decode())


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

big_map = go.Figure(go.Scattermapbox(
    lat=["42.2512652"], lon=["-7.0271794"],
    marker={"size": 15, "color": colors["text"]})
)
big_map.update_layout(
    mapbox={"style": "stamen-terrain",
            "zoom": 12,
            "center": go.layout.mapbox.Center(
                lat=42.2512652,
                lon=-7.0271794)},

)

monitorizacion = html.Div([
    html.Div(
        html.Img(src=svg, width="500"), style={"textAlign": "center"}),

    html.Div(
        children="Panel de monitorización",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),
    html.Hr(),

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
                            colors["text"]: [0, 800], "red":[800, 1000]}},
                        value=0,
                        label={"label": "Chama", "style": {
                            "color": colors["text"]}},
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
                        label={"label": "MQ-7",
                               "style": {"color": colors["text"]}},
                    ),
                )),
                dbc.Col(html.Div(
                    daq.LEDDisplay(
                        id="mq2sensor",
                        value=0,
                        color=colors["other"],
                        label={"label": "MQ-2",
                               "style": {"color": colors["text"]}},
                    ),
                ))])]),
    ], justify="end")),



    dcc.Interval(
        id="interval-component",
        interval=10000,
        n_intervals=0
    ),
])

alertas = html.Div([
    html.Div(
        html.Img(src=svg, width="500"), style={"textAlign": "center"}),

    html.Div(
        children="Alarmas",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),
    html.Hr(),
    dbc.Row([dbc.Col(daq.Knob(
        id='alarm_temp',
        min=0,
        max=10,
        value=8,
        color=colors["other"],
        label={"label": "Temperatura",
               "style": {"color": colors["text"]}}
    )),
        dbc.Col(daq.Knob(
            id='alarm_flame',
            min=0,
            max=10,
            value=8,
            color=colors["other"],
            label={"label": "Chama",
                   "style": {"color": colors["text"]}}
        )),
        dbc.Col(daq.Knob(
            id='alarm_lum',
            min=0,
            max=10,
            value=8,
            color=colors["other"],
            label={"label": "Luminosidade",
                   "style": {"color": colors["text"]}}
        ))]),
    dbc.Row([dbc.Col(daq.Knob(
        id='alarm_hum',
        min=0,
        max=10,
        value=8,
        color=colors["other"],
        label={"label": "Humidade",
               "style": {"color": colors["text"]}}
    )),
        dbc.Col(daq.Knob(
            id='alarm_mq7',
            min=0,
            max=10,
            value=8,
            color=colors["other"],
            label={"label": "MQ-7",
                   "style": {"color": colors["text"]}}
        )),
        dbc.Col(daq.Knob(
            id='alarm_mq2',
            min=0,
            max=10,
            value=8,
            color=colors["other"],
            label={"label": "MQ-2",
                   "style": {"color": colors["text"]}}
        ))])])

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=svg_mini, style={"width": "3rem"}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.Span("Monitorización")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [html.Span("Alarmas")],
                    href="/alarmas",
                    active="exact",
                ),
                dbc.NavLink(
                    [html.Span("Mapa")],
                    href="/mapa",
                    active="exact",
                )
            ],
            vertical=True,
            pills=True
        )
    ],
    className="sidebar",
)

mapa = html.Div([html.Div(
    html.Img(src=svg, width="500"), style={"textAlign": "center"}),

    html.Div(
        children="Mapa",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
),
    html.Hr(),
    dcc.Graph(
    # px.scatter_mapbox(lat=["42.2512652"], lon=["-7.0271794"], zoom= 12,mapbox_style="stamen-terrain")
    figure=big_map,
    responsive=True,
    style={
        "height": 900
    }
)])
