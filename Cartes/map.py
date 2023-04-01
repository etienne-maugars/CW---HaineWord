import json
import pandas as pd
import plotly.express as px
from urllib.request import urlopen

#USA
def map_usa_sub(): #Renvoie la carte de subjectivité des USA
    f=open('database/gz_2010_us_040_00_500k.json')
    states=json.load(f)

    g=open('database/simple_usa.json')
    df = json.load(g)

    maximum=max(df["mean_sub"].values())
    minimum=min(df["mean_sub"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.name', color='mean_sub',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="usa",
                            labels={'mean_sub':'Subjectivité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    return fig


def map_usa_pol(): #Renvoie la carte de polarité des USA
    f=open('database/gz_2010_us_040_00_500k.json')
    states=json.load(f)

    g=open('database/simple_usa.json')
    df = json.load(g)

    maximum=max(df["mean_pol"].values())
    minimum=min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.name', color='mean_pol',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="usa",
                            labels={'mean_pol':'Polarité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    return fig


def map_usa_insultes(): #Renvoie la carte d'insultes' des USA
    f=open('database/gz_2010_us_040_00_500k.json')
    states=json.load(f)

    g=open('database/simple_insulte_usa.json')
    df = json.load(g)

    maximum=max(df["mean_insultes"].values())
    minimum=min(df["mean_insultes"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.name', color='mean_insultes',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="usa",
                            labels={'mean_insultes':"Nombre d'insulte moyenne"}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    return fig


#OBSOLETE
def map_fr_sub(): #Renvoie la carte de subjectivité de France basé sur une base de données avec uniquement 100 tweets par dpt (on a augmenté la database par la suite)
    with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as f:
        states=json.load(f)

    g=open('database/simple_fr.json')
    df = json.load(g)

    maximum=max(df["mean_sub"].values())
    minimum=min(df["mean_sub"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.nom', color='mean_sub',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_sub':'Subjectivité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


def map_fr_pol(): #Renvoie la carte de polarité de France basé sur une base de données avec uniquement 100 tweets par dpt (on a augmenté la database par la suite)
    with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as f:
        states=json.load(f)

    g=open('database/simple_fr.json')
    df = json.load(g)

    maximum=max(df["mean_pol"].values())
    minimum=min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.nom', color='mean_pol',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_pol':'Polarité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


#EUROPE
def map_europe_sub(): #Renvoie la carte de subjectivité de l'Europe
    with open('database/europe.json') as f:
        states=json.load(f)

    g=open('database/simple_europe.json')
    df = json.load(g)

    maximum=max(df["mean_sub"].values())
    minimum=min(df["mean_sub"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.NAME', color='mean_sub',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_sub':'Subjectivité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


def map_europe_pol(): #Renvoie la carte de polarité de l'Europe
    with open('database/europe.json') as f:
        states=json.load(f)

    g=open('database/simple_europe.json')
    df = json.load(g)

    maximum=max(df["mean_pol"].values())
    minimum=min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.NAME', color='mean_pol',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_pol':'Polarité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


def map_europe_insulte(): #Renvoie la carte d'insultes de l'Europe
    with open('database/europe.json') as f:
        states=json.load(f)

    g=open('database/simple_insulte_europe.json')
    df = json.load(g)

    maximum=max(df["mean_insultes"].values())
    minimum=min(df["mean_insultes"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.NAME', color='mean_insultes',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_insultes':"Nombre d'insulte en moyenne"}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig    



#EUROPE LEADER
def map_europe_leader_sub(): #Renvoie la carte de subjectivité des chefs d'Etat européens
    with open('database/europe.json') as f:
        states=json.load(f)

    g=open('database/simple_leader_europe.json')
    df = json.load(g)

    maximum=max(df["mean_sub"].values())
    minimum=min(df["mean_sub"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.NAME', color='mean_sub',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_sub':'Subjectivité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


def map_europe_leader_pol(): #Renvoie la carte de polarité des chefs d'Etat européens
    with open('database/europe.json') as f:
        states=json.load(f)

    g=open('database/simple_leader_europe.json')
    df = json.load(g)

    maximum=max(df["mean_pol"].values())
    minimum=min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.NAME', color='mean_pol',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_pol':'Polarité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


def map_europe_leader_insulte(): #Renvoie la carte d'insultes des chefs d'Etat européens
    with open('database/europe.json') as f:
        states=json.load(f)
        
    g = open('database/simple_insulte_leader_europe.json')
    df = json.load(g)

    maximum=max(df["mean_insultes"].values())
    minimum=min(df["mean_insultes"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.NAME', color='mean_insultes',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_insultes':"Nombres d'insultes en  moyenne"}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


#FR MERGE
def map_fr_merge_pol(): #Renvoie la carte de polarité de France basé sur une base de données étendue
    with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as f:
        states=json.load(f)

    g=open('database/simple_fr_merge_200_14-11-2022_ET_16-11-2022.json')
    df = json.load(g)

    maximum=max(df["mean_pol"].values())
    minimum=min(df["mean_pol"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.nom', color='mean_pol',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_pol':'Polarité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig    
    

def map_fr_merge_sub(): #Renvoie la carte de subjectivité de France basé sur une base de données étendue
    with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as f:
        states=json.load(f)

    g=open('database/simple_fr_merge_200_14-11-2022_ET_16-11-2022.json')
    df = json.load(g)

    maximum=max(df["mean_sub"].values())
    minimum=min(df["mean_sub"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.nom', color='mean_sub',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_sub':'Subjectivité moyenne'}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig  


def map_fr_merge_insulte(): #Renvoie la carte d'insultes de France basé sur une base de données étendue
    with urlopen("https://france-geojson.gregoiredavid.fr/repo/departements.geojson") as f:
        states=json.load(f)

    g = open('database/simple_insulte_fr_merge.json')
    df = json.load(g)

    maximum=max(df["mean_insultes"].values())
    minimum=min(df["mean_insultes"].values())

    fig = px.choropleth(df, geojson=states, locations='name',featureidkey='properties.nom', color='mean_insultes',
                            color_continuous_scale="bluered",
                            range_color=(minimum, maximum),
                            scope="europe",
                            labels={'mean_insultes':"Nombres d'insultes en  moyenne"}
                            )
    
    # Aller voir la doc, tout est expliqué : https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#BBD2E1')
    fig.update_geos(fitbounds="locations")
    return fig


# if __name__ == "__main__":
# """
#     map_usa_sub().show()
#     map_usa_pol().show()
#     map_usa_insultes().show()
    
#     map_europe_sub().show()
#     map_europe_pol().show()
#     map_europe_insulte().show()
    
#     map_europe_leader_sub().show()
#     map_europe_leader_pol().show()
#     map_europe_leader_insulte().show()

#     map_fr_merge_sub().show()
#     map_fr_merge_pol().show()
#     map_fr_merge_insulte().show()
# """ 
    
