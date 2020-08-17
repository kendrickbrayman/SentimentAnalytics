import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from datetime import datetime

def getSentiment(text):
    return SentimentIntensityAnalyzer().polarity_scores(text)['compound']

def convertTime(text):
    return datetime.strptime(text).strftime("%Y-%m-%d")

with open("tweets.json", encoding="utf-8") as jsonf:
    tweets = json.load(jsonf)

data = pd.DataFrame()
for tweet in tweets:
    vs = getSentiment(tweet["text"])
    date = convertTime(tweet["created_at"])
    data = data.append(
        pd.DataFrame([[vs,date]], columns=["score","date"], index=tweet["id_str"])
        )
indexNames = data[data['score'] == 0].index
data.drop(indexNames, inplace=True)
data.to_csv("tweetScore.csv")

