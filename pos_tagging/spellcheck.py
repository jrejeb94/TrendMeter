import pandas as pd
from spellchecker import SpellChecker
from gensim.models import Word2Vec
from nltk import RegexpTokenizer

import os #import os module
PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))

data_path= PATH + "/reviews.csv" #set the path that we are going to read through
tagged_coms=[] #open up an empty array into which we will store our tagged coms

datas = pd.read_csv(data_path)

spell = SpellChecker(language='fr')


def get_nltk_text(raw,tokenizer,encoding='utf8'):
    '''create an nltk text using the passed argument (raw) after filtering out the commas'''
    #turn the raw text into an nltk text object
    text = tokenizer.tokenize(raw)
    return text

tokenizer = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')
sentences = []

numb_com = len(datas)    
for ind in range(numb_com):
    print(float(ind/numb_com))
    com = datas["review_txt"][ind]
    if type(com)==str:
        sentences.append(get_nltk_text(com,tokenizer))

model = Word2Vec(sentences=sentences, size=100, window=5, min_count=5, workers=8, sg=1)
#model.wv.most_similar("❤")

# find those words that may be misspelled
for com in datas["review_txt"]:
    for w in get_nltk_text(com,tokenizer):
        if w not in spell and w in model:
            if spell.correction(w) in model:
                print(w,spell.correction(w))