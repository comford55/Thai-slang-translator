import csv
from collections import Counter
import pandas as pd
from attacut import Tokenizer, tokenize

def attacut():
    df = pd.read_csv('tweetCleanUp.csv')
    df = df.dropna()
    token = [tokenize(i) for i in df['tweet']]
    # for i in df['tweet']:
    #     words = tokenize(i)
    #     token.append(words)
    return token    

def saveToCsv(token):
    with open('tweetTokenization.csv', 'w', newline='',encoding="UTF-8") as myfile:
        writer = csv.writer(myfile, delimiter=",")
        writer.writerow(['words'])
        for row in token:
            writer.writerow(row)    

def getCandidate(token):
    # flatten the nested list
    words = [j for i in token for j in i]

    # count the words
    word_count = Counter(words)

    # keep words with count more than 5
    candidate = [w for w, c in word_count.items() if c > 5]

    return candidate

# find co-occurrences
def getCooccurrences(candidate, token):
    co_occur = {}
    for w in candidate:
        temp = []
        for i in token:
            if w in i:
                temp.append([x for x in i if x != w])
        co_occur[w] = list(set([tuple(i) for i in temp]))
    return co_occur

def save_co_occur(co_occur):
    with open('co_occur.csv', 'w', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(['words', 'co-occur'])
        for key, value in co_occur.items():
            writer.writerow([key, value])

token = attacut()
saveToCsv(token)
    





