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
fig = map_fr_merge_pol()
# initialize app
# set app layout
layout = html.Div(children=[
    html.Div(children =[html.P("Choix du pays : ", style={'font-size':'25px'}),
                        dcc.RadioItems(options=[{'label': "France", 'value': "simple_fr_merge_pol"},
                                                {'label': 'Europe', 'value' : "simple_europe_pol"},
                                                {'label': "Etats-Unis", 'value': "simple_usa_pol"}],
                                        value = 'simple_fr_merge_pol',
                                        id = 'radioitems_pol',
                                        className='three columns',
                                        labelStyle={'display': 'block'})],
            style={'width': '400px', 'float':'left','margin-left':'100px'}),
    html.Div(children=[dcc.Graph(id='carte_pol', figure=fig, style={"max-width": "900px",'margin':'auto'})],style={'margin':'auto'}), ]
)

#callbacks Polarité 
@callback(
    Output(component_id='carte_pol', component_property='figure'),
    Input(component_id='radioitems_pol', component_property='value'),
)
def update_hist2(value):
    if value == "simple_fr_merge_pol":
        return map_fr_merge_pol()
    if value == "simple_europe_pol":
        return map_europe_pol()
    if value == "simple_usa_pol":
        return map_usa_pol()
