import json
from urllib.request import urlopen
import deepl
from datetime import date
import os
import pandas as pd
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob import TextBlob
from geopy.geocoders import Nominatim
import geopy
import tweepy
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'tweet_connection'))
if True:
    from deepl_auth import *
    from twitter_connection_setup import *
sys.path.append(
    'C:\\Users\\Théo Fernet\\Documents\\CodingWeeks\\pascoollesinsultes\\tweet_collect')
sys.path.append(
    'C:\\Users\\Théo Fernet\\Documents\\CodingWeeks\\pascoollesinsultes\\tweet_analysis')


lang_ok = ['bg',
           'cs',
           'da',
           'de',
           'el',
           'en',
           'en'
           'es',
           'et',
           'fi',
           'fr',
           'hu',
           'id',
           'it',
           'ja',
           'lt',
           'lv',
           'nl',
           'pl',
           'pt'
           'ro',
           'ru',
           'sk',
           'sl',
           'sv',
           'tr',
           'uk',
           'zh']


def quelle_langue(pays): #Donnée le pays, cette fonction renvoie la langue courante sous forme du code ISO 639-1
    data = pd.read_json(
        'database/name_to_iso.json')
    a = pd.Index(data['name']).get_loc(pays)
    return data["iso"][a]


def traduit(texte, langue_src, langue_dest='en-gb'):  # Pour traduire le texte
    auth_key = DEEPL_AUTH
    translator = deepl.Translator(auth_key)
    resultat = translator.translate_text(
        texte, source_lang=langue_src, target_lang=langue_dest)
    return str(resultat)


def get_tweet_pays_euro(pays, c=1000):  # Obtenir les tweets d'un pays donné

    langue = quelle_langue(pays)
    if not (langue in lang_ok):
        langue = 'en'  # Si pas supporté par DeepL, on prend des tweets en anglais

    print(langue)

    data = pd.read_json(
        'database/europe.json')["features"]
    data_bis = pd.read_json(
        'database/name_to_iso.json')

    a = pd.Index(data_bis['name']).get_loc(pays)
    long, lat = data[a]["properties"]["LON"], data[a]["properties"]["LAT"]
    aire = data[a]["properties"]["AREA"]  # en km²

    # On considère le pays comme un cercle centré en LAT, LON (la database donne le LAT, LON du centre)
    rayon = get_rayon(aire)

    api = twitter_setup()

    tweets = api.search_tweets(" ", count=c, lang=langue, tweet_mode="extended", geocode="{},".format(
        lat) + "{},".format(long) + str(rayon) + "km")

    filename = "database/" + pays+'_'+str(c)+'_' + \
        str(date.today().strftime("%d-%m-%Y"))+'.json'

    dict = {}

    dict["original_text"] = []
    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity'] = []
    dict['subjectivity'] = []
    dict['mean_subjectivity'] = []
    dict['screen_name'] = []
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state'] = []
    dict['iso_639'] = []

    s_pol = 0
    s_sub = 0
    compteur = 0
    for status in tweets:
        texte_traduit = traduit(status.full_text, langue)
        text = TextBlob(texte_traduit)
        pol, sub = text.sentiment
        s_pol += pol
        s_sub += sub
        compteur += 1
        dict['original_text'].append(status.full_text)
        dict['full_text'].append(texte_traduit)
        dict['date'].append(status.created_at)
        dict['screen_name'].append(status.user.screen_name)
        dict['polarity'].append(pol)
        dict['subjectivity'].append(sub)
        dict['Likes'].append(status.favorite_count)
        dict['RTs'].append(status.retweet_count)
        dict['state'].append(pays)
        dict["iso_639"].append(langue)

    for k in range(compteur):
        dict['mean_polarity'].append(s_pol/compteur)
        dict['mean_subjectivity'].append(s_sub/compteur)

    finalement = pd.DataFrame(dict)
    pd.DataFrame.to_json(finalement, filename, indent=2, orient='columns')


def get_rayon(a): #Donnée l'aire d'un pays, cette fonction renvoie le rayon de recherche des tweets (il faut fournir LON, LAT et rayon à l'api)
    #En fait on a considéré qu'un pays était un cercle de rayon r et donc d'aire pi*r².
    #L'aire ainsi que la LON LAT du centre du pays sont fournis par le geojson
    import numpy as np
    pi = np.pi
    r = (a/pi)**(0.5)
    return r


def geoloc(town): #Donne la LAT, LON d'une ville
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode(town)
    return ((location.latitude, location.longitude))


