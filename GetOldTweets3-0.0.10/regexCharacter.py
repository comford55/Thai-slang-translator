import csv
import re
import pandas as pd


# clean text from csv keep only thai alphabet
def cleanText(tweets):
    clean = []
    for i in tweets:
        regex = re.sub('[^\u0E00-\u0E7F]', '', i)
        clean.append(regex)
    return clean

def saveToCsv(list):
    with open('PhueakCleanUp.csv', 'w', newline='',encoding="UTF-8") as myfile:
        writer = csv.writer(myfile, delimiter=",")
        writer.writerow(['tweet'])
        for row in list:
            columns = [c.strip() for c in row.strip(', ').split(',')]
            writer.writerow(columns)

# df = pd.read_csv('tweet.csv')
df = pd.read_csv('Phueak.csv')
tweets = df['tweet'].dropna()
# print(tweets)
cleanTweets = cleanText(tweets)
saveToCsv(cleanTweets)