import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from layouts import monitorizacion, alertas, mapa, sidebar
import callbacks
from helpers import colors

content = html.Div(id="page-content", className="content")
app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[dcc.Location(id="url"), sidebar, content])
app.config.suppress_callback_exceptions = True

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return monitorizacion
    elif pathname == "/alarmas":
        return alertas
    elif pathname == "/mapa":
        return mapa
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
