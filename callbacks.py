from app import app, Users, Users_tbl, engine, datastore_client
from collections import deque
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
from helpers import get_events, Alertas
import plotly.graph_objects as go
import plotly.express as px
from helpers import colors
from werkzeug.security import generate_password_hash, check_password_hash
import dash_core_components as dcc
import dash_html_components as html
from flask_login import login_user, current_user
import pandas as pd

X = deque(maxlen=15)
T = deque(maxlen=15)
H = deque(maxlen=15)
GAS = deque(maxlen=15)
LUZ = deque(maxlen=15)
RINF = deque(maxlen=15)
FLAME = deque(maxlen=15)


@app.callback(
    Output("grafico-temperatura", "figure"),
    Output("tempsensor", "value"),
    Output("humsensor", "value"),
    Output("gassensor", "value"),
    Output("luzsensor", "value"),
    Output("rinfsensor", "value"),
    Output("flamesensor", "value"),
    [Input("interval-component", "n_intervals")])
def update_temp_graph(n):

    df = get_events()

    values = df.mean(0)

    X.extend(df["timestamp"].tolist())
    T.extend(df["temp"].tolist())
    H.extend(df["hum"].tolist())
    GAS.extend(df["gas"].tolist())
    LUZ.extend(df["luz"].tolist())
    RINF.extend(df["rinf"].tolist())
    FLAME.extend(df["flame"].tolist())

    temp = [t for _, t in sorted(zip(X, T))]
    hum = [t for _, t in sorted(zip(X, H))]
    gas = [t for _, t in sorted(zip(X, GAS))]
    luz = [t for _, t in sorted(zip(X, LUZ))]
    rinf = [t for _, t in sorted(zip(X, RINF))]
    flame = [t for _, t in sorted(zip(X, FLAME))]
    ts = sorted(X)

    fig = make_subplots(
        rows=3, cols=2,
        shared_xaxes=True,
        vertical_spacing=0.1)

    fig.add_trace(
        go.Scatter(x=ts, y=temp,
                   name="Temperatura"),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=ts, y=hum,
                   name="Humidade"),
        row=2, col=1)

    fig.add_trace(
        go.Scatter(x=ts, y=rinf,
                   name="Radiación infravermella"),
        row=3, col=1)

    fig.add_trace(
        go.Scatter(x=ts, y=gas,
                   name="Concentración de gases"),
        row=1, col=2)

    fig.add_trace(
        go.Scatter(x=ts, y=luz,
                   name="Luminosidade"),
        row=2, col=2)

    fig.add_trace(
        go.Scatter(x=ts, y=flame,
                   name="Sensor de lume"),
        row=3, col=2)

    fig.update_xaxes(range=[min(ts), max(ts)], col=1)
    fig.update_xaxes(range=[min(ts), max(ts)], col=2)
    fig.update_yaxes(range=[min(temp) - 0.1 * (max(temp) - min(temp)),
                            max(temp) + 0.1 * (max(temp) - min(temp))], row=1, col=1)
    fig.update_yaxes(range=[min(gas) - 0.1 * (max(gas) - min(gas)),
                            max(gas) + 0.1 * (max(gas) - min(gas))], row=1, col=2)
    fig.update_yaxes(range=[min(hum) - 0.1 * (max(hum) - min(hum)),
                            max(hum) + 0.1 * (max(hum) - min(hum))], row=2, col=1)
    fig.update_yaxes(range=[min(luz) - 0.1 * (max(luz) - min(luz)),
                            max(luz) + 0.1 * (max(luz) - min(luz))], row=2, col=2)
    fig.update_yaxes(range=[min(rinf) - 0.1 * (max(rinf) - min(rinf)),
                            max(rinf) + 0.1 * (max(rinf) - min(rinf))], row=3, col=1)
    fig.update_yaxes(range=[min(flame) - 0.1 * (max(flame) - min(flame)),
                            max(flame) + 0.1 * (max(flame) - min(flame))], row=3, col=2)

    fig.update_layout(plot_bgcolor=colors["background"],
                      paper_bgcolor=colors['background'], font_color=colors['text'])

    return fig, values["temp"], values["hum"], values["gas"], values["luz"], values["rinf"], values["flame"]


@app.callback(
    Output("datos-historico", "children"),
    Input("consultar-historico", "n_clicks"),
    [State("dispositivo-historico", "value"),
     State("rango-historico", "start_date"),
     State("rango-historico", "end_date")]
)
def get_hist_data(n, device_id, start_date, end_date):

    if device_id:
        sql = f"""
        SELECT *
        FROM `gold-braid-297420.prueba.medidas`
        WHERE timestamp >= "{start_date}"
        AND timestamp <= "{end_date}"
        AND id_dispositivo = {device_id}
        ORDER BY timestamp
        """

        project_id = 'gold-braid-297420'
        df = pd.read_gbq(sql, project_id=project_id, dialect='standard')

        return df.to_json(date_format='iso', orient='split')


