import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'Cartes'))
if True:
    from map import *
    from map_TT import *


app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.LUX], use_pages=True)
liste_nav = []
liste_nav.append(html.P(style={"margin-left": "130px", 'color': '#7393B3'}))
for name in dash.page_registry.keys():
    liste_nav.append(dbc.NavLink(
        dash.page_registry[name]['name'], href=dash.page_registry[name]['path'], style={"font-weight": "bold"}))
    liste_nav.append(
        html.P(style={"margin-left": "150px", 'color': '#7393B3'}))


# set app layout
app.layout = html.Div(children=[html.Br(),
                                html.H1('HaineWord, le site des cartes de tweets !', style={
                                        'text-align': 'center'}),
                                dbc.NavbarSimple(
    liste_nav,
    className="mb-5",
    color='#7393B3',
    links_left=True,
    style={'border-radius': '15px', 'border-color': '#6F8FAF'}),
    dash.page_container])


if __name__ == "__main__":
    app.run_server(debug=False)
