import json
import pandas as pd
from twitter_connection_setup import *

api = twitter_setup()

def store_tweets(tweets,filename):
    pd.DataFrame.to_json(tweets,filename)

def create_dataframe(tweets):
    df2 = pd.DataFrame(
    {
        "full_text": pd.Categorical([tweet.text for tweet in tweets]),
        "name": pd.Categorical([tweet.user.name for tweet in tweets]),
        "favorite_count": pd.Categorical([tweet.favorite_count for tweet in tweets]),
        "retweet_count": pd.Categorical([tweet.retweet_count for tweet in tweets]),
        "created_at": pd.Categorical([tweet.created_at for tweet in tweets]),
        "id": pd.Categorical([tweet.id for tweet in tweets]),
    })
    return df2
    
if __name__ == "__main__":
    tweets = api.search_tweets('le',lang='fr', count=200)
    df2 =create_dataframe(tweets)
    store_tweets(df2,"tweet_français.json")
