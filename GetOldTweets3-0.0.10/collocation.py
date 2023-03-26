import nltk
nltk.download('all')
# from nltk.corpus import wordnet as wn
from pythainlp.corpus.wordnet import synsets,synset
from attacut import tokenize

def lesk_algorithm(word, sentence):
    best_sense = None
    max_overlap = 0
    context = tokenize(sentence)
    for sense in synsets(word):
        signature = set(sense.definition().split())
        for example in sense.examples():
            signature.union(set(example.split()))
        overlap = len(signature.intersection(context))
        for hypernym in sense.hypernyms():
            signature.union(set(hypernym.definition().split()))
        if overlap > max_overlap:
            best_sense = sense
            max_overlap = overlap
    return best_sense

n = synset("catbird.n.02")
p = synset("albinal.a.01")
print(n.definition())