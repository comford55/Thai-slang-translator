import os
import pandas as pd
from regexCharacter import cleanText
from attacut import tokenize

text = input("Enter your word : ")
file_path = f'../slangwords/WordFromTweetCSV/{text}.csv'
existed = os.path.exists(file_path)
if not existed:
    os.system(f'python cli.py -s {text} -l th --limit 100 -o {file_path} --csv')
# existed = os.path.exists(f'./{text}.csv')

df = pd.read_csv(file_path)
tweet = df['tweet']
regex = cleanText(tweet)
print(regex)
# token = [tokenize(i) for i in regex]
# for word in token:
#     print(word)




