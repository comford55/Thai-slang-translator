from attacut import tokenize
import pandas as pd
from pythainlp.tag import pos_tag
import json

# test_txt = tokenize('สวยจึ้งมากเลยแม่วันนี้บูดสุดปังสุดปัง')
# test_txt = tokenize('ของจริงไม่มีจกตา')
test_txt = tokenize('วันนี้โคตรดีดเต็มคาราเบล เพราะกินแต่อะไรบูดๆมา')

# print(pos_tag(test_txt, corpus='orchid_ud'))

# f = open('sample_slang.json',encoding='utf-8')

df = pd.read_excel('Slang Parallel Corpora.xlsx')

slang = df

# def getSlang(txt, slang):
#     sl = []
#     slang_words = set(slang['Slang'])
#     for word in txt:
#         if word in slang_words:
#             sl.append((word, 'คำสแลง'))
#         else:
#             sl.append((word, 'คำปกติ'))
#     return sl

def getSlang(txt, slang):

    T = len(txt)
    possible_ngrams = int((T*(T+1))/2)
    word_ngrams = []
    for i in range(1,possible_ngrams+1):
        for j in range(T+1-i):
            if i <= 6:
                ngram_words = txt[j:j+i]
                word_ngrams.append("".join(ngram_words))

    sl = []
    slang_words = set(slang['Slang'])
    for word in txt:
        if word in slang_words:
            sl.append((word, 'คำสแลง'))
        else:
            sl.append((word, 'คำปกติ'))

    ngramsl = []
    for word in word_ngrams:
        if word in slang_words:
            ngramsl.append((word, 'คำสแลง'))
        else:
            ngramsl.append((word, 'คำปกติ'))

    # print(ngramsl)
    return ngramsl
    # return sl


def printFullText(txt):
    for word, tag in txt:
        if tag == 'คำสแลง':
            s = 'คำสแลง'
            c = f' <{s}> {word} </{s}> '
            print(c, end='')
        else:
            print(word, end='')

def findSlang(txt):
    tokenWords = tokenize(txt)
    getTag = getSlang(tokenWords, slang)
    printFullText(getTag)
    print('\n')
    already_printed = set()
    slang_found = False
    for word, tag in getTag:
        if tag == 'คำสแลง' and word not in already_printed:
            already_printed.add(word)
            meaning = slang.loc[slang['Slang']==word]['Meaning'].values[0]
            print(f'{word} = {meaning}')
            slang_found = True
    if not slang_found:
        print('No slang found')
    print(50*'=')

# findSlang('ข้าวแกงวันนี้บูดมาก ไม่จึ้งเอาซะเลยอ่ะ')

# findSlang('ทั้งปังทั้งจึ้งทั้งบิดทั้งปั๊วะ')

# findSlang('มองไปทางนั้นก็เจอนก แถมวันนี้ยังเจอคนนกอีก')

# findSlang('ของจริงไม่มีจกตา')

# findSlang('วันนี้โคตรดีดเต็มคาราเบล')

# findSlang('วันนี้ท่านรมตได้มาเข้าที่ประชุมเมื่อเวลา 10 โมง')

findSlang('เจอเธอแล้วรู้สึกว่าเกินปุยมุ้ย')

findSlang('ถึงเวลาที่เราจะต้องมูฟออนได้แล้ว')

findSlang('เจอแบบนี้งานไม่ใหญ่แน่นะวิ จากคหสตเลย')

# print(getSlang(test_txt, slang))


