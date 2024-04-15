import pandas as pd
import dash_bootstrap_components as dbc
import dash
from dash import Dash, html, Input, Output, dash_table, dcc, callback
from dash.dash_table.Format import Format, Group
from dash.dash_table import DataTable, FormatTemplate
import plotly.express as px
import datetime as dt


dash.register_page(__name__,
            meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                    )

image_path = 'assets/ROC_score_breakdown.jpg'
df = pd.read_csv("assets/ROC_player_scores.csv", thousands=',')
df.date = pd.to_datetime(df['date']).dt.date

df = df.loc[df.date == df.date.max()]

df = df.rename(columns=lambda x: x.strip())

df['calc_rp'] = df['rp_spent'] * 0.25
df['calc_battles'] = df['battles'] * 2
df['calc_neg'] = df['negotiations'] * 2
df['calc_trade'] = df['traded_goods'] * 0.002
df['calc_orbs'] = df['wonder_orbs'] * 5
df['calc_activity'] = df['activity_points'] * 0.1
df['calc_event'] = df['events'] * 1

df['calc_score'] = df['calc_rp'] + df['calc_battles'] + df['calc_neg'] + df['calc_trade'] + df['calc_orbs'] + df['calc_activity'] + df['calc_event']

df['RP Spent'] = df['calc_rp'] / df['calc_score'] 
df['Battles'] = df['calc_battles'] / df['calc_score']
df['Negotiations'] = df['calc_neg'] / df['calc_score']
df['Traded Goods'] = df['calc_trade'] / df['calc_score']
df['Wonder Orbs'] = df['calc_orbs'] / df['calc_score']
df['Activity Points'] = df['calc_activity'] / df['calc_score']
df['Events'] = df['calc_event'] / df['calc_score']

percent_df = df[['player','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events']]

percent_df = percent_df.rename(columns={'player':'Player'})
percent_df = percent_df.sort_values('Player')

percentage = FormatTemplate.percentage(2)

table_columns = [{'name':'Player', 'id':'Player', 'type':'text'},
                 {'name':'RP Spent', 'id':'RP Spent', 'type':'numeric', 'format':percentage},
                 {'name':'Battles', 'id':'Battles', 'type':'numeric', 'format':percentage},
                 {'name':'Negotiations', 'id':'Negotiations', 'type':'numeric', 'format':percentage},
                 {'name':'Traded Goods', 'id':'Traded Goods', 'type':'numeric', 'format':percentage},
                 {'name':'Wonder Orbs', 'id':'Wonder Orbs', 'type':'numeric', 'format':percentage},
                 {'name':'Activity Points', 'id':'Activity Points', 'type':'numeric', 'format':percentage},
                 {'name':'Events', 'id':'Events', 'type':'numeric', 'format':percentage}]


layout = html.Div([
    html.P("The table contains the percentage that each profile score category makes up of a player's total score."),
    dbc.Row([
        dbc.Col(html.Img(src=image_path, style={'height': '100%', 'width': '100%'}),
            # width="3",
            style={"height":"35%"},
            xs=5, sm=5, md=3, lg=3, xl=3
            ),
        dbc.Col(
            dcc.Markdown("""Player scores are calculated using the formula below:  
            **Wonder Orbs:** x5  
            **Battles Won:** x2  
            **Negotiations Won:** x2  
            **Event Progress:** x1  
            **RP Spent:** x0.25  
            **Activity Points gained:** x0.1  
            **Traded Goods:** x0.002
            """),
            # width=3
            xs=7, sm=7, md=3, lg=3, xl=3
            )
        ],   
        style={'margin': 25}),
    # dbc.Row([
    #     dbc.Col(dbc.Table.from_dataframe(percent_df, bordered=True, hover=True),
    #     width="auto")
        
    # ])
    dbc.Row([
        dash_table.DataTable(
            id='table',

            columns=table_columns,
            data=percent_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'height': 'auto',
                'minWidth': '80px', 'width': '80px', 'maxWidth': '80px',
                'whiteSpace': 'normal'
    }
        )
    ])
    
],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})
