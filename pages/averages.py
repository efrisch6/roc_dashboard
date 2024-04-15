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

df.Date = pd.to_datetime(df.Date)
avg_diff = df.set_index('Date').last('50D').groupby('Player').apply(lambda x: x.diff().mean() * -1).dropna().drop(['Compass Donations','TH Encounters'],axis=1)
avg_th = df.set_index('Date').last('50D').groupby('Player')[['Compass Donations','TH Encounters']].mean().dropna()

final_df = pd.concat([avg_diff,avg_th],axis = 1).round(2)
final_df = final_df.reset_index()

categories = ['Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']

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
    html.H1('Player Average Change (Last 7 weeks)'),
    html.P('Below are the average increases in player profile scores from one week to the next for the last 7 weeks.  For compass donations and TH encounters, this is the average for the last 7 weeks'),
    html.P(id='table'),
    dash_table.DataTable(
        id='table',

        columns=table_columns,
        data=final_df.to_dict('records'),
        editable=True,
        sort_action="native",
        filter_action="native",
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ), 
],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})
