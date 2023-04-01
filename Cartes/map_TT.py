from datetime import date
import json
import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'TT'))
if True:
    from collect_TT import *


def map_usa():
    # on ouvre le fichier geojson des états unis (ce qui permet d'afficher les différents états et de les voir comme entités différentes)
    f = open('database/gz_2010_us_040_00_500k.json')
    # on le transforme en type dictionnaire (c'était un type json)
    states = json.load(f)

    # on ouvre le fichier contenant les données des états des usa dans la database
    g = open('database/simple_usa.json')
    # on le transforme en type dictionnaire (c'était un type json)
    df = json.load(g)

    # valeur maximale de polarité moyenne des états (pour l'échelle)
    maximum = max(df["mean_pol"].values())
    # valeur minimale de polarité moyenne des états (pour l'échelle)
    minimum = min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name', featureidkey='properties.name', color='mean_pol',
                        color_continuous_scale="bluered",
                        range_color=(minimum, maximum),
                        scope="usa",
                        labels={'mean_pol': 'Polarité moyenne'}
                        )  # on crée la figure avec comme locations la clé "name" du dictionnaire df

    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},paper_bgcolor='#7393B3')
    return fig


def map_fr():
    # c'est le fichier geojson des departements de france, compliqué à télécharger dans la database, on va le chercher sur internet à chaque fois
    with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as f:
        states = json.load(f)

    # on ouvre le fichier contenant les données de chaque departement (polarité moyenne, noms, subjectivité moyenne)
    g = open('database/simple_fr.json')
    df = json.load(g)

    # max de polarité moyenne (pour l'échelle)
    maximum = max(df["mean_pol"].values())
    # min de polarité moyenne (pour l'échelle)
    minimum = min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name', featureidkey='properties.nom', color='mean_pol',
                        color_continuous_scale="bluered",
                        range_color=(minimum, maximum),
                        scope="europe",
                        labels={'mean_pol': 'Polarité moyenne'}
                        )

    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


def map_europe():
    # on read le fichier geojson d'europe (c'est ce qui nous précise la forme des pays à afficher)
    with open('database/europe.json') as f:
        states = json.load(f)

    # on read le fichier contenant les données des pays d'europe (polarité moyenne, noms...)
    g = open('database/simple_europe.json')
    df = json.load(g)

    # valeur maximale de polarité dans le fichier contenant les données des pays
    maximum = max(df["mean_pol"].values())
    # valeur minimale de polarité dans le fichier contenant les données du candidat
    minimum = min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name', featureidkey='properties.NAME', color='mean_pol',
                        color_continuous_scale="bluered",
                        range_color=(minimum, maximum),
                        scope="europe",
                        labels={'mean_pol': 'Polarité moyenne'}
                        )  # on crée la figure

    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    fig.show()


def map_candi_date(candidate_name):
    # on read le fichier geojson des états unis
    f = open('database/gz_2010_us_040_00_500k.json', 'r')
    states = json.load(f)

    g = open('database/simples/simple_states_' +  # on read le fichier contenant les données du candidat qu'on étudie
             candidate_name + '.json')
    df = json.load(g)

    # valeur maximale de polarité dans le fichier contenant les données du candidat
    maximum = max(df["mean_pol"].values())
    # valeur minimale de polarité dans le fichier contenant les données du candidat
    minimum = min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name', featureidkey='properties.name', color='mean_pol',
                        color_continuous_scale="bluered",
                        range_color=(minimum, maximum),
                        scope="usa",
                        labels={'mean_pol': 'Polarité moyenne'}
                        )  # on crée la figure

    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},paper_bgcolor='#BBD2E1')
    return fig


def map_usa_recherche(candidate_name):
    # si les données sont déja dans la database, pas besoin de rechercher, on return directement la figure voulue
    if os.path.exists('database/simples/simple_states_' + candidate_name + ".json"):
        return (map_candi_date(candidate_name))
    else:  # les données sont pas dans la databasen on collectionne donc les tweets
        state_capitals_dict = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
                               'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Colombus', 'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}
        # pour tous les états, on rajoute à la database les données des 100 tweets collectionnés
        simple_candidate(state_capitals_dict, candidate_name)
        return (map_candi_date(candidate_name))  # on return la figure


if __name__ == "__main__":
    state_capitals_dict = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
                           'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Colombus', 'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}
    map_usa_recherche("Fuck").show()
