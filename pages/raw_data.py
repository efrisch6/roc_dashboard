import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dash_table, dcc, callback
from dash.dash_table.Format import Format, Group
import plotly.express as px
import datetime as dt

dash.register_page(__name__)

df = pd.read_csv("assets/ROC_player_scores.csv", thousands=',')
df.date = pd.to_datetime(df['date']).dt.date

col_names = ['Date','Player','Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events']
df.columns = col_names

categories = ['Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events']
 
table_columns = [{'name':'Date', 'id':'Date', 'type':'datetime'},
                 {'name':'Player', 'id':'Player', 'type':'text'},
                 {'name':'Rank', 'id':'Rank', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Total', 'id':'Total', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'RP Spent', 'id':'RP Spent', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Battles', 'id':'Battles', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Negotiations', 'id':'Negotiations', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Traded Goods', 'id':'Traded Goods', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Wonder Orbs', 'id':'Wonder Orbs', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Activity Points', 'id':'Activity Points', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Events', 'id':'Events', 'type':'numeric', 'format':Format().group(True)}]


# app = Dash(__name__)
layout = html.Div([
    html.H1('Raw Data Table'),
    html.P(id='table_out'),
    dash_table.DataTable(
        id='table',

        columns=table_columns,
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ), 
],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})

@callback(
    Output('table_out', 'children'), 
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell:
        cell_data = df.iloc[active_cell['row']][active_cell['column_id']]
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    return "Click the table"

# if __name__ == '__main__':
#     app.run(debug=True)
