import pandas as pd
import dash_bootstrap_components as dbc
import dash
from dash import Dash, html, Input, Output, dash_table, dcc, callback
from dash.dash_table.Format import Format, Group
import plotly.express as px
import datetime as dt


dash.register_page(__name__)


df = pd.read_csv("assets/ROC_player_scores.csv", thousands=',')
df.date = pd.to_datetime(df['date'], format="%m/%d/%y").dt.date

col_names = ['Date','Player','Rank','Total','RP Spent','Battles','Negotiations','Traded Goods','Wonder Orbs','Activity Points','Events','Compass Donations','TH Encounters']
df.columns = col_names

max_date = df.Date.max()

max_df = df.loc[df.Date == max_date].set_index('Player').drop("Date",axis=1)
remaining = df.loc[df.Date != max_date]
second_df = remaining.loc[remaining.Date == remaining.Date.max()].set_index('Player').drop("Date",axis=1)

diff_df = max_df - second_df

def reward_df(score):
     reward = diff_df[[score]].loc[diff_df[score].isin(diff_df[[score]].sort_values(score,ascending=False)[score].unique()[:5])].sort_values(score,ascending=False).reset_index()
     reward['Place'] = reward[[score]].rank(method='dense', ascending=False)
     return reward
                                        

rp_reward = reward_df("RP Spent")
orb_reward = reward_df("Wonder Orbs")
activity_reward = reward_df("Activity Points")

def results(df,score):
    # text_results = f"{score}:\n" 
    text_results = [f"{score}:",html.Br()]
    for i,row in df.iterrows():
        # text_results = text_results + f"{i+1} - {row['Player']} - {int(row[1])} \n" 
        text_results.append(f"{int(row['Place'])} - {row['Player']} - {int(row[1])} \n")
        text_results.append(html.Br())
    return text_results

layout = html.Div([
   html.H1(f"Rewards for {max_date.strftime('%m/%d/%Y')}"),
   html.P('Below are the winners of the RagnOroCk Player Profile Rewards for the current week.  There is a section of text for easy copying for announcements in Discord.'),
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
            dbc.CardHeader("Wonder Orbs"),
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
]),
dbc.Row([html.Br()]),
dbc.Row([
     html.P([
        f"""For the week of {max_date.strftime('%m/%d/%Y')}, the results are:""",
        html.Br(),
        html.Br()] +
        results(orb_reward,"Orbs") + [
        html.Br()] +
        results(activity_reward,"Activity Points") + [
        html.Br()] +
        results(rp_reward,"RP Spent")
       
        )])
          

],
style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})

f"""For the week of {max_date.strftime('%m/%d/%Y')}, the results are:\n"""
results(orb_reward,"Orbs")