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
from sklearn.metrics import confusion_matrix
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
    df = pd.read_csv('ปังTrain_data.csv')
    df = df.dropna()
    token = [word_tokenize(i, engine="newmm") for i in df['tweet']]
    # for i in df['tweet']:
    #     words = tokenize(i)
    #     token.append(words)
    return token


# data = getToken()

# data_test_slang = pd.read_csv('เผือกTest_data.csv')
# data_test = pd.read_csv('เผือกTest_set.csv')
# data_check_test = pd.read_csv('เผือก_checktest.csv')
# data_test_slang2 = pd.read_csv('แกงTest_data.csv')
# data_test2 = pd.read_csv('แกงTest_set.csv')
# data_check_test2 = pd.read_csv('แกง_checktest.csv')
# data_test_slang3 = pd.read_csv('เทTest_data.csv')
# data_test3 = pd.read_csv('เทTest_set.csv')
# data_check_test3 = pd.read_csv('เท_checktest.csv')
# data_test_slang4 = pd.read_csv('ลำไยTest_data.csv')
# data_test4 = pd.read_csv('ลำไยTest_set.csv')
# data_test_slang5 = pd.read_csv('บูดTest_data.csv')
# data_test5 = pd.read_csv('บูดTest_set.csv')
# data_test_slang6 = pd.read_csv('ปังTest_data.csv')
# data_test6 = pd.read_csv('ปังTest_set.csv')

# model = NgramLanguageModel(3, data,"ปัง")

# with open('ปัง_probabilities.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['context', 'next_word', 'probability'])
#     for n in range(1, model.max_n+1):
#         model_n = model.models[n].copy()
#         for context in model_n:
#             for next_word in model_n[context]:
#                 prob = model.probability(context, next_word)
#                 if next_word == "ปัง":
#                     writer.writerow([context, next_word, prob])

def getprob(context_in_sentence,slang):
    smoothing_value = 1
    prob = 1
    probabilities = []
    with open(slang+'_probabilities.csv', 'r',encoding='utf-8') as f:
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
                    # print(float(col3))
                    probabilities.append(float(col3))

    for i in range(len(context_in_sentence)):
        if i < len(probabilities):
            prob *= probabilities[i]+smoothing_value
        else:
            prob *= smoothing_value
    return prob
    
def getprob_datatest(data_test_slang,slang):
    probabilities_test = []
    for i in data_test_slang["tweet_test"]:
        # print(type(i))
        context_in_sentence = generate_contexts(word_tokenize(i),3,slang)
        # print(context_in_sentence)
        smoothing_value = 1
        prob = 1
        probabilities = []
        with open(slang+'_probabilities.csv', 'r',encoding='utf-8') as f:
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

def getprob_datatest_threshold(data_test_slang,threshold,slang):
    probabilities_test = []
    for i in data_test_slang["tweet_test"]:
        # print(type(i))
        context_in_sentence = generate_contexts(word_tokenize(i),3,slang)
        # print(context_in_sentence)
        sentence = i
        smoothing_value = 1
        prob = 1
        probabilities = []
        with open(slang+'_probabilities.csv', 'r',encoding='utf-8') as f:
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
        if prob >=threshold:
            probabilities_test.append(1)
        else:
            probabilities_test.append(0)


    return probabilities_test

def calculate_metrics(confusion_matrix):
    """
    Calculates accuracy, error rate, precision, and recall given a confusion matrix.
    Args:
        confusion_matrix (array): Array of shape (2, 2) representing the confusion matrix.
    Returns:
        Tuple of (accuracy, error_rate, precision, recall).
    """
    true_positives = confusion_matrix[0][0]
    false_positives = confusion_matrix[0][1]
    false_negatives = confusion_matrix[1][0]
    true_negatives = confusion_matrix[1][1]

    accuracy = (true_positives + true_negatives) / np.sum(confusion_matrix)
    error_rate = (false_positives + false_negatives) / np.sum(confusion_matrix)
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    return accuracy, error_rate, precision, recall

def SlangTranslator(sentence):
    sentence = word_tokenize(sentence)  
    slang_dict = pd.read_excel('threshold.xlsx')
    slang_dict_2 = pd.read_excel('Slang Parallel Corpora.xlsx')
    slang_dict_2 = slang_dict_2['Slang']
    # print(slang_dict_2)
    for word in sentence:
        if word in slang_dict['slang'].values:
            row = slang_dict.loc[slang_dict['slang'] == word]
            threshold = row['threshold'].values[0]
            meaning = row['meaning'].values[0]
            context = generate_contexts(sentence,3,word)
            print(context)
            prob = getprob(context,word)
            print(prob)
            if prob >= threshold:
                print(f"พบคำแสลง {word} หมายถึง {meaning}")
            else:
                print("ไม่เจอคำแสลง")
        # else :

        #     print()


