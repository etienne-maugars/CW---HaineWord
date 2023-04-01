# HAINE WORDS

# Description globale du projet


Ce projet a pour but d'évaluer la positivité et la subjectivité des tweets tout en prenant en compte la position géographique de ces derniers. L'objectif sera donc de pouvoir obtenir une carte de l'Europe et des Etats-Unis avec pour chaque pays une positivité moyenne des tweets, la subjectivité ainsi que le nombre d'insultes moyen.

On tentera également d'analyser la popularité des leaders des pays européens en récoltant la positivité moyenne de ces derniers dans leur pays. On généralisera également cela avec certaines entreprises.

# Comment lancer l'application :
On ouvre le dossier `Application` et on lance le programme `app.py`. On clique ensuite sur le lien que renvoie le programme. On arrive sur un site et on selectionne alors les cartes dont on en besoin !


# Liste des fonctionnalités 

- Le dossier 'Application' contient les éléments nécessaires à la mise en place du site.
  + On lance l'application avec le programme `app.py`, et en cliquant sur le lien que renvoie la fonction.
  + Le dossier 'pages' contient les différentes pages de l'application.
  + Le dossier 'assets' contient les ressources numériques (images, fichier css) nécessaire à l'esthétique du site.

- On retrouve dans le dossier 'database' l'ensemble des tweets récoltés sous forme de .json et regroupés par départements français ou états américains ou pays européens.

- Le dossier 'tweet_collect' contient les fonctionnalités indispensables pour pouvoir récupérer les tweets. En particulier on retrouve :
   + `twitter_connection_setup.py` qui est une fonction d'initialisation de l'API Twitter
   + `storage.py` qui regroupe tous les tweets ainsi que leurs données (text, nombre de likes, retweets, clé primaire) sous forme de tableau.
   + `collect.py` qui contient plusieurs fonctionnalités qui seront nécessaires à la constitution des cartes. Parmi elles, on a :
      - quelle_langue() : donne la langue d'un tweet
      - traduit() : traduit un tweet d'une langue quelconque en anglais
      - get_tweet_pays_euro() : renvoie les tweets pour un pays européen donné
      - geoloc() : donne la localisation d'une ville
      - town_tweets() : liste l'ensemble des tweets provenant d'une même ville
      - town_polarity() : donne la polarité moyenne des tweets d'une même ville
      - store_tweets_usa() : pour un état américain donné, renvoie un .json avec les colonnes
      - store_tweets_fr() : idem que la fonction précédente mais avec les départements français
      - mean_polarity() et mean_subjectivity()
    En plus des fonctionnalités présentes dans collect.py, on retrouve les dictionnaires 'departements' et 'state_capitals_dict' listant respectivement les départements français et les capitales de chaque état américains

- Le dossier 'Cartes' contient l'ensemble des fonctionnalités permettant d'afficher une carte, notamment avec le fichier `map.py`, on retrouve alors les fonctions suivantes : 
    + map_usa_sub()
    + map_usa_pol()
    + map_usa_insultes()
    + map_fr_sub()
    + map_fr_pol()
    + map_europe_sub()
    + map_europe_pol()
    + map_europe_insulte()
    + map_europe_leader_sub()
    + map_europe_leader_pol()
    + map_europe_leader_insulte()
    + map_fr_merge_pol()
    + map_fr_merge_sub()
    + map_fr_merge_insulte()

- Le dossier 'tweet_collection' contient quant à lui 2 fichiers :
  + `twitter_connection_setup.py` vu précédemment dans le fichier 'tweet_collect'
  + `credentials.py` qui contient les "Consumer API keys et Access token & access token secret" nécéssaires pour se connecter    

- Le dossier 'tweet_connection' contient des fichiers vus auparavant et les clés d'authentification (les comptes ont été créés uniquement pour ce projet et les clés ne sont donc pas sensibles.)

# Liste des modules

Pour pouvoir réaliser ce projet, nous avons du importer plusieurs modules. Voyons comment nous y avons accès et un exemple d'usage pour chaque module.

## tweepy 

### Installation 

On utilise le pip du gestionnaire de packages pour installer tweepy.

```bash
pip install tweepy
```
### Usage

```python
import tweepy

 # Authentification et accès en utilisant les clés :
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Renvoie l'API avec une authentification:
    api = tweepy.API(auth)
```

## pandas

### Installation

```bash
pip install pandas
```
### Usage

```python
import pandas as pd

#Renvoie un tableau contenant toutes les infos classées d'un .json
df = pd.read_json('data_10_11_2020.json')
print(df)

```
### dash

### Installation
```pip install dash
pip install dash_bootstrap_components
```

## geopy

### Installation

```bash
pip install geopy
```
### Usage

```python
import geopy
from geopy.geocoders import Nominatim

#Renvoie la latitude et la longitude pour une ville donnée 
geolocator = Nominatim(user_agent="MyApp")
location = geolocator.geocode(town)
latitude, longitude = location.latitude , location.longitude

```

## textblob

### Installation

```bash
pip install textblob
```
### Usage

```python
from textblob import TextBlob

animals = TextBlob("cat dog octopus")
WordList = animals.words #Renvoie une liste avec les mots séparés
WordListPlural = animals.words.pluralize() #Renvoie une liste avec les mots au pluriel
testimonial = TextBlob("What great fun!")
Sentiment = testimonial.sentiment #Renvoie un tuple contenant la polarité et la subjectivité 

```

## os

### Usage

```python
import os
os.mkdir("d:\\newdir") #Crée un nouveau répertoire
print(os.getcwd()) #Renvoie le Current Work Directory (CWD) du fichier

```

## deepl

### Installation

```bash
pip install deepl
```
### Usage

```python
import deepl

#Traduit un texte qui est dans la langue 'langue_src' en la langue 'langue_dest'
translator=deepl.Translator(auth_key)
resultat=translator.translate_text(texte, source_lang=langue_src, target_lang=langue_dest)
print(str(resultat))

```

## plotly.express

### Installation

```bash
pip install plotly.express
```
### Usage

```python
import plotly.express as px
px.choropleth() #Commande permettant d'afficher les cartes 

```














