import math
from collections import defaultdict
from collections import Counter
import pandas as pd
import numpy as np
from attacut import Tokenizer, tokenize
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from math import log, exp
import matplotlib.ticker as ticker

class NgramLanguageModel:
    def __init__(self, n, data):
        self.n = n
        self.model = defaultdict(Counter)
        for sentence in data:
            for i in range(len(sentence)):
                left_context = tuple(sentence[max(0, i - n + 1):i])
                right_context = tuple(sentence[i+1:i+n])
                context = left_context + right_context
                next_word = sentence[i]
                self.model[context][next_word] += 1

    def min_probability(self):
        min_prob = 1
        for context in self.model.keys():
            for word in self.model[context].keys():
                prob = self.probability(context, word)
                if prob < min_prob:
                    min_prob = prob
        return min_prob/4

    def probability(self, context, next_word):
        context = tuple(context)
        context_counts = sum(self.model[context].values())
        smoothing_value = 1
        return (self.model[context][next_word] + smoothing_value) / (context_counts + smoothing_value * len(self.model))

    

def slang_word_probability(model, sentence, slang_word):
    probability = 1
    for i in range(len(sentence)):
        if sentence[i] == slang_word:
            left_context = sentence[max(0, i - model.n + 1):i]
            right_context = sentence[i+1:i+model.n]
            context = left_context + right_context
            next_word = sentence[i]
            probability *= model.probability(context, next_word)
    return probability

def attacut():
    df = pd.read_csv('phueakCleanUp.csv')
    df = df.dropna()
    token = [tokenize(i) for i in df['tweet']]
    # for i in df['tweet']:
    #     words = tokenize(i)
    #     token.append(words)
    return token   


data = attacut()
model = NgramLanguageModel(2, data)

data_test_slang = pd.read_csv('phueaktest.csv')
data_test_notslang = pd.read_csv('phueaktest2.csv')

def test_slang(model,data_test ,slang):
    prob_list = []
    for i in data_test["tweet_test"]:
        test_sentence = tokenize(i)
        prob = slang_word_probability(model,test_sentence,slang)
        prob_list.append(prob)
    return prob_list

corre_test = test_slang(model,data_test_slang,"เผือก")
# incorre_test = test_slang(model,data_test_notslang,"เผือก")

# print(incorre_test)
print(corre_test)
# fig, ax = plt.subplots()
plt.plot(corre_test)
plt.plot(incorre_test)
plt.ylim([0.00125,0.00140])
plt.xlim(1,14)
# ax.set_xlabel('Data Point Index')
# ax.set_ylabel('Data Value')
# formatter = ScalarFormatter(useMathText=True)
# formatter.set_powerlimits((-3, 4))
# ax.yaxis.set_major_formatter(formatter)
plt.show()
    
    
# print(tokenize(data_test_slang["tweet_test"]))

def getProb():
    prob = 0
    return prob






# Calculate the probability of a word given its context

# sentence = tokenize("โลกนี้มีคนขี้เผือกแบบอิชั้นอยู่")
# prob1 = slang_word_probability(model, sentence,"เผือก")
# print("Probability of sentence:", prob1)



# print(prob1/(prob1+prob2+prob3+prob4+prob5+prob6)) 
# print(prob2/(prob1+prob2+prob3+prob4+prob5+prob6)) 
# print(prob3/(prob1+prob2+prob3+prob4+prob5+prob6))
# print(prob4/(prob1+prob2+prob3+prob4+prob5+prob6)) 
# print(prob5/(prob1+prob2+prob3+prob4+prob5+prob6)) 
# print(prob6/(prob1+prob2+prob3+prob4+prob5+prob6))
