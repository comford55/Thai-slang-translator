from collections import Counter
import pandas as pd
import csv

def getCandidate(token):
    # flatten the nested list
    words = [j for i in token for j in i]

    # count the words
    word_count = Counter(words)

    # keep words with count more than 5
    candidate = {w for w, c in word_count.items() if c > 5}

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

def getThaiWordList():
    with open('lexitron.txt', 'r', encoding="UTF-8") as file:
        thaiwords = set(i.rstrip() for i in file)
    return thaiwords

df = pd.read_csv('tweetTokenization.csv',sep='\t')
token = [i.split(',') for i in df['words']]
print('Tokenize words = ', len(token))

# get thai dictionary
thaiwords = getThaiWordList()
print('Thai dictionary words = ', len(thaiwords))

candidates = getCandidate(token)
print('Candidate words = ', len(candidates))

# get words not within thai dictionary
wordsInThailist = thaiwords.intersection(candidates)
wordsCandidate = candidates - wordsInThailist

def saveCandidateWords():
    with open('candidateWords.csv', 'w',newline='',encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(['candidate'])
        for row in wordsCandidate:
            columns = [c.strip() for c in row.strip(', ').split(',')]
            writer.writerow(columns)