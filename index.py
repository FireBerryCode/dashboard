import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from layouts import monitorizacion, alertas, mapa, login, register, sidebar, logout
import callbacks
from helpers import colors
from flask_login import current_user, logout_user



content = html.Div(id="page-content", className="content")
app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[dcc.Location(id="url"), content])
app.config.suppress_callback_exceptions = True

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        if current_user.is_authenticated:
            return sidebar, monitorizacion
        else:
            return logout

    elif pathname == "/alarmas":
        if current_user.is_authenticated:
            return sidebar, alertas
        else:
            return logout

    elif pathname == "/mapa" and current_user.is_authenticated:
        if current_user.is_authenticated:
            return sidebar, mapa
        else:
            return logout

    elif pathname == "/login":
        return login

    elif pathname == "/register":
        return register
        
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout
        else:
            return logout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Non se atopou o dominio", className="text-danger"),
            html.Hr(),
            html.P(f"A ruta {pathname} non é recoñecida..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
