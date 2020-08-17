import time
import requests
import pandas as pd
from datetime import timezone
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import statistics


#June 16th 2015 the day the Trump's campaign officially began
startDate = "2015-06-16"

#current date
endDate = pd.to_datetime(time.time(), unit='s')

dates = pd.date_range(start=startDate, end=endDate)

#subreddit and query params which could be changed to alter the analysis
subreddit = "all"
query = "trump"
data = pd.DataFrame()

for date in dates:
    startS = int(date.replace(tzinfo=timezone.utc).timestamp())
    endS = int(startS + 86400) #doesnt account for leap seconds at the end of some dates, but overall doesnt have much of an impact on the final numbers

    try:
        #pulls the 1000 highest scoring comments from the indicated subreddit within the indicated timeframe
        comments_data = requests.get("https://api.pushshift.io/reddit/search/comment/?fields=body&sort_type=score",
                                 {"q":query,"before":endS ,"after": startS}).json()
    #known to throw an exception when the subreddit didnt exist on the date in question OR there were no comments that day which contained the query
    except Exception as e:
        print(str(e.__class__.__name__) + ": " + str(e))
    scores = []
    if(len(comments_data["data"]) > 0):
        for comment in comments_data["data"]:
            #compound sentiment score is a normalized weighted composite score for each comment
            vs = SentimentIntensityAnalyzer().polarity_scores(comment['body'])['compound']
            scores.append(vs)
        data = data.append(pd.DataFrame([[date,statistics.mean(scores)]], columns=["date","score"]))

data.to_csv("dataAll.csv")