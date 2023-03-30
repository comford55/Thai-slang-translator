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

def saveToCsv(list, name):
    with open(f'cleanUp-{name}.csv', 'w', newline='',encoding="UTF-8") as myfile:
        writer = csv.writer(myfile, delimiter=",")
        writer.writerow(['tweet'])
        for row in list:
            columns = [c.strip() for c in row.strip(', ').split(',')]
            writer.writerow(columns)

# df = pd.read_csv('tweet.csv')
# df = pd.read_csv('Phueak.csv')
# tweets = df['tweet'].dropna()
# # print(tweets)
# cleanTweets = cleanText(tweets)
# saveToCsv(cleanTweets)

# def saveMultipleToCsv():
#     name = ['เฉียบ', 'เม้าท์', 'เม้า', 'แห้ว', 'กาก', 'จกตา', 'จึ้ง', 'ซิง', 'ดือ', 'ติส', 'บ้ง', 'บิด', 'บูด', 'ปัง', 'มงลง', 'มองแรง', 'มู', 'ลำไย', 'สับ', 'หยอง']
    
#     for i in name:
#         df = pd.read_csv(f"E:/Optimized-Modified-GetOldTweets3-OMGOT/GetOldTweets3-0.0.10/slangwords/snscrape_words/thai-language-tweets-{i}.csv")
#         tweet = df['content']
#         cleanTweets = cleanText(tweet)
#         with open(f'cleanUp-{i}.csv', 'w', newline='',encoding="UTF-8") as myfile:
#             writer = csv.writer(myfile, delimiter=",")
#             writer.writerow(['tweet'])
#             for row in cleanTweets:
#                 columns = [c.strip() for c in row.strip(', ').split(',')]
#                 writer.writerow(columns)


name = ['เฉียบ', 'เม้าท์', 'เม้า', 'แห้ว', 'กาก', 'จกตา', 'จึ้ง', 'ซิง', 'ดือ', 'ติส', 'บ้ง', 'บิด', 'บูด', 'ปัง', 
        'มงลง', 'มองแรง', 'มู', 'ลำไย', 'สับ', 'หยอง']

df = pd.read_csv("E:/Optimized-Modified-GetOldTweets3-OMGOT/GetOldTweets3-0.0.10/slangwords/snscrape_words/thai-language-tweets-หยอง.csv")
tweets = df['content'].dropna()
cleanTweets = cleanText(tweets)
saveToCsv(cleanTweets, 'หยอง')