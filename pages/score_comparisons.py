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

col_names = ['Date','Player','Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']
df.columns = col_names

categories = ['Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']
 

# app = Dash(__name__)
layout = html.Div([
    html.H1("Player Score Ratios"),
    html.P('Select two score categories.  The graph below will display the ratio of those scores.'),
    html.Div([
        html.Label([
            "First Score",
            dcc.Dropdown(
                id='score1', clearable=False,
                value='Wonder Orbs', options=[
                    {'label': c, 'value': c}
                    for c in categories
                ])
        ], style={"width":"25%"}),
        html.Label([
            "Second Score",
            dcc.Dropdown(
                id='score2', clearable=False,
                value='RP Spent', options=[
                    {'label': c, 'value': c}
                    for c in categories
                ])
        ], style={"width":"25%"})
        
    ]
    ),
    html.Div([
        html.Label([
            "Sort By",
            dcc.RadioItems(
                id='sort_order', 
                value='Rank', options=[
                    {'label': c, 'value': c}
                    for c in ["Rank","Player","Ratio"]
                ])
        ])
    ]),
    dcc.Graph(id='score_comp')
],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})

# Define callback to update graph
@callback(
    Output('score_comp', 'figure'),
    [Input("score1", "value"), Input("score2","value"), Input("sort_order","value")]
)

def score_comp_fig(score1,score2,sort_order="Rank"):

    score1_df = df.loc[df.Date == df.Date.max(), ['Date','Player','Rank',score1]]
    score2_df = df.loc[df.Date == df.Date.max(), ['Date','Player','Rank',score2]]

    new_df = pd.merge(score1_df,score2_df,how="left", on=["Player","Date","Rank"])
    new_df['score_comp'] = new_df[score1] / new_df[score2]
    new_df['score_comp'] = new_df['score_comp'].map("{:,.4f}".format)
    new_df['score_comp'] = new_df['score_comp'].astype('float')

    if sort_order == "Ratio":
        sorted_df = new_df.sort_values('score_comp',ascending=False)
    else:
        sorted_df = new_df.sort_values(sort_order)

    # latest_df = sorted_df.loc[sorted_df.Date == sorted_df.Date.max(),['Date','Player',dropdown]]
    # avg_value = df.loc[df.Date == df.Date.max(),dropdown].mean()
    # formatted_value = "{:,.2f}".format(avg_value)
    fig = px.bar(
        sorted_df, x="Player", y="score_comp",
        title=f"Player {score1} per {score2} As Of {df.Date.max().strftime('%m/%d/%Y')}",
        labels={'score_comp':'Score Ratio'}
        
    )
    # fig.add_hline(y=avg_value,line_dash="dot",annotation_text=f"<b>Average: {formatted_value}</b>",annotation_position="bottom left")
    fig.update_traces(marker_color="lightseagreen")
    return fig

# if __name__ == '__main__':
#     app.run(debug=True)