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
            # print(model.probability(context, next_word))
            probability *= model.probability(context, next_word)
            # print(f"P({next_word} | {context}) = {probability}")
    return probability

def contains_slang_word(model, sentence, slang_word, threshold):
    probability = 1
    for i in range(len(sentence)):
        if sentence[i] == slang_word:
            left_context = sentence[max(0, i - model.n + 1):i]
            right_context = sentence[i+1:i+model.n]
            context = left_context + right_context
            next_word = sentence[i]
            # print(model.probability(context, next_word))
            probability *= model.probability(context, next_word)
            print(probability)
            # print(f"P({next_word} | {context}) = {probability}")
    return probability >= threshold

# def find_threshold_prob(model, slang_word, data):
#     probabilities = []
#     for sentence in data:
#         sentence_tokens = word_tokenize(sentence, engine="newmm")
#         for i in range(len(sentence_tokens)):
#             if sentence_tokens[i] == slang_word:
#                 left_context = sentence_tokens[max(0, i - model.n + 1):i]
#                 right_context = sentence_tokens[i+1:i+model.n]
#                 context = left_context + right_context
#                 next_word = sentence_tokens[i]
#                 probability = model.probability(context, next_word)
#                 probabilities.append(probability)
#     return np.quantile(probabilities, 0.01)

def attacut():
    df = pd.read_csv('phueakCleanUp.csv')
    df = df.dropna()
    token = [word_tokenize(i, engine="newmm") for i in df['tweet']]
    # for i in df['tweet']:
    #     words = tokenize(i)
    #     token.append(words)
    return token   


data = attacut()
model = NgramLanguageModel(2, data)

data_test_slang = pd.read_csv('phueaktest.csv')
data_test_notslang = pd.read_csv('phueaktest2.csv')

data_test_threshold = pd.read_csv('phueaktest3.csv')

def test_slang(model,data_test ,slang):
    prob_list = []
    for i in data_test["tweet_test"]:
        test_sentence = word_tokenize(i, engine="newmm")
        prob = slang_word_probability(model,test_sentence,slang)
        prob_list.append(prob)
    return prob_list

corre_test = test_slang(model,data_test_slang,"เผือก")
threshold = min(corre_test)
incorre_test = test_slang(model,data_test_notslang,"เผือก")

def test_threshold(data_test, threshold, slang):
    threshold -= threshold*0.01
    for i in data_test["tweet_test"]:
        test_sentence = word_tokenize(i, engine="newmm")
        prob = contains_slang_word(model, test_sentence, slang,threshold)
        # print(prob)
        if prob == True:
            print(f"{i} | มีคำแสลง ")
        elif prob == False:
            print(f"{i} | ไม่มีคำแสลง ")

print(threshold)


test_threshold(data_test_threshold,threshold,"เผือก")

# print(corre_test)
# print(incorre_test)
# fig, ax = plt.subplots()
# plt.plot(corre_test)
# plt.plot(incorre_test)
# plt.ylim([0.0009,0.001])
# plt.xlim(1,20)
# plt.show()
    
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
