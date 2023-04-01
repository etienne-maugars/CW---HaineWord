import dash
from dash import html
from dash import dcc, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import os
import sys
sys.path.append(os.path.join(os.getcwd(),'Cartes'))
if True :
    from map import *


dash.register_page(__name__)
# make plot
fig = map_fr_merge_sub()
# initialize app
# set app layout
layout = html.Div(children=[
    html.Div(children =[html.P("Choix du pays :               ",style={"font-size":'25px'}),
                        dcc.RadioItems(options=[{'label': "France", 'value': "simple_fr_merge_sub"},
                                                {'label': 'Europe', 'value' : "simple_europe_sub"},
                                                {'label': "Etats-Unis", 'value': "simple_usa_sub"}],
                                        value = 'simple_fr_merge_sub',
                                        id = 'radioitems_sub',
                                        labelStyle={'display': 'block'})],
            style={'width': '400px', 'float':'left','margin-left':'100px'}),

    html.Div(children=[dcc.Graph(id='carte_sub', figure=fig, style={"max-width": "900px",'margin':'auto','background-color':'#9966FF'})])
    
    ]
)
#callbacks Subjectivité 
@callback(
    Output(component_id='carte_sub', component_property='figure'),
    Input(component_id='radioitems_sub', component_property='value'),
)
def update_hist2(value):
    if value == "simple_fr_merge_sub":
        return map_fr_merge_sub()
    if value == "simple_europe_sub":
        return map_europe_sub()
    if value == "simple_usa_sub":
        return map_usa_sub()


if __name__ == "__main__":
    app.run_server(debug=True)