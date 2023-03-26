import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter

query = "lang:th"
scraper = sntwitter.TwitterSearchScraper(query)

tweets = []
n_tweets = 100

for i, tweet in tqdm(enumerate(scraper.get_items()), total=n_tweets):
  data = [tweet.date, tweet.content]
  tweets.append(data)
  if i > n_tweets:
    break

tweet_df = pd.DataFrame(tweets, columns=["date", "content"])
tweet_df.to_csv("thai-language-tweets.csv", index=False)