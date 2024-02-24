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

col_names = ['Date','Player','Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events']
df.columns = col_names

max_df = df.loc[df.Date == df.Date.max()].set_index('Player').drop("Date",axis=1)
remaining = df.loc[df.Date != df.Date.max()]
second_df = remaining.loc[remaining.Date == remaining.Date.max()].set_index('Player').drop("Date",axis=1)

diff_df = max_df - second_df

rp_reward = diff_df[["RP Spent"]].sort_values("RP Spent",ascending=False).reset_index().head(3)
orb_reward = diff_df[["Wonder Orbs"]].sort_values("Wonder Orbs",ascending=False).reset_index().head(3)
activity_reward = diff_df[["Activity Points"]].sort_values("Activity Points",ascending=False).reset_index().head(3)

layout = html.Div([
   html.H1(f"Rewards for {df.Date.max().strftime('%m/%d/%Y')}"),
   dbc.Row([
    dbc.Col(
        dbc.Card([
            dbc.CardHeader("RP Spent"),
            dbc.CardBody([
                # html.H4("Activity Points", className="card-title"),
                dbc.Table.from_dataframe(rp_reward, bordered=True, hover=True)
            ])
        ],
        outline=True
        ),    
        width="auto", 
    ),
    dbc.Col(
       dbc.Card([
            dbc.CardHeader("Wonder POrbs"),
            dbc.CardBody([
                # html.H4("Activity Points", className="card-title"),
                dbc.Table.from_dataframe(orb_reward, bordered=True, hover=True)
            ])
        ],
        outline=True
        ),
            
        width="auto", 
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardHeader("Activity Points"),
            dbc.CardBody([
                # html.H4("Activity Points", className="card-title"),
                dbc.Table.from_dataframe(activity_reward, bordered=True, hover=True)
            ])
        ],
        outline=True
        ),
            
        width="auto", 
    )
])
],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})