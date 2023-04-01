import sys
sys.path.append('C:\\Users\\emaug\\Desktop\\CW\\pascoollesinsultes\\tweet_collect')
sys.path.append('C:\\Users\\emaug\\Desktop\\CW\\pascoollesinsultes\\tweet_analysis')

import tweepy
import geopy
from geopy.geocoders import Nominatim
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import pandas as pd
import os
from twitter_connection_setup import *
from datetime import date
import deepl
from urllib.request import urlopen
import json
from insultes import *
from name_to_leader import *

lang_ok=['bg', 
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


def quelle_langue(pays): #Donne l'ISO 639-1 de la langue officielle du pays
    data=pd.read_json('C:/Users/emaug/Desktop/CW/haineword/haineword/database/name_to_iso.json')
    a=pd.Index(data['name']).get_loc(pays)
    return str(data["iso"][a])
    
    
def isminor(langue): #Dit si une langue est parlée dans un seul pays en Europe. On se sert de ça pour augmenter le rayon si c'est le cas.
    data=pd.read_json('C:/Users/emaug/Desktop/CW/haineword/haineword/database/name_to_iso.json')
    a=pd.Index(data['iso']).get_loc(langue)
    return str(data["minor"][a])=="True" 
    

def traduit(texte, langue_src, langue_dest='en-gb'): #Traduit un texte en anglais avec DeepL
    auth_key='58735b0c-1c8b-21f8-8e88-7c9e9ce8e5c1:fx'
    translator=deepl.Translator(auth_key)
    resultat=translator.translate_text(texte, source_lang=langue_src, target_lang=langue_dest)
    return str(resultat)


def get_tweet_pays_euro(pays, c=100): #Stocke les tweets d'un pays européen
    
    langue=quelle_langue(pays)
    if not(langue in lang_ok):
       langue='en' #Si pas supportée par DeepL, on prend des tweets en anglais
    
    print(langue, pays)
    
    data=pd.read_json('C:/Users/emaug/Desktop/CW/haineword/haineword/database/europe.json')["features"]
    data_bis=pd.read_json('C:/Users/emaug/Desktop/CW/haineword/haineword/database/name_to_iso.json')
    
    a=pd.Index(data_bis['name']).get_loc(pays)
    long, lat= data[a]["properties"]["LON"] , data[a]["properties"]["LAT"]
    aire=data[a]["properties"]["AREA"] #en km²
    
    rayon=get_rayon(aire) #On considère le pays comme un cercle centré en LAT, LON (la database donne le LAT, LON du centre)
    
    api=twitter_setup()
    
    if isminor(langue):
        tweets=api.search_tweets("a", count=c, lang=langue, tweet_mode="extended")
    else:
        tweets=api.search_tweets("a", count=c, lang=langue, tweet_mode="extended", geocode="{},".format(
            lat) + "{},".format(long) + str(rayon) + "km")
    
    #filename=pays+'_'+str(c)+'_'+str(date.today().strftime("%d-%m-%Y"))+'.json'
    filename=pays+'_'+str(c)+'_16-11-2022.json'
    
    dict={}
    
    dict["original_text"]= []
    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity']=[]
    dict['subjectivity'] = []
    dict['mean_subjectivity']=[]
    dict['screen_name']=[]
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state']=[]
    dict['iso_639']=[]
    
    s_pol=0
    s_sub=0
    compteur=0
    for status in tweets:
        try:
            texte_traduit=traduit(status.full_text, langue)
        except:
            texte_traduit=traduit_blob(langue, status.full_text)
        text=TextBlob(texte_traduit)
        pol,sub=text.sentiment
        s_pol+=pol
        s_sub+=sub
        compteur+=1
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
        
    finalement=pd.DataFrame(dict)
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    pd.DataFrame.to_json(finalement, filename, indent=2, orient='columns')


def get_rayon(a): #Donne le rayno de recherche
    import numpy as np
    pi=np.pi
    r=(a/pi)**(0.5)
    return r
    
      
def geoloc(town): #Renvoie LAT, LON d'une ville
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode(town)
    return ((location.latitude, location.longitude))


def town_tweets(town, radius, c, l='en'): #Renvoie des tweets d'une ville
    api = twitter_setup()

    (lat, long) = geoloc(town)
    tweets = api.search_tweets(" ", count=c, lang=l, tweet_mode="extended", geocode="{},".format(
        lat) + "{},".format(long) + str(radius) + "km")
    return (tweets)


def town_polarity(town): #Renvoie la polarité moyenne de tweets
    tweets = town_tweets(town, 100)
    polarity_moy = 0
    n = len(tweets)
    for tweet in tweets:
        text = TextBlob(tweet.full_text, pos_tagger=PatternTagger(),
                        analyzer=PatternAnalyzer())
        (pol, sub) = text.sentiment
        polarity_moy += pol
    return (polarity_moy/n)


def simple_df(states, langue, d1=date.today().strftime("%d-%m-%Y"), d2=date.today().strftime("%d-%m-%Y")): #Stocke un dictionnaire contenant juste les infos nécessaires à la carte
    dic = pd.DataFrame(
        {'name': pd.Categorical([e for e in states.keys()]),
         'mean_pol': pd.Categorical([mean_polarity(e, d1=d1, d2=d2) for e in states.keys()]),
         'mean_sub': pd.Categorical([mean_subjectivity(e, d1=d1, d2=d2) for e in states.keys()])
         })
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    pd.DataFrame.to_json(dic, 'simple_'+langue+'.json', indent=2, orient='columns')
   

def simple_df_euro(states, d=date.today().strftime("%d-%m-%Y")): #Stocke un dictionnaire contenant juste les infos nécessaires à la carte europe
    dic = pd.DataFrame(
        {'name': pd.Categorical([e for e in states]),
         'mean_pol': pd.Categorical([mean_polarity(e, da=d) for e in states]),
         'mean_sub': pd.Categorical([mean_subjectivity(e, da=d) for e in states])
         })
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    pd.DataFrame.to_json(dic, 'simple_'+'europe'+'.json', indent=2, orient='columns') 


def simple_leader_euro(states, d=date.today().strftime("%d-%m-%Y")): #Stocke un dictionnaire contenant juste les infos nécessaires à la carte insultes
    dic = pd.DataFrame(
        {'name': pd.Categorical([e for e in states]),
         'mean_pol': pd.Categorical([mean_polarity(e) for e in states]),
         'mean_sub': pd.Categorical([mean_subjectivity(e) for e in states])
         })
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    pd.DataFrame.to_json(dic, 'simple_leader_'+'europe'+'.json', indent=2, orient='columns') 


def store_tweets_usa(state, c=100, langue='en'): #Pour un état donné par state, enregistre un .json avec les colonnes (voir dans la définition)
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    filename=state+'_'+str(c)+'_'+str(date.today().strftime("%d-%m-%Y"))+'.json'
    tweets=town_tweets(state_capitals_dict[state], 25, c, langue)
    
    dict={}
    
    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity']=[]
    dict['subjectivity'] = []
    dict['mean_subjectivity']=[]
    dict['screen_name']=[]
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state']=[]
    
    s_pol=0
    s_sub=0
    compteur=0
    for status in tweets:
        if langue=='fr':
            text = TextBlob(status.full_text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        elif langue=='en':
            text=TextBlob(status.full_text)
        pol,sub=text.sentiment
        s_pol+=pol
        s_sub+=sub
        compteur+=1
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
    
    
    data=pd.DataFrame(dict)
    pd.DataFrame.to_json(data, filename, indent=2, orient='columns')
        

def store_tweets_fr(state, c=100, langue='fr'): #Pour un département donné par state, enregistre un .json avec les colonnes (voir dans la définition)
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    filename=state+'_'+str(c)+'_'+str(date.today().strftime("%d-%m-%Y"))+'.json'
    
    rayon=25
    if state in ['Paris', 'Seine-et-Marne', 'Yvelines', 'Seine-Saint-Denis', 'Val-de-Marne', "Val-d'Oise", "Hauts-de-Seine"]:
        rayon=5 # Car les départements d'Ile de France sont très serrés
    tweets=town_tweets(departements[state], rayon, c, langue)
    
    dict={}
    
    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity']=[]
    dict['subjectivity'] = []
    dict['mean_subjectivity']=[]
    dict['screen_name']=[]
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state']=[]
    
    s_pol=0
    s_sub=0
    compteur=0
    for status in tweets:
        if langue=='fr':
            text = TextBlob(status.full_text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        elif langue=='en':
            text=TextBlob(status.full_text)
        pol,sub=text.sentiment
        s_pol+=pol
        s_sub+=sub
        compteur+=1
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
    
    
    data=pd.DataFrame(dict)
    pd.DataFrame.to_json(data, filename, indent=2, orient='columns')

        
def mean_polarity(state, c=100, d1='17-11-2022', d2=date.today().strftime("%d-%m-%Y")): #Renvoie la polarité moyenne de tweets
    #file='C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+state+'_merge_'+str(c)+'_'+str(d1)+'_ET_'+str(d2)+'.json'
    file='C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+state+'_leader_'+str(c)+'_'+str(d1)+'.json'
    data=pd.read_json(file)
    s=0
    n=len(data.polarity)
    if n==0:
        return 0
    for elt in data.polarity:
        s+=elt
    return s/n


def mean_subjectivity(state, c=100,d1='17-11-2022', d2=date.today().strftime("%d-%m-%Y")): #Renvoie la subjectivité moyenne de tweets
    #file='C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+state+'_merge_'+str(c)+'_'+str(d1)+'_ET_'+str(d2)+'.json'
    file='C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+state+'_leader_'+str(c)+'_'+str(d1)+'.json'
    data=pd.read_json(file)
    s=0
    n=len(data.subjectivity)
    if n==0:
        return 0
    for elt in data.subjectivity:
        s+=elt
    return s/n


def merge(state, date1, date2, c1=100, c2=100): #Donné un état, la date de création de la database 1 et celle de la database 2, fusionne les fichiers de stockage des tweets pour obtenir un fichier avec 200 tweets
    dicm={}
    f=open('C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+state+'_'+str(c1)+'_'+str(date1)+'.json')
    g=open('C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+state+'_'+str(c2)+'_'+str(date2)+'.json')
    dic1=json.load(f)
    dic2=json.load(g)
    k=list(dic1.keys())
    filename=state+'_merge_'+str(c1+c2)+'_'+date1+'_ET_'+date2+'.json'
    
    for cle in k:
        n1=len(dic1[cle])
        n2=len(dic1[cle])
        dicm[cle]=[]
        for i in range(max(n1,n2)):
            try:
                dicm[cle].append(dic1[cle][str(i)])
            except:
                continue
            try:
                dicm[cle].append(dic2[cle][str(i)])
            except:
                continue
    
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    data=pd.DataFrame(dicm)
    pd.DataFrame.to_json(data, filename, indent=2, orient='columns')
    

def traduit_blob(src_lang,text): #Traduit le texte avec TextBlob en anglais
    text_blob=TextBlob(text)
    resultat=text_blob.translate(from_lang=src_lang,to='en')  
    return str(resultat)
       
       
def get_tweet_pays_euro_blob(pays, c=100): #Store les tweets en les traduisant avec TextBlob
    
    langue=quelle_langue(pays)
    
    print(langue, pays)
    
    data=pd.read_json('database/europe.json')["features"]
    data_bis=pd.read_json('database/name_to_iso.json')
    
    a=pd.Index(data_bis['name']).get_loc(pays)
    long, lat= data[a]["properties"]["LON"] , data[a]["properties"]["LAT"]
    aire=data[a]["properties"]["AREA"] #en km²
    
    rayon=get_rayon(aire) #On considère le pays comme un cercle centré en LAT, LON (la database donne le LAT, LON du centre)
    
    api=twitter_setup()
    
    dict={}
    
    dict["original_text"]= []
    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity']=[]
    dict['subjectivity'] = []
    dict['mean_subjectivity']=[]
    dict['screen_name']=[]
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state']=[]
    dict['iso_639']=[]
    
    filename='database/'+pays+'_'+str(c)+'_'+str(date.today().strftime("%d-%m-%Y"))+'_blob.json'
    
    if isminor(langue):
        try:
            tweets=api.search_tweets(" ", count=c, lang=langue, tweet_mode="extended") #On prend pas en compte la geoloc
        except:
            pd.DataFrame.to_json(pd.DataFrame(dict), filename, indent=2, orient='columns') #Si jamais la langue est pas supportée par Twitter, on ne prend rien
            return None
    else:
        tweets=api.search_tweets(" ", count=c, lang=langue, tweet_mode="extended", geocode="{},".format(
            lat) + "{},".format(long) + str(rayon) + "km") #On doit prendre en compte la geoloc


    s_pol=0
    s_sub=0
    compteur=0
    for status in tweets:
        if langue in lang_ok:
            try:
                texte_traduit=traduit(status.full_text, langue)
            except:
                texte_traduit=traduit_blob(langue, status.full_text)
        else:
            texte_traduit=traduit_blob(langue, status.full_text)
        text=TextBlob(texte_traduit)
        pol,sub=text.sentiment
        s_pol+=pol
        s_sub+=sub
        compteur+=1
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
        
    finalement=pd.DataFrame(dict)
    pd.DataFrame.to_json(finalement, filename, indent=2, orient='columns')  


def insulte_ou_pas(tweet): #Dit si le tweet contient une insulte et combien
    c=0 #Compte les insultes du tweet
    txtblob=TextBlob(str(tweet))
    mots=list(txtblob.words)
    l_insultes=INSULTES["RECORDS"] #C'est une liste de dict
    n=len(l_insultes)
    for k in range(n):
        for mot in mots:
            if mot.lower()==l_insultes[k]["word"]: #on met le mot en minuscule au cas où le mec insulte en majuscule
                c+=1
    return c


def insulte_pays(pays, date, c=100): #Pour un pays donné, renvoie le nombre d'insultes moyen par tweet
    #file='C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+pays+'_merge_'+str(200)+'_14-11-2022'+'_ET_'+'16-11-2022'+'.json'
    file='C:/Users/emaug/Desktop/CW/haineword/haineword/database/'+pays+'_'+str(c)+'_'+str(date)+'.json'
    data=pd.read_json(file)
    s=0
    n=len(data.full_text)
    if n==0:
        return 0
    for elt in data.full_text:
        s+=insulte_ou_pas(elt)
    return s/n


def crée_insulte_simple(dic, date, nom): #Crée un dictionnaire avec uniquement les infos nécessaires à la carte insultes
    dic = pd.DataFrame(
        {'name': pd.Categorical([e for e in dic.keys()]),
         'mean_insultes': pd.Categorical([insulte_pays(e, date) for e in dic.keys()]),
         })
    pd.DataFrame.to_json(dic, 'database/simple_insulte_'+nom+'.json', indent=2, orient='columns')    
    
    
def get_tweet_dirigeant_euro(pays, c=100): #Pour un pays donné, renvoie 100 tweets associés à leur chef d'Etat
    
    langue='en'
    # langue=quelle_langue(pays)
    if not(langue in lang_ok):
       langue='en' #Si pas supportée par DeepL, on prend des tweets en anglais
    
    print(langue, pays)
    
    data=pd.read_json('C:/Users/emaug/Desktop/CW/haineword/haineword/database/europe.json')["features"]
    data_bis=pd.read_json('C:/Users/emaug/Desktop/CW/haineword/haineword/database/name_to_iso.json')
    
    a=pd.Index(data_bis['name']).get_loc(pays)
    long, lat= data[a]["properties"]["LON"] , data[a]["properties"]["LAT"]
    aire=data[a]["properties"]["AREA"] #en km²
    
    rayon=get_rayon(aire) #On considère le pays comme un cercle centré en LAT, LON (la database donne le LAT, LON du centre)
    
    api=twitter_setup()
    
    query=DIC_LEADER[pays]
    tweets=api.search_tweets(query, count=c, lang=langue, result_type='recent', tweet_mode="extended")

    
    filename=pays+'_leader_'+str(c)+'_'+str(date.today().strftime("%d-%m-%Y"))+'.json'
    
    dict={}
    
    dict["original_text"]= []
    dict['full_text'] = []
    dict['date'] = []
    dict['polarity'] = []
    dict['mean_polarity']=[]
    dict['subjectivity'] = []
    dict['mean_subjectivity']=[]
    dict['screen_name']=[]
    dict['Likes'] = []
    dict['RTs'] = []
    dict['state']=[]
    dict['iso_639']=[]
    
    s_pol=0
    s_sub=0
    compteur=0
    for status in tweets:
        #try:
        #    texte_traduit=traduit(status.full_text, langue)
        #except:
        text=TextBlob(str(status.full_text))
        texte_traduit=str(text)
        pol,sub=text.sentiment
        s_pol+=pol
        s_sub+=sub
        compteur+=1
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
        
    finalement=pd.DataFrame(dict)
    os.chdir('C:/Users/emaug/Desktop/CW/haineword/haineword/database')
    pd.DataFrame.to_json(finalement, filename, indent=2, orient='columns')

    
    
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
    
    pays_euro=pd.read_json('database/name_to_iso.json')['name']
    
    crée_insulte_simple(state_capitals_dict, '14-11-2022', 'usa')


    
    
    

    
    
    

    
        
    
    