input = input("input text = ")
SlangTranslator(input)






# test = getprob_datatest(data_test_slang,"เผือก")
# filtered_list = [x for x in test if x != 1]
# threshold = min(filtered_list)
# print(threshold)
# test_check = getprob_datatest_threshold(data_test,threshold,"เผือก")
# result_matrix = confusion_matrix(data_check_test["result"],test_check)
# cal = calculate_metrics(result_matrix)
# # print("confusion Matrix ของคำว่า เผือก :")
# # print(result_matrix)
# # print("accuracy : "+ str(cal[0]*100) +"  %")
# # print("error_rate : "+ str(cal[1]*100) +"  %")
# # print("precision : "+ str(cal[2]*100) +"  %")
# # print("recall : "+ str(cal[3]*100) +"  %")

# test_2 = getprob_datatest(data_test_slang2,"แกง")
# filtered_list = [x for x in test_2 if x != 1]
# threshold_2 = min(filtered_list)
# print(threshold_2)
# test_check_2 = getprob_datatest_threshold(data_test2,threshold_2,"แกง")
# result_matrix2 = confusion_matrix(data_check_test2["result"],test_check_2)
# cal2 = calculate_metrics(result_matrix2)
# # print("confusion Matrix ของคำว่า แกง :")
# # print(result_matrix2)
# # print("accuracy : "+ str(cal2[0]*100) +"  %")
# # print("error_rate : "+ str(cal2[1]*100) +"  %")
# # print("precision : "+ str(cal2[2]*100) +"  %")
# # print("recall : "+ str(cal2[3]*100) +"  %")

# test_3 = getprob_datatest(data_test_slang3,"เท")
# filtered_list = [x for x in test_3 if x != 1]
# threshold_3 = min(filtered_list)
# print(threshold_3)
# test_check_3 = getprob_datatest_threshold(data_test3,threshold_3,"เท")
# result_matrix3 = confusion_matrix(data_check_test3["result"],test_check_3)
# cal3 = calculate_metrics(result_matrix3)
# # print("confusion Matrix ของคำว่า เท :")
# # print(result_matrix3)
# # print("accuracy : "+ str(cal3[0]*100) +"  %")
# # print("error_rate : "+ str(cal3[1]*100) +"  %")
# # print("precision : "+ str(cal3[2]*100) +"  %")
# # print("recall : "+ str(cal3[3]*100) +"  %")

# test_4 = getprob_datatest(data_test_slang4,"ลำไย")
# filtered_list = [x for x in test_4 if x != 1]
# threshold_4 = min(filtered_list)
# print(threshold_4)
# test_check_4 = getprob_datatest_threshold(data_test4,threshold_4,"ลำไย")
# result_matrix4 = confusion_matrix(data_test4["result"],test_check_4)
# cal4 = calculate_metrics(result_matrix4)
# # print("confusion Matrix ของคำว่า ลำไย :")
# # print(result_matrix4)
# # print("accuracy : "+ str(cal4[0]*100) +"  %")
# # print("error_rate : "+ str(cal4[1]*100) +"  %")
# # print("precision : "+ str(cal4[2]*100) +"  %")
# # print("recall : "+ str(cal4[3]*100) +"  %")

# test_5 = getprob_datatest(data_test_slang5,"บูด")
# filtered_list = [x for x in test_5 if x != 1]
# threshold_5 = min(filtered_list)
# print(threshold_5)
# test_check_5 = getprob_datatest_threshold(data_test5,threshold_5,"บูด")
# result_matrix5 = confusion_matrix(data_test5["result"],test_check_5)
# cal5 = calculate_metrics(result_matrix5)
# # print("confusion Matrix ของคำว่า บูด :")
# # print(result_matrix5)
# # print("accuracy : "+ str(cal5[0]*100) +"  %")
# # print("error_rate : "+ str(cal5[1]*100) +"  %")
# # print("precision : "+ str(cal5[2]*100) +"  %")
# # print("recall : "+ str(cal5[3]*100) +"  %")

# test_6 = getprob_datatest(data_test_slang6,"ปัง")
# filtered_list = [x for x in test_6 if x != 1]
# threshold_6 = min(filtered_list)
# print(threshold_6)
# test_check_6 = getprob_datatest_threshold(data_test6,threshold_6,"ปัง")
# result_matrix6 = confusion_matrix(data_test6["result"],test_check_6)
# cal6 = calculate_metrics(result_matrix6)
# # print("confusion Matrix ของคำว่า ปัง :")
# # print(result_matrix6)
# # print("accuracy : "+ str(cal6[0]*100) +"  %")
# # print("error_rate : "+ str(cal6[1]*100) +"  %")
# # print("precision : "+ str(cal6[2]*100) +"  %")
# # print("recall : "+ str(cal6[3]*100) +"  %")