import tweepy
import geopy
from geopy.geocoders import Nominatim
from tweet_collection.credentials import *
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import pandas as pd
from storage import store_tweets


def geoloc(town): #Renvoie la LAt, LON d'une ville
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode(town)
    return ((location.latitude, location.longitude))


def town_tweets(town, radius): #Renvoie les tweets postés dans une ville dans un rayon de radius km
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)

    (lat, long) = geoloc(town)
    tweets = api.search_tweets(" ", count=50, tweet_mode="extended", geocode="{},".format(
        lat) + "{},".format(long) + str(radius) + "km")
    return (tweets)


def town_polarity(town): #Renvoie la polarité moyenne des tweets associés à une ville
    tweets = town_tweets(town, 100)
    polarity_moy = 0
    n = len(tweets)
    for tweet in tweets:
        text = TextBlob(tweet.full_text, pos_tagger=PatternTagger(),
                        analyzer=PatternAnalyzer())
        (pol, sub) = text.sentiment
        polarity_moy += pol
    return (polarity_moy/n)


def town_list(states):
    dic = pd.DataFrame(
        {'state': pd.Categorical([e for e in states.keys()]),
         'town': pd.Categorical([e for e in states.values()]),
         'pol': pd.Categorical([town_polarity(e) for e in states.values()])
         })

    store_tweets(
        dic, "C:/Users/Théo Fernet/Documents/CodingWeeks/haineword/storage/dataframe-usa.json")
    return (dic)


def store_town(states):
    for state in states.keys():
        dic = pd.DataFrame(
            {'state': state,
             'town': states[state],
             'pol': town_polarity(states[state])
             })
        store_tweets(
            dic, "C:/Users/Théo Fernet/Documents/CodingWeeks/haineword/storage/{}.json".format(states[state]))


def df(town):
    tweets = town_tweets(town, 100)
    dict = {}
    dict['tweet_textual_content'] = []
    dict['Date'] = []
    dict['hashtags'] = []
    dict['id_tweet'] = []
    dict['Likes'] = []
    dict['RTs'] = []
    dict['pol'] = []
    for status in tweets:
        text = TextBlob(status.full_text)
        (pol, sub) = text.sentiment
        dict['town'] = town
        dict['tweet_textual_content'].append(status.full_text)
        dict['Date'].append(status.created_at)
        dict['hashtags'].append(status.entities['hashtags'])
        dict['id_tweet'].append(status.id)
        dict['Likes'].append(status.favorite_count)
        dict['RTs'].append(status.retweet_count)
        dict['pol'].append(pol)
    data = pd.DataFrame(dict)
    store_tweets(
        data, "C:/Users/Théo Fernet/Documents/CodingWeeks/haineword/storage/{}.json".format(town))
    return (data)


