import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, dash_table, dcc, callback
from dash.dash_table.Format import Format, Group
import plotly.express as px
import datetime as dt

dash.register_page(__name__)

df = pd.read_csv("assets/ROC_player_scores.csv", thousands=',')
df.date = pd.to_datetime(df['date'], format="%m/%d/%y").dt.date

col_names = ['Date','Player','Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']
df.columns = col_names

categories = ['Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']
 

# app = Dash(__name__)
layout = html.Div([
    html.H1("Player Scores By Category"),
    html.P('Select a score category.  The results can be sorted by player ranks, player names, or player scores.  The dotted line represents the average score for the alliance.'),
    html.Div([
        html.Label([
            "Category",
            dcc.Dropdown(
                id='dropdown', clearable=False,
                value='Total', options=[
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
                id='buttons', 
                value='Rank', options=[
                    {'label': c, 'value': c}
                    for c in ["Rank","Player","Score"]
                ])
        ])
    ]),
    dcc.Graph(id='averages_by_cat')
],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})

# Define callback to update graph
@callback(
    Output('averages_by_cat', 'figure'),
    [Input("dropdown", "value"), Input("buttons","value")]
)

def update_figure(dropdown="Total",buttons="Rank"):
    if buttons == "Score":
        sorted_df = df.sort_values(dropdown,ascending=False)
    else:
        sorted_df = df.sort_values(buttons)
    latest_df = sorted_df.loc[sorted_df.Date == sorted_df.Date.max(),['Date','Player',dropdown]]
    avg_value = df.loc[df.Date == df.Date.max(),dropdown].mean()
    formatted_value = "{:,.2f}".format(avg_value)
    fig = px.bar(
        latest_df, x="Player", y=dropdown,
        title=f"Player {dropdown} Scores As Of {df.Date.max().strftime('%m/%d/%Y')}",
        
    )
    fig.add_hline(y=avg_value,line_dash="dot",annotation_text=f"<b>Average: {formatted_value}</b>",annotation_position="bottom left")
    fig.update_traces(marker_color="lightseagreen")
    return fig

# if __name__ == '__main__':
#     app.run(debug=True)