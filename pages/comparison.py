import pandas as pd
import dash_bootstrap_components as dbc
import dash
from dash import Dash, html, Input, Output, dash_table, dcc, callback
from dash.dash_table.Format import Format, Group
import plotly.express as px
import datetime as dt


dash.register_page(__name__)

df = pd.read_csv("assets/ROC_player_scores.csv", thousands=',')
df.date = pd.to_datetime(df['date']).dt.date

col_names = ['Date','Player','Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']
df.columns = col_names

categories = ['Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']

dates = [dt.datetime.strftime(each,'%m-%d-%Y') for each in df[['Date']].sort_values('Date',ascending=False)['Date'].unique()]
min_date = df.Date.min().strftime('%m-%d-%Y')
max_date = df.Date.max().strftime('%m-%d-%Y')

table_columns = [
                 {'name':'Player', 'id':'Player', 'type':'text'},
                 {'name':'Rank', 'id':'Rank', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Total', 'id':'Total', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'RP Spent', 'id':'RP Spent', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Battles', 'id':'Battles', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Negotiations', 'id':'Negotiations', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Traded Goods', 'id':'Traded Goods', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Wonder Orbs', 'id':'Wonder Orbs', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Activity Points', 'id':'Activity Points', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Events', 'id':'Events', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'Compass Donations', 'id':'Compass Donations', 'type':'numeric', 'format':Format().group(True)},
                 {'name':'TH Encounters', 'id':'TH Encounters', 'type':'numeric', 'format':Format().group(True)}
                 ]


# app = Dash(__name__)
layout = html.Div([
    html.H1('Comparison View'),
    html.P('Enter in a start date and an end date.  The table below will calculate the difference between scores from the selected dates.  The default is the first week for the start date and the most recent week for the end date.'),
    html.P(id='table'),
    html.Label([
            "Start Date",
            dcc.Dropdown(
                id='start_date', clearable=False,
                value=min_date, options=[
                    {'label': d, 'value': d}
                    for d in dates
                ])
                ], style={"width":"25%"}),
    html.Label([
            "End Date",
            dcc.Dropdown(
                id='end_date', clearable=False,
                value=max_date, options=[
                    {'label': d, 'value': d}
                    for d in dates
                ])
                ], style={"width":"25%"}),
    dash_table.DataTable(
        id='table',

        columns=table_columns,
        data=df.to_dict('records'),
        editable=True,
        sort_action="native",
        filter_action="native",
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ), 
],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})

@callback(
    Output('table', 'data'),
    [Input("start_date", "value")
     , Input("end_date","value")
     ]
)

def update_table(start_date=min_date,end_date=max_date):
    first_df = df.loc[df.Date == dt.datetime.strptime(start_date,'%m-%d-%Y').date()].set_index('Player').drop("Date",axis=1)
    second_df = df.loc[df.Date == dt.datetime.strptime(end_date,'%m-%d-%Y').date()].set_index('Player').drop("Date",axis=1)
    diff_df = second_df - first_df
    diff_df = diff_df.reset_index()

    return diff_df.to_dict('records')