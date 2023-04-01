import tweepy
# We import our access keys:
import os 
import sys
sys.path.append(os.path.join(os.getcwd(),'tweet_connection'))
if True:
    from credentials import *


def twitter_setup(): #Initialise l'API
    """
    Utility function to setup the Twitter's API
    with an access keys provided in a file credentials.py
    :return: the authentified API
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api
