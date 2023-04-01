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
    from map_TT import *


dash.register_page(__name__)
# make plot
fig = map_europe_leader_insulte()
# initialize app
# set app layout
layout = html.Div(children=[
    html.Div(children =[html.P("Choix du critère : ",style={"font-size":'25px'}),
                        dcc.RadioItems(options=[{'label': "Insultes", 'value': "insultes"},
                                                {'label': 'Polarité', 'value' : "polarite"},
                                                {'label': "Subjectivité", 'value': "subjectivite"}],
                                        value = 'insultes',
                                        id = 'radioitems_leader',
                                        labelStyle={'display': 'block'})],
            style={'width': '400px', 'float':'left','margin-left':'100px'}),
    html.Div(children=[dcc.Graph(id='carte_leader', figure=fig, style={"max-width": "900px",'margin':'auto'})],style={'margin':'auto'}), ]
)

#callbacks Polarité 
@callback(
    Output(component_id='carte_leader', component_property='figure'),
    Input(component_id='radioitems_leader', component_property='value'),
)
def update_hist2(value):
    if value == "insultes":
        return map_europe_leader_insulte()
    if value == "polarite":
        return map_europe_leader_pol()
    if value == "subjectivite":
        return map_europe_leader_sub()
