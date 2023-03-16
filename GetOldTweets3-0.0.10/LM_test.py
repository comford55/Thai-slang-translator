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
from pythainlp.tokenize import word_tokenize

class SlangLanguageModel:
    def __init__(self, n, data, max_context_size):
        self.n = n
        self.model = defaultdict(Counter)
        self.vocab = set()
        for sentence in data:
            for i in range(len(sentence)):
                # Only use contexts up to max_context_size
                for context_size in range(1, max_context_size+1):
                    left_context = tuple(sentence[max(0, i - context_size + 1):i])
                    right_context = tuple(sentence[i+1:i+context_size])
                    context = left_context + right_context
                    next_word = sentence[i]
                    self.model[context][next_word] += 1
                    self.vocab.add(next_word)

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
        # if context not in self.model:
        #     return self.min_probability()  # Return a probability of 0 for unknown context
        context_counts = sum(self.model[context].values())
        smoothing_value = 1
        # Check if next_word is in the vocabulary
        # if next_word not in self.model[tuple()]:
        #     return self.min_probability()
        # Calculate probability using smoothing
        return (self.model[context][next_word] + smoothing_value) / (context_counts + smoothing_value * len(self.model))

    def slang_word_probability(self, sentence, slang_word):
        sentence_tokens = word_tokenize(sentence)
        for i in range(len(sentence_tokens)):
            if sentence_tokens[i] == slang_word:
                left_context = sentence_tokens[max(0, i - 2):i]
                right_context = sentence_tokens[i+1:i+3]
                context = left_context + right_context
                next_word = sentence_tokens[i]
                probability = self.probability(context, next_word)
                print(f"P({next_word} | {context}) = {probability}")
                return probability
        return 0

def attacut():
    df = pd.read_csv('phueakCleanUp.csv')
    df = df.dropna()
    token = [word_tokenize(i, engine="newmm") for i in df['tweet']]
    # for i in df['tweet']:
    #     words = tokenize(i)
    #     token.append(words)
    return token   


data = attacut()
model = SlangLanguageModel(2, data,max_context_size=4)

data_test_slang = pd.read_csv('phueaktest.csv')
data_test_notslang = pd.read_csv('phueaktest2.csv')

def test_slang(model,data_test ,slang):
    prob_list = []
    for i in data_test["tweet_test"]:
        prob = model.slang_word_probability(i,slang)
        prob_list.append(prob)
    return prob_list

corre_test = test_slang(model,data_test_slang,"เผือก")
incorre_test = test_slang(model,data_test_notslang,"เผือก")
# print(corre_test)
# print(incorre_test)
# print(corre_test)
# fig, ax = plt.subplots()
plt.plot(corre_test)
plt.plot(incorre_test)
plt.ylim([0.00039,0.0004])
plt.xlim(1,14)
plt.show()
    
    
# print(tokenize(data_test_slang["tweet_test"]))

def getProb(data_test ,slang):
    # prob_list = []
    test_sentence = word_tokenize(data_test, engine="newmm")
    prob = slang_word_probability(model,test_sentence,slang)
    # prob_list.append(prob)
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
