import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from layouts import layout, sidebar
import callbacks
from helpers import colors


app.layout = html.Div(
    style={"backgroundColor": colors["background"]}, children=[sidebar, layout])

# @app.callback(Output('page-content', 'children'),
#               Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == '/apps/app1':
#          return layout1
#     elif pathname == '/apps/app2':
#          return layout2
#     else:
#         return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
