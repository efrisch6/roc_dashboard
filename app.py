import pandas as pd
import dash
from dash import Dash, html, Input, Output, dash_table, dcc
from dash.dash_table.Format import Format, Group
import plotly.express as px
import datetime as dt

app = Dash(__name__, use_pages=True)

server = app.server

app.layout = html.Div([
    html.H1('RagnOroCk Player Statistics Page'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
