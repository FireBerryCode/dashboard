from app import app, dispositivos_dropdown_list
import base64
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from helpers import colors
from datetime import date


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
            figure=map
        )),
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Div(children=[
                    daq.Gauge(
                        id="tempsensor",
                        color={"gradient": True, "ranges": {
                            "blue": [0, 80], "red":[80, 100]}},
                        value=0,
                        label={"label": "Temperatura", "style": {
                            "color": colors["text"]}},
                        max=100,
                        min=0
                    ),
                ],
                )
                ),
                dbc.Col(html.Div(
                    daq.Gauge(
                        id="humsensor",
                        color={"gradient": True, "ranges": {
                            "blue": [0, 80], "red":[80, 100]}},
                        value=0,
                        label={"label": "Humidade relativa", "style": {
                            "color": colors["text"]}},
                        max=100,
                        min=0
                    ),
                )),

                dbc.Col(html.Div(
                    daq.Gauge(
                        id="gassensor",
                        color={"gradient": True, "ranges": {
                            "blue": [0, 800], "red":[800, 1000]}},
                        value=0,
                        label={"label": "Concentración de gases", "style": {
                            "color": colors["text"]}},
                        max=1000,
                        min=0
                    ),
                ))]),
            dbc.Row([
                dbc.Col(html.Div(
                    daq.Gauge(
                        id="luzsensor",
                        color={"gradient": True, "ranges": {
                            "blue": [0, 800], "red":[800, 1000]}},
                        value=0,
                        label={"label": "Radiación visible", "style": {
                            "color": colors["text"]}},
                        max=1000,
                        min=0
                    ),
                )),
                dbc.Col(html.Div(
                    daq.Gauge(
                        id="rinfsensor",
                        color={"gradient": True, "ranges": {
                            "blue": [0, 800], "red":[800, 1000]}},
                        value=0,
                        label={"label": "Radiación infravermella", "style": {
                            "color": colors["text"]}},
                        max=1000,
                        min=0
                    ),
                )),
                dbc.Col(html.Div(
                    daq.Gauge(
                        id="flamesensor",
                        color={"gradient": True, "ranges": {
                            "blue": [0, 800], "red":[800, 1000]}},
                        value=0,
                        label={"label": "Sensor de lume", "style": {
                            "color": colors["text"]}},
                        max=1000,
                        min=0
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
    dbc.Jumbotron([dbc.Row([
            daq.NumericInput(
                id='alarm_temp',
                min=0,
                max=100,
                value=0,
                size=120,
                label={"label": "Temperatura",
                       "style": {"color": colors["text"]}},
                style={"margin-right": "5em"}
            ),
            daq.NumericInput(
            id='alarm_hum',
            min=0,
            max=100,
            value=0,
            size=120,
            label={"label": "Humidade relativa",
                   "style": {"color": colors["text"]}},
            style={"margin-right": "5em"}
        ),
        daq.NumericInput(
            id='alarm_gas',
            min=0,
            max=10,
            value=8,
            size=120,
            label={"label": "Concentración de gases",
                   "style": {"color": colors["text"]}},
            style={"margin-right": "5em"}
        ),
        daq.NumericInput(
            id='alarm_luz',
            min=0,
            max=10,
            value=8,
            size=120,
            label={"label": "Radiación visible",
                   "style": {"color": colors["text"]}},
            style={"margin-right": "5em"}
        ),
        daq.NumericInput(
                id='alarm_rinf',
                min=0,
                max=10,
                value=8,
                size=120,
                label={"label": "Radiación infraveermella",
                       "style": {"color": colors["text"]}},
                style={"margin-right": "5em"}
            ),
            daq.NumericInput(
                id='alarm_flame',
                min=0,
                max=10,
                value=8,
                size=120,
                label={"label": "Sensor de lume",
                       "style": {"color": colors["text"]}},
                style={"margin-right": "5em"}
            )], justify="center")]),
    dcc.Dropdown(
        id="dispositivo-alertas",
        options=dispositivos_dropdown_list,
        placeholder='Seleccione un punto de medida',
        style=dict(
            width='60%',
            display='inline-block',
            verticalAlign="middle",
        )
    ),
    html.Br(),
    html.Br(),
    html.Button('Establecer alertas', id='actualizar-alertas',
                n_clicks=0, type='submit', className='btn btn-primary btn-lg',
                style={"margin-right": "2em"}),
    html.Button('Comprobar alertas', id='comprobar-alertas',
                n_clicks=0, type='submit', className='btn btn-primary btn-lg',),
    html.Br(),
    html.Br(),
    html.Div(id='updatesuccess',
        style={
            "color": colors["text"]
        })

])

historico = html.Div([
    html.Div(
        html.Img(src=svg, width="500"), style={"textAlign": "center"}),

    html.Div(
        children="Histórico de datos",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),
    html.Hr(),
    html.Div([
        dcc.DatePickerRange(
            id="rango-historico",
            end_date=date.today(),
            display_format='MM Do, YY',
            start_date_placeholder_text='Do MMM, YY',
            style={'margin-right': '2em',
                   "margin-left": "2em"}
        ),
        dcc.Dropdown(
            id="dispositivo-historico",
            options=dispositivos_dropdown_list,
            placeholder='Seleccione un punto de medida',
            style=dict(
                width='40%',
                display='inline-block',
                verticalAlign="middle",
            )
        ),
        html.Button('Consultar', id='consultar-historico', n_clicks=0, className='btn btn-primary btn-lg'),
    ], style=dict(display='flex')),
    html.Br(),
    dcc.Tabs(id='tabs-historico', value='tab-temp', children=[
        dcc.Tab(label='Temperatura', value='tab-temp'),
        dcc.Tab(label='Humidade relativa', value='tab-hum'),
        dcc.Tab(label="Concentración de gases", value="tab-gas"),
        dcc.Tab(label="Radiación visible", value="tab-luz"),
        dcc.Tab(label="Radiación infravermella", value="tab-rinf"),
        dcc.Tab(label="Sensor de lume", value="tab-flame")
    ]),
    html.Div(id="grafico-hist"),
    # dcc.Graph(
    #     id="grafico-hist",
    #     animate=True
    # ),
    html.Div(id='datos-historico', style={'display': 'none'})

])

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
                ),
                dbc.NavLink(
                    [html.Span("Historico")],
                    href="/historico",
                    active="exact",
                )
            ],
            vertical=True,
            pills=True
        ),
        html.Div([dcc.Link("Cerrar sesión", href="/logout"),
                  html.Br(), html.Br()], className="sidebar-footer")
    ],
    className="sidebar"
)

