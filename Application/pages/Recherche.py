import dash
from dash import html
from dash import dcc,callback
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

fig = map_usa_recherche("Trump")
dash.register_page(__name__)
layout = html.Div(children=[html.Div([
        html.Div("Recherchez une personne, une entreprise : ",style={"text-align":'center', 'font-size':'25px'}),
        html.Div([
            dcc.Input(id='my_input', type='text',value="Trump", style={'padding':'12px','margin-left':'450px','width':'600px','border-radius': '10px'}),
            dbc.Button('Valider', 
                    color="success", 
                    className="me-1", 
                    id='submit_val',
                    n_clicks=0, 
                    style={'padding':'10px','margin':'auto','border-radius': '12px'})]
            ),
        dcc.Graph(id="my_output",figure=fig, style = {"max-width": "800px",'margin':'auto','border-radius': '100px'} )

    ])]
)

@callback(
    Output(component_id='my_output', component_property='figure'),
    Input(component_id='submit_val', component_property='n_clicks'),
    State(component_id='my_input',component_property='value')
)
def update_hist(n_clicks,value):
    print(value)
    if value != None:
        return map_usa_recherche(str(value))
    return dbc.Spinner(color='primary')