@app.callback(Output('grafico-hist', 'children'),
              [Input('tabs-historico', 'value'),
               Input("datos-historico", "children")])
def render_hist_tabs(tab, json_data):
    if json_data:
        df = pd.read_json(json_data, orient='split')

        if tab == "tab-temp":

            fig = px.line(df, x="timestamp", y="temperatura", labels={
                        "timestamp": "Data", "temperatura": "Temperatura"})

            return dcc.Graph(figure=fig)

        elif tab == "tab-hum":

            fig = px.line(df, x="timestamp", y="hum", labels={
                        "timestamp": "Data", "hum": "Humidade relativa"})

            return dcc.Graph(figure=fig)

        elif tab == "tab-gas":

            fig = px.line(df, x="timestamp", y="gas", labels={
                        "timestamp": "Data", "gas": "Concentración de gases"})

            return dcc.Graph(figure=fig)

        elif tab == "tab-luz":

            fig = px.line(df, x="timestamp", y="luz", labels={
                        "timestamp": "Data", "luz": "Radiación visible"})

            return dcc.Graph(figure=fig)

        elif tab == "tab-rinf":

            fig = px.line(df, x="timestamp", y="rinf", labels={
                        "timestamp": "Data", "rinf": "Radiación infravermella"})

            return dcc.Graph(figure=fig)

        elif tab == "tab-flame":

            fig = px.line(df, x="timestamp", y="flame", labels={
                        "timestamp": "Data", "flame": "Sensor de lume"})

            return dcc.Graph(figure=fig)


@app.callback(
    Output("updatesuccess", "children"),
    [Input("actualizar-alertas", "n_clicks")],
    [State("alarm_temp", "value"),
     State("alarm_hum", "value"),
     State("alarm_gas", "value"),
     State("alarm_luz", "value"),
     State("alarm_rinf", "value"),
     State("alarm_flame", "value"),
     State("dispositivo-alertas", "value")]
)
def update_alert(n, temp, hum, gas, luz, rinf, flame, device):
    if device:
        user = current_user.username

        with datastore_client.context():
            alerta = Alertas(
                usuario=user,
                id_dispositivo=device,
                temp=temp,
                hum=hum,
                gas=gas,
                luz=luz,
                rinf=rinf,
                flame=flame)
            alerta.put()
        return("Alarma actualizada con éxito!")

@app.callback(
    [Output("alarm_temp", "value"),
    Output("alarm_hum", "value"),
    Output("alarm_gas", "value"),
    Output("alarm_luz", "value"),
    Output("alarm_rinf", "value"),
    Output("alarm_flame", "value")],
    [Input("comprobar-alertas", "n_clicks")],
    [State("dispositivo-alertas", "value")]
)
def alert_default(n, device):
    if device:
        
        with datastore_client.context():
            value = Alertas.query().filter(Alertas.usuario==current_user.username, Alertas.id_dispositivo==device).fetch()[0]
            return value.temp, value.hum, value.gas, value.luz, value.rinf, value.flame

    else:

        return [0, 0, 0, 0, 0, 0]


@app.callback(
    Output("registersuccess", "children"),
    [Input("registerbutton", "n_clicks")],
    [State("registerusername", "value"),
     State("registerpassword", "value"),
     State("registerpassword2", "value"),
     State("registeremail", "value")]
)
def insert_users(n_clicks, un, pw, pw2, em):
    if pw == pw2:
        hashed_password = generate_password_hash(pw, method='sha256')
        if un is not None and pw is not None and em is not None:
            ins = Users_tbl.insert().values(username=un,
                                            password=hashed_password, email=em)
            conn = engine.connect()
            conn.execute(ins)
            conn.close()
            #Retorno un botón para ir a pantalla del login e un mensaxe de exito
            return (dcc.Link("Rexistro completado, prema aquí para iniciar sesión.", href="/login"))

    else:
        return html.Div("Os contrasinais non coinciden.")


@app.callback(
    Output("url_login", "pathname"),
    [Input("loginbutton", "n_clicks")],
    [State("usernamelogin", "value"),
     State("passwordlogin", "value")]
)
def login(n_clicks, un, pw):
    user = Users.query.filter_by(username=un).first()
    if user:
        if check_password_hash(user.password, pw):
            login_user(user)
            return '/'
        else:
            pass
    else:
        pass