mapa = html.Div([html.Div(
    html.Img(src=svg, width="500"), style={"textAlign": "center"}),

    html.Div(
        children="Mapa",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }),
    html.Hr(),
    dcc.Graph(
    # px.scatter_mapbox(lat=["42.2512652"], lon=["-7.0271794"], zoom= 12,mapbox_style="stamen-terrain")
    figure=big_map,
    responsive=True,
    style={
        "height": 900
    }
)])

login = dbc.Container([dcc.Location(id='url_login', refresh=True),
                       html.Br(),
                       dbc.Container([
                           html.Div([
                               dbc.Container(
                                   html.Img(
                                       src=svg,
                                       className='center'
                                   ),
                               ),
                               dbc.Container(children=[
                                   dcc.Input(
                                       placeholder='Introduza o seu nome de usuario',
                                       type='text',
                                       id='usernamelogin',
                                       className='form-control',
                                       n_submit=0,
                                   ),
                                   html.Br(),
                                   dcc.Input(
                                       placeholder='Introduza o seu contrasinal',
                                       type='password',
                                       id='passwordlogin',
                                       className='form-control',
                                       n_submit=0,
                                   ),
                                   html.Br(),
                                   html.Button(
                                       children='Iniciar sesión',
                                       n_clicks=0,
                                       type='submit',
                                       id='loginbutton',
                                       className='btn btn-primary btn-lg'
                                   ),
                                   html.Br(),
                                   html.Br(),
                                   dcc.Link(
                                       'Se non ten usuario prema aquí para rexistrarse', href='/register')
                               ], className='form-group'),
                           ]),
                       ]),
                       ], className='jumbotron')

register = dbc.Container([
    html.Br(),
    dbc.Container([
        html.Div([
            dbc.Container([
                html.Img(
                    src=svg,
                    className='center'
                ),
                html.Div(
                    children="Rexistro de usuario",
                    style={
                        "textAlign": "center",
                        "color": colors["text"]
                    }
                ),
                html.Br(), html.Br()]
            ),
            dbc.Container(children=[
                dbc.Row([dbc.Col(
                    dcc.Input(
                        placeholder='Introduza un nome de usuario',
                        type='text',
                        id='registerusername',
                        className='form-control',
                        n_submit=0,
                    )), dbc.Col(
                    dcc.Input(
                        placeholder='Introduza un correo electrónico',
                        type='text',
                        id='registeremail',
                        className='form-control',
                        n_submit=0,
                    ))]),
                html.Br(),
                dbc.Row([dbc.Col(
                    dcc.Input(
                        placeholder='Introduza un contrasinal',
                        type='password',
                        id='registerpassword',
                        className='form-control',
                        n_submit=0,
                    )), dbc.Col(
                    dcc.Input(
                        placeholder='Repita o contrasinal',
                        type='password',
                        id='registerpassword2',
                        className='form-control',
                        n_submit=0,
                    ))]),
                html.Br(),
                html.Button(
                    children='Rexistrarse',
                    n_clicks=0,
                    type='submit',
                    id='registerbutton',
                    className='btn btn-primary btn-lg'
                ),
                html.Br(),
                html.Div(id='registersuccess')
            ], className='form-group',),
        ]),
    ]),
], className='jumbotron')


logout = dbc.Container([
    html.Br(),
    dbc.Container([
        html.Div([
            dbc.Container([
                html.Img(
                    src=svg,
                    className='center'
                ),
                html.Div(
                    children="Sesión cerrada.",
                    style={
                        "textAlign": "center",
                        "color": colors["text"]
                    }
                ),
                html.Br(),
                html.Br(),
                dcc.Link("Se desexa iniciar sesión prema aquí.", href="/login")
            ]
            ),
        ]),
    ]),
], className='jumbotron')
