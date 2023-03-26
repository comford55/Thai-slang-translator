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
import csv

import re
from collections import defaultdict, Counter
import re
from collections import defaultdict, Counter

class NgramLanguageModel:
    def __init__(self, max_n, data, slangword=None):
        self.max_n = max_n
        self.models = {}
        for n in range(1, self.max_n+1):
            model = defaultdict(Counter)
            for sentence in data:
                for i in range(len(sentence)):
                    if sentence[i] in slangword:
                        left_context = tuple(sentence[max(0, i - n + 1):i])
                        left_left_context = tuple(sentence[max(0, i - n + 2):i])
                        right_context = tuple(sentence[i+1:i+n])
                        right_right_context = tuple(sentence[i+2:i+n])
                        context = left_context + right_context
                        next_word = sentence[i]
                        model[left_context][next_word] += 1
                        model[right_context][next_word] += 1
                        model[left_left_context][left_context] += 1
                        model[right_right_context][right_context] += 1
                        model[context][next_word] += 1
            self.models[n] = model
        self.slangword = slangword

    # def probability(self, context, next_word):
    #     probabilities = []
    #     for n in range(1, len(context)+2):
    #         if n in self.models:
    #             model = self.models[n]
    #             context_counts = 0
    #             probability_sum = 0
    #             for c in model.keys():
    #                 if len(context) >= n-1 and c[-1] == context[-1]:
    #                     context_counts += sum(model[c].values())
    #                     smoothing_value = 1
    #                     probability = (model[c][next_word] + smoothing_value) / (context_counts + smoothing_value * len(model))
    #                     probability_sum += probability
    #             if context_counts > 0:
    #                 probabilities.append(probability_sum / context_counts)
    #     if len(probabilities) > 0:
    #         return sum(probabilities) / len(probabilities)
    #     else:
    #         return 0.0
        
    
    
    def probability(self, context, next_word):
        probabilities = []
        for n in range(1, len(context)+2):
            if n in self.models:
                model = self.models[n]
                context_n = context[-n+1:]
                context_counts = sum(model[context_n].values())
                smoothing_value = 1
                probability = (model[context_n][next_word] + smoothing_value) / (context_counts + smoothing_value * len(model))
                probabilities.append(probability)
        return sum(probabilities) / len(probabilities)
    
def generate_contexts(sentence,n,slangword):
    contexts = []
    for n in range(1, n+1):
        for i in range(len(sentence)):
            if sentence[i] == slangword:
                left_context = tuple(sentence[max(0, i - n + 1):i])
                right_context = tuple(sentence[i+1:i+n])
                context = left_context + right_context
                contexts.append(left_context)
                contexts.append(right_context)
                contexts.append(context)
    new_contexts = tuple(x for x in contexts if x != ())
    return new_contexts

def getToken():
    df = pd.read_csv('phueakCleanUp.csv')
    df = df.dropna()
    token = [word_tokenize(i, engine="newmm") for i in df['tweet']]
    # for i in df['tweet']:
    #     words = tokenize(i)
    #     token.append(words)
    return token

data = getToken()

data_test_slang = pd.read_csv('phueaktest.csv')
data_test_notslang = pd.read_csv('phueaktest2.csv')
data_test = pd.read_csv('phueaktest3.csv')
model = NgramLanguageModel(3, data,"เผือก")
sentence = "ไม่เผือกนะคะ"
# print(model.models)

# with open('probabilities.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['context', 'next_word', 'probability'])
#     for n in range(1, model.max_n+1):
#         model_n = model.models[n].copy()
#         for context in model_n:
#             for next_word in model_n[context]:
#                 prob = model.probability(context, next_word)
#                 if next_word == "เผือก":
#                     writer.writerow([context, next_word, prob])

context_in_sentence = generate_contexts(word_tokenize(sentence),3,"เผือก")
# print(range(len(context_in_sentence)))
# print(context_in_sentence)
# print(type(context_in_sentence[-1]))

def getprob():
    smoothing_value = 0.001
    prob = 1
    probabilities = []
    with open('probabilities.csv', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            col1 = row[0]
            col2 = row[1]
            col3 = row[2]
            for n in range(len(context_in_sentence)):
                if str(context_in_sentence[n]) == "()":
                    pass
                elif str(context_in_sentence[n]) == col1:
                    # print(str(context_in_sentence[n]) + col1)
                    print(float(col3))
                    probabilities.append(float(col3))

    for i in range(len(context_in_sentence)):
        if i < len(probabilities):
            prob *= probabilities[i]
        else:
            prob *= smoothing_value
    
def getprob_datatest(data_test_slang):
    probabilities_test = []
    for i in data_test_slang["tweet_test"]:
        # print(type(i))
        context_in_sentence = generate_contexts(word_tokenize(i),3,"เผือก")
        # print(context_in_sentence)
        smoothing_value = 1
        prob = 1
        probabilities = []
        with open('probabilities.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                row1 = row[0]
                row3 = row[2]
                for n in range(len(context_in_sentence)):
                    if str(context_in_sentence[n]) == "()":
                        pass
                    if str(context_in_sentence[n]) == row1:
                        # print(str(context_in_sentence[n]) + col1)
                        probabilities.append(float(row3))
                    # else:
                    #     probabilities.append(smoothing_value)

        for i in range(len(context_in_sentence)):
            if i < len(probabilities):
                prob *= probabilities[i]+smoothing_value
            else:
                prob *= smoothing_value
        probabilities_test.append(prob)

    return probabilities_test

def getprob_datatest_threshold(data_test_slang,threshold):
    probabilities_test = {}
    for i in data_test_slang["tweet_test"]:
        # print(type(i))
        context_in_sentence = generate_contexts(word_tokenize(i),3,"เผือก")
        # print(context_in_sentence)
        sentence = i
        smoothing_value = 1
        prob = 1
        probabilities = []
        with open('probabilities.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                row1 = row[0]
                row3 = row[2]
                for n in range(len(context_in_sentence)):
                    if str(context_in_sentence[n]) == "()":
                        pass
                    if str(context_in_sentence[n]) == row1:
                        # print(str(context_in_sentence[n]) + col1)
                        probabilities.append(float(row3))
                    # else:
                    #     probabilities.append(smoothing_value)

        for i in range(len(context_in_sentence)):
            if i < len(probabilities):
                prob *= probabilities[i]+smoothing_value
            else:
                prob *= smoothing_value
        probabilities_test[sentence] = prob >=threshold

    return probabilities_test

test = getprob_datatest(data_test_slang)
test2 = getprob_datatest(data_test_notslang)
filtered_list = [x for x in test if x != 1]
threshold = min(filtered_list)
test_check = getprob_datatest_threshold(data_test,threshold)
print(test_check)
# print(test2)

# # create x-axis values
# x = list(range(len(test)))

# # plot the two lists as line graphs
# plt.plot(x, test, label='Probabilities Test')
# plt.plot(x, test2, label='Probabilities Train')

# # add labels and legend
# plt.xlabel('Tweet Index')
# plt.ylabel('Probability')
# plt.title('Probability Comparison')
# plt.legend()

# # show the plot
# plt.show()