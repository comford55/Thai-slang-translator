from gensim.models import Word2Vec
import pandas as pd
from pythainlp.tag import pos_tag
from attacut import tokenize
from pythainlp.corpus import thai_stopwords


df = pd.read_csv('phueaktest.csv')
df = df.dropna()
token = [tokenize(i) for i in df['tweet_test']]

# model = Word2Vec(token)
# print(model)

# words = list(model.wv.index_to_key)
# print(words)

# print(model.wv.most_similar('นก'))

for i in token:
    print(pos_tag(i, corpus='orchid_ud'))

stopwords = list(thai_stopwords())

rem_stopwords = [[j for j in i if j not in stopwords] for i in token]

# rem_stopwords = []
# for i in token:
#     new_i = []
#     for j in i:
#         if j not in stopwords:
#             new_i.append(j)
#     rem_stopwords.append(new_i)


# for i in rem_stopwords:
#     print(pos_tag(i, corpus='orchid_ud'))