if __name__ == "__main__":
    departements = {"Ain": "Bourg-en-Bresse",
                    "Aisne":	"Laon",
                    "Allier": "Moulins",
                    "Alpes de Haute-Provence": "Digne-les-Bains",
                    "Hautes-Alpes": "Gap",
                    "Alpes-Maritimes": "Nice",
                    "Ardêche": "Privas",
                    "Ardennes": "Charleville-Mézières",
                    "Ariège": "Foix",
                    "Aube": "Troyes",
                    "Aude": "Carcassonne",
                    "Aveyron": "Rodez",
                    "Bouches-du-Rhône": "Marseille",
                    "Calvados": "Caen",
                    "Cantal	Aurillac": "Auvegne",
                    "Charente": "Angoulême",
                    "Charente-Maritime": "La Rochelle",
                    "Cher": "Bourges",
                    "Corrèze": "Tulle",
                    "Corse-du-Sud": "Ajaccio",
                    "Haute-Corse": "Bastia",
                    "Côte-d'Or": "Dijon",
                    "Côtes d'Armor": "St-Brieuc",
                    "Creuse": "Guéret",
                    "Dordogne": "Périgueux",
                    "Doubs": "Besançon",
                    "Drôme": "Valence",
                    "Eure": "Évreux",
                    "Eure-et-Loir": "Chartres",
                    "Finistère": "Quimper",
                    "Gard": "Nîmes",
                    "Haute-Garonne": "Toulouse",
                    "Gers": "Auch",
                    "Gironde": "Bordeaux",
                    "Hérault": "Montpellier",
                    "Île-et-Vilaine": "Rennes",
                    "Indre": "Châteauroux",
                    "Indre-et-Loire": "Tours",
                    "Isère": "Grenoble",
                    "Jura": "Lons-le-Saunier",
                    "Landes": "Mont-de-Marsan",
                    "Loir-et-Cher": "Blois",
                    "Loire": "Saint-Étienne",
                    "Haute-Loire": "Le Puy-en-Velay",
                    "Loire-Atlantique": "Nantes",
                    "Loiret": "Orléans",
                    "Lot": "Cahors",
                    "Lot-et-Garonne": "Agen",
                    "Lozère": "Mende",
                    "Maine-et-Loire": "Angers",
                    "Manche": "Saint-Lô",
                    "Marne": "Châlons-en-Champagne",
                    "Haute-Marne": "Chaumont",
                    "Mayenne": "Laval",
                    "Meurthe-et-Moselle": "Nancy",
                    "Meuse": "Bar-le-Duc",
                    "Morbihan": "Vannes",
                    "Moselle": "Metz",
                    "Nièvre": "Nevers",
                    "Nord": "Lille",
                    "Oise": "Beauvais",
                    "Orne": "Alençon",
                    "Pas-de-Calais": "Arras",
                    "Puy-de-Dôme": "Clermont-Ferrand",
                    "Pyrénées-Atlantiques": "Pau",
                    "Hautes-Pyrénées": "Tarbes",
                    "Pyrénées-Orientales":	"Perpignan",
                    "Bas-Rhin": "Strasbourg",
                    "Haut-Rhin": "Colmar",
                    "Rhône": "Lyon",
                    "Haute-Saône": "Vesoul",
                    "Saône-et-Loire": "Mâcon",
                    "Sarthe": "Le Mans",
                    "Savoie": "Chambéry",
                    "Haute-Savoie": "Annecy",
                    "Paris": "Paris",
                    "Seine-Maritime": "Rouen",
                    "Seine-et-Marne": "Melun",
                    "Yvelines": "Versailles",
                    "Deux-Sèvres": "Niort",
                    "Somme": "Amiens",
                    "Tarn": "Albi",
                    "Tarn-et-Garonne": "Montauban",
                    "Var": "Toulon",
                    "Vaucluse": "Avignon",
                    "Vendée": "La Roche-sur-Yon",
                    "Vienne": "Poitiers",
                    "Haute-Vienne": "Limoges",
                    "Vosges": "Épinal",
                    "Yonne": "Auxerre",
                    "Territoire-de-Belfort": "Belfort",
                    "Essonne": "Évry",
                    "Hauts-de-Seine": "Nanterre",
                    "Seine-Saint-Denis": "Bobigny",
                    "Val-de-Marne": "Créteil",
                    "Val-d'Oise": "Pontoise"}
    dic = {"Paris": "Paris", "Bouches-du-Rhône": "Marseille", "Rhône": "Lyon", "Haute-Garonne": "Toulouse", "Alpes-Maritimes": "Nice", "Loire-Atlantique": "Nantes", "Hérault": "Montpellier", "Bas-Rhin": "Strasbourg", "Gironde": "Bordeaux", "Nord": "Lille", "Île-et-Vilaine": "Rennes", "Var": "Toulon", "Isère": "Grenoble", "Côte-d'Or": "Dijon", "Maine-et-Loire": "Angers",
           "Gard": "Nîmes", "Puy-de-Dôme": "Clermont-Ferrand", "Sarthe": "Le Mans", "Indre-et-Loire": "Tours", "Somme": "Amiens", "Haute-Vienne": "Limoges", "Haute-Savoie": "Annecy", "Pyrénées-Orientales": "Perpignan", "Moselle": "Metz", "Doubs": "Besançon", "Loiret": "Orléans", "Seine-Maritime": "Rouen", "Calvados": "Caen"}
    state_capitals_dict = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
                           'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Colombus', 'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}
    
    #for town in state_capitals_dict.values():
    #    df(town)