def town_tweets(town, radius, c, l='en'): #Renvoie les tweets postés dans une ville dans un rayon de radius km
    api = twitter_setup()

    (lat, long) = geoloc(town)
    tweets = api.search_tweets(" ", count=c, lang=l, tweet_mode="extended", geocode="{},".format(
        lat) + "{},".format(long) + str(radius) + "km")
    return (tweets)


def town_polarity(town):  # polarité moyenne des tweets sortant de cette ville
    tweets = town_tweets(town, 100)
    polarity_moy = 0
    n = len(tweets)
    for tweet in tweets:
        text = TextBlob(tweet.full_text, pos_tagger=PatternTagger(),
                        analyzer=PatternAnalyzer())  # si la langue est francaise ojn rajoute pos_tagger et analyzer
        (pol, sub) = text.sentiment
        polarity_moy += pol
    return (polarity_moy/n)


# crée un fichier de format qu'on a appelé 'simple' des polarités moyennes des tweets dans les régions states
def simple_df(states, langue, d=date.today().strftime("%d-%m-%Y")):
    dic = pd.DataFrame(
        {'name': pd.Categorical([e for e in states.keys()]),
         'mean_pol': pd.Categorical([mean_polarity(e, da=d) for e in states.keys()])
         })
    pd.DataFrame.to_json(dic, 'database/simples/simple_'+langue+'.json',
                         indent=2, orient='columns')


