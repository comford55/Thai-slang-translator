from attacut import tokenize
import pandas as pd
from pythainlp.tag import pos_tag
import json

# test_txt = tokenize('สวยจึ้งมากเลยแม่วันนี้บูดสุดปังสุดปัง')
# test_txt = tokenize('ของจริงไม่มีจกตา')
# test_txt = tokenize('วันนี้โคตรดีดเต็มคาราเบล เพราะกินแต่ของบูดๆมา')

df = pd.read_excel('Slang Parallel Corpora.xlsx')

slang = df

def getSlang(txt, slang):

    T = len(txt)
    possible_ngrams = int((T*(T+1))/2)
    word_ngrams = [] # get all possible less than 6-grams and tag the index
    for i in range(1,possible_ngrams+1):
        for j in range(T+1-i):
            if i <= 6:
                ngram_words = txt[j:j+i]
                word_ngrams.append((("".join([i[0] for i in ngram_words])), [i[1] for i in ngram_words]))

#     print(word_ngrams) [('ของ', [0]), ('จริง', [1]), ('ไม่', [2]), ('มี', [3]), ('จก', [4]), ('ตา', [5]), ('ของจริง', [0, 1]), ('จริงไม่', [1, 2]), ('ไม่มี', [2, 3]), ('มีจก', [
                        # 3, 4]), ('จกตา', [4, 5]), ('ของจริงไม่', [0, 1, 2]), ('จริงไม่มี', [1, 2, 3]), ('ไม่มีจก', [2, 3, 4]), ('มีจกตา', [3, 4, 5]), ('ของจริงไม่มี', [0, 1, 2, 3
                        # ]), ('จริงไม่มีจก', [1, 2, 3, 4]), ('ไม่มีจกตา', [2, 3, 4, 5]), ('ของจริงไม่มีจก', [0, 1, 2, 3, 4]), ('จริงไม่มีจกตา', [1, 2, 3, 4, 5]), ('ของจริงไม่มีจกต
                        # า', [0, 1, 2, 3, 4, 5])]

    slang_words = set(slang['Slang'])

    ngramsl = [] # get 1-grams and n-grams that have คำสแลง tag
    for word in word_ngrams:
        if len(word[1]) == 1:
            if word[0] in slang_words:
                ngramsl.append((word[0], word[1], 'คำสแลง'))
            else:
                ngramsl.append((word[0], word[1], 'คำปกติ'))
        else:
            if word[0] in slang_words:
                ngramsl.append((word[0], word[1], 'คำสแลง'))

#     print(ngramsl) [('ถึง', [0], 'คำปกติ'), ('เวลา', [1], 'คำปกติ'), ('ที่', [2], 'คำปกติ'), ('เรา', [3], 'คำปกติ'), ('จะ', [4], 'คำปกติ'), ('ต้อง', [5], 'คำปกติ'), 
                    # ('มูฟออน', [6], 'คำสแลง'), ('ได้', [7], 'คำปกติ'), ('แล้ว', [8], 'คำปกติ')]

    # find the index of n-grams slang ('งานไม่ใหญ่แน่นะวิ', [3, 4, 5, 6, 7, 8], 'คำสแลง')] index is 3, 4, 5, 6, 7, 8
    delngram = [j for word in ngramsl if len(word[1])>1 for j in word[1]]

    for i in delngram:
        for j in ngramsl:
            if len(j[1]) == 1:
                if i == j[1][0]:
                    ngramsl.remove((j[0], j[1], 'คำปกติ')) # remove 1-grams that contain delngram

    for i in ngramsl: # remove and replace n-grams in the rigt index ('เกินปุยมุ้ย', [5, 6], 'คำสแลง') will place in index of 5
        if len(i[1]) > 1:
            if i[1][0] < len(i[1]):
                replaceword = (i[0], i[1], 'คำสแลง')
                ngramsl.remove(replaceword)
                ngramsl[i[1][0]] = replaceword

    sl = [(word[0], word[-1]) for word in ngramsl] # [('เจอ', 'คำปกติ'), ('เธอ', 'คำปกติ'), ('แล้ว', 'คำปกติ'), ('รู้สึก', 'คำปกติ'), ('ว่า', 'คำปกติ'), ('เกินปุยมุ้ย', 'คำสแลง')]

    return sl

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
    tagwords = [(tokenWords[i], i) for i in range(len(tokenWords))]
    getTag = getSlang(tagwords, slang)
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

findSlang('ข้าวแกงวันนี้บูดมาก ไม่จึ้งเอาซะเลยอ่ะ')

findSlang('ทั้งปังทั้งจึ้งทั้งบิดทั้งปั๊วะ')

findSlang('มองไปทางนั้นก็เจอนก แถมวันนี้ยังเจอคนนกอีก')

findSlang('ของจริงไม่มีจกตา')

findSlang('วันนี้โคตรดีดเต็มคาราเบล')

findSlang('วันนี้ท่านรมตได้มาเข้าที่ประชุมเมื่อเวลา 10 โมง')

findSlang('เจอเธอแล้วรู้สึกว่าเกินปุยมุ้ย')

findSlang('ถึงเวลาที่เราจะต้องมูฟออนได้แล้ว')

findSlang('เจอแบบนี้งานไม่ใหญ่แน่นะวิ จากคหสตเลย')

findSlang('โป๊ะ??? ...โป๊ะคืออะไร? อะไรคือโป๊ะ? มันเป็นยังไง?')

