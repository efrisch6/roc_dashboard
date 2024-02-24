import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dash_table, dcc
from dash.dash_table.Format import Format, Group
import plotly.express as px
import datetime as dt

app = Dash(__name__, 
            use_pages=True, 
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )

server = app.server

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(f"{page['name']}", href=page["relative_path"]
                                        ) for page in dash.page_registry.values()
                ],
                nav=True,
                in_navbar=True,
                label="Menu",
            ),
        ],
        brand="RagnOroCK Player Analytics",
        brand_href="/",
        color="secondary",
        dark=True
        
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