# Pour un état donné par state, enregistre un .json avec les colonnes (voir dans la définition)
# stocke les tweets d'un état américain, même commentaire que la fonction state_candidate_dict (voir en dessous)
def store_tweets_usa(state, c=100, langue='en'):
    filename = "database/" + state+'_'+str(c)+'_' + \
        str(date.today().strftime("%d-%m-%Y"))+'.json'
    tweets = town_tweets(state_capitals_dict[state], 25, c, langue)

    dict = {}

    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity'] = []
    dict['subjectivity'] = []
    dict['mean_subjectivity'] = []
    dict['screen_name'] = []
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state'] = []

    s_pol = 0
    s_sub = 0
    compteur = 0
    for status in tweets:
        if langue == 'fr':
            text = TextBlob(
                status.full_text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        elif langue == 'en':
            text = TextBlob(status.full_text)
        pol, sub = text.sentiment
        s_pol += pol
        s_sub += sub
        compteur += 1
        dict['full_text'].append(status.full_text)
        dict['date'].append(status.created_at)
        dict['screen_name'].append(status.user.screen_name)
        dict['polarity'].append(pol)
        dict['subjectivity'].append(sub)
        dict['Likes'].append(status.favorite_count)
        dict['RTs'].append(status.retweet_count)
        dict['state'].append(state)

    for k in range(compteur):
        dict['mean_polarity'].append(s_pol/compteur)
        dict['mean_subjectivity'].append(s_sub/compteur)

    data = pd.DataFrame(dict)
    pd.DataFrame.to_json(data, filename, indent=2, orient='columns')


# Pour un département donné par state, enregistre un .json avec les colonnes (voir dans la définition)
# stocke les tweets d'un deparetement francais, même commentaire que la fonction state_candidate_dict (voir en dessous)
def store_tweets_fr(state, c=100, langue='fr'):
    filename = 'database/' + state+'_'+str(c)+'_' + \
        str(date.today().strftime("%d-%m-%Y"))+'.json'

    rayon = 25
    if state in ['Paris', 'Seine-et-Marne', 'Yvelines', 'Seine-Saint-Denis', 'Val-de-Marne', "Val-d'Oise", "Hauts-de-Seine"]:
        rayon = 5  # Car les départements d'Ile de France sont très serrés
    tweets = town_tweets(departements[state], rayon, c, langue)

    dict = {}

    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity'] = []
    dict['subjectivity'] = []
    dict['mean_subjectivity'] = []
    dict['screen_name'] = []
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state'] = []

    s_pol = 0
    s_sub = 0
    compteur = 0
    for status in tweets:
        if langue == 'fr':
            text = TextBlob(
                status.full_text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        elif langue == 'en':
            text = TextBlob(status.full_text)
        pol, sub = text.sentiment
        s_pol += pol
        s_sub += sub
        compteur += 1
        dict['full_text'].append(status.full_text)
        dict['date'].append(status.created_at)
        dict['screen_name'].append(status.user.screen_name)
        dict['polarity'].append(pol)
        dict['subjectivity'].append(sub)
        dict['Likes'].append(status.favorite_count)
        dict['RTs'].append(status.retweet_count)
        dict['state'].append(state)

    for k in range(compteur):
        dict['mean_polarity'].append(s_pol/compteur)
        dict['mean_subjectivity'].append(s_sub/compteur)

    data = pd.DataFrame(dict)
    pd.DataFrame.to_json(data, filename, indent=2, orient='columns')


# fonction returnant la polarité moyenne des tweets d'un état state, pas utilisée pour l'appli
def mean_polarity(state, c=100, da=date.today().strftime("%d-%m-%Y")):
    file = 'database/' + \
        state+'_'+str(c)+'_'+str(da)+'.json'
    data = pd.read_json(file)
    s = 0
    n = len(data.polarity)
    for elt in data.polarity:
        s += elt
    return s/n


# fonction qui return un dictionnaire des c=100 tweets collectionné dans l'état state concernant le candidat, dans un disque de rayon radius centré en la capitale de l'état
def state_candidate_dict(candidate_name, radius, state, c=100):
    filename = "database/state_candidate_tweets/" + state+'_'+candidate_name+'_' + str(c) + \
        str(date.today().strftime("%d-%m-%Y")) + \
        '.json'  # pas nécessaire mais utile si on veut rajouter une fonction de stockage dans cette fonction
    api = twitter_setup()  # la fonction twitter_setup se trouve dans tweet_connection/twitter_connection_setup.py et utilise les clés d'authentification à l'api twitter
    state = str(state)
    state_capitals_dict = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
                           'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Colombus', 'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}
    # on a besoin des coordonnées de la capitale d'état pour pouvoir rechercher des tweets proche de celle ci
    (lat, long) = geoloc(state_capitals_dict[state])
    tweets = api.search_tweets(candidate_name, count=c, tweet_mode="extended", result_type='recent', geocode="{},".format(
        lat) + "{},".format(long) + str(radius) + "km")  # on collectionne c=100 tweets dans un disque de rayon radius centré en les coordonnés de la capitale d'état
    s_pol = 0
    s_sub = 0
    dict = {}  # on crée le dictionnaire qu'on returnera contenant les infos qui nous intéressent

    dict['full_text'] = []  # le text du tweet
    dict['date'] = []  # la date du tweet
    dict['polarity'] = []  # la polarité du tweet
    # la polarité moyenne de l'état qu'on rajoutera dans la deuxieme boucle
    dict['mean_polarity'] = []
    dict['subjectivity'] = []  # la subjectivité du tweet
    # la subjectivité moyenne de l'état qu'on rajoutera dans la deuxieme boucle
    dict['mean_subjectivity'] = []
    dict['screen_name'] = []  # le pseudo de l'utilisateur qui a tweeté
    dict['Likes'] = []  # le nombre de likes du tweet
    dict['RTs'] = []  # le nombre de retweets du tweet
    dict['state'] = []  # le nom de l'état

    compteur = 0
    for status in tweets:  # on parcourt l'ensemble des tweet collectionnés, appelés status
        # on transforme en type TextBlob le text du tweet pour pouvoir analyser la polarité et subjectivité
        text = TextBlob(status.full_text)
        # la fonction .sentiment nous rend un tuple (polarité, subjectivité) du tweet
        pol, sub = text.sentiment
        s_pol += pol  # variable utile pour calcul de polarité moyenne
        s_sub += sub  # variable utile pour calcul de subjectivité moyenne
        compteur += 1  # variable utile pour calcul de  moyenne
        dict['full_text'].append(status.full_text)  # on garde le text du tweet
        dict['date'].append(status.created_at)  # on garde la date du tweet
        # on garde le pseudo de l'utilisateur
        dict['screen_name'].append(status.user.screen_name)
        dict['polarity'].append(pol)  # on garde la polarité du tweet
        dict['subjectivity'].append(sub)  # on garde la subjectivité du tweet
        # on garde le nombre de likes
        dict['Likes'].append(status.favorite_count)
        # on garde le nombre de retweets
        dict['RTs'].append(status.retweet_count)
        dict['state'].append(state)  # on garde l'état
    for k in range(compteur):
        dict['mean_polarity'].append(s_pol/compteur)
        dict['mean_subjectivity'].append(s_sub/compteur)  # calculs de moyennes
    return (dict)


def store_dict_as_df(dict, filename):
    # fait store_dict_as_df(state_candidat(candidate_name, radius, state, c=100)))
    data = pd.DataFrame(dict)
    pd.DataFrame.to_json(data, filename, indent=2, orient='columns')


def mean_state_candidate(candidate_name, state, c, date):
    filename = 'database/state_candidate_tweets/' + str(state) +\
        "_" + str(candidate_name) + "_" + str(c) + date + ".json"
    file = open(filename, 'r')
    x = file.read()
    dict = json.loads(x)
    mean_pol = dict['mean_polarity']['0']
    mean_sub = dict['mean_subjectivity']['0']
    return ((mean_pol, mean_sub))


def simple_state_candidate(states, candidate_name, date):
    dic = pd.DataFrame(
        {'name': pd.Categorical([e for e in states.keys()]),
         'mean_pol': pd.Categorical([mean_state_candidate(candidate_name, 100, e, 100)[0] for e in states.keys()]),
         'mean_sub': pd.Categorical([mean_state_candidate(candidate_name, e, 100, date)[1] for e in states.keys()])
         })
    pd.DataFrame.to_json(dic, 'database/simples/simple_states_' +
                         str(candidate_name) + date + '.json', indent=2, orient='columns')


# fonction qui stocke sous format de fichier que l'on a nommé 'simple' les données voulues sur la popularité du 'candidate_name' dans les états states
def simple_candidate(states, candidate_name):
    # on crée le dictionnaire qu'on voudra stocker sous format json dans la database:
    dic = {}
    dic['name'] = []  # on veut stocker le nom de l'état
    # on veut stocker la polarité moyenne des tweets concernant le candidat dans l'état
    dic['mean_pol'] = []
    # on veut stocker la subjectivité moyenne des tweets concernant le candidat dans l'état
    dic['mean_sub'] = []
    for state in states.keys():
        # dictionnaire contenant tous les  100 tweets collectionnés dans l'état state concernant le candidat
        dict = state_candidate_dict(candidate_name, 100, state)
        filename = "database/state_candidate_tweets/" + state + "_" + candidate_name + "_" + \
            "100" + date.today().strftime("%d-%m-%Y") + ".json"  # on veut stocker ces 100 tweets et données dans la database dans le dossier state_candidate_tweets en conservant le nom de l'état, le candidat, le nb de tweets, la date (pour voir l'évolution en fonction du temps)
        # on stocke les 100 tweets de l'état dans le fichier filename
        store_dict_as_df(dict, filename)
        try:
            # si il n'y a pas d'erreur (càd si on a pu collectionner plus que zero tweets):
            dic['mean_pol'].append(dict['mean_polarity'][0])
            # on stocke dans le dico "dic" la polarité moyenne, subjectivité moyenne et le nom de l'état
            dic['mean_sub'].append(dict['mean_subjectivity'][0])
            # on stocke le nom de l'état en dernier pour que, si aucun tweet a été collectionné, le nom n'est pas ajouté
            dic['name'].append(state)
            # on print le nom de l'état pour que l'utilisateur voie la progression du stockage
            print(state)
        except:
            # s'il y a eu erreur: c'est qu'aucun tweet n'a pu être collecté
            print("pas de tweets au {}".format(state))
            # pour pouvoir afficher la carte on met 0 dans les infos de l'état
            dic['mean_pol'].append(0)
            dic['mean_sub'].append(0)
            dic['name'].append(state)
    filename = 'database/simples/simple_states_' + \
        str(candidate_name) + '.json'
    # on stocke le dico sous format json dans la database sous format qu'on appelle "simple"
    store_dict_as_df(dic, filename)


if __name__ == "__main__":

    departements = {"Ain": "Bourg-en-Bresse",
                    "Aisne":	"Laon",
                    "Allier": "Moulins",
                    "Alpes-de-Haute-Provence": "Digne-les-Bains",
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
                    "Cantal": "Aurillac",
                    "Charente": "Angoulême",
                    "Charente-Maritime": "La Rochelle",
                    "Cher": "Bourges",
                    "Corrèze": "Tulle",
                    "Corse-du-Sud": "Ajaccio",
                    "Haute-Corse": "Bastia",
                    "Côte-d'Or": "Dijon",
                    "Côtes-d'Armor": "St-Brieuc",
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
                    "Ille-et-Vilaine": "Rennes",
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

    liste = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Montpellier", "Strasbourg", "Bordeaux", "Lille", "Rennes", "Reims", "Toulon", "Saint-Etienne", "Le Havre", "Grenoble", "Dijon", "Angers", "Saint-Denis", "Villeurbanne",
             "Nîmes", "Clermont-Ferrand", "Aix-en-Provence", "Le Mans", "Brest", "Tours", "Amiens", "Limoges", "Annecy", "Boulogne-Billancourt", "Perpignan", "Metz", "Besançon", "Orléans", "Rouen", "Montreuil", "Argenteuil", "Mulhouse", "Caen"]

    state_capitals_dict = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
                           'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Colombus', 'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

    # pays_euro = pd.read_json(
    #        'C:/Users/Théo Fernet/Documents/CodingWeeks/haineword-1/database/name_to_iso.json')['name']

    #simple_state_candidate(state_capitals_dict, "Trump", "16-11-2022")
    #simple_candidate(state_capitals_dict, "Trump")
