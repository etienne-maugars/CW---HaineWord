import json
import pandas as pd
import numpy as np
# ETAPE 1


def store_tweets(tweets, filename): #Stocke les tweets
    pd.DataFrame.to_json(tweets, filename)


# sauvegarder: Text, date, id_tweet, hashtags, autres
# ref à quel candidat

def df(tweets):
    dict = {}
    dict['tweet_textual_content'] = []
    dict['Date'] = []
    dict['hashtags'] = []
    dict['id_tweet'] = []
    dict['Likes'] = []
    dict['RTs'] = []
    for status in tweets:
        dict['tweet_textual_content'].append(status.text)
        dict['Date'].append(status.created_at)
        dict['hashtags'].append(status.entities['hashtags'])
        dict['id_tweet'].append(status.id)
        dict['Likes'].append(status.favorite_count)
        dict['RTs'].append(status.retweet_count)
    return (pd.DataFrame(dict))


if __name__ == "__main__":
    data = df(Sb.timeline("@KDTrey5"))
    print(data)
    rt_max = np.max(data['RTs'])
    rt = data[data.RTs == rt_max].index[0]

    # Max RTs:
    print("The tweet with more retweets is: \n{}".format(
        data['tweet_textual_content'][rt]))
    print("Number of retweets: {}".format(rt_max))