from __future__ import unicode_literals

import pandas as pd
import numpy as np
import os
import codecs
import spacy
from spacy.symbols import nsubj, VERB, NOUN, PRON

nlp = spacy.load('fr_core_news_sm')
PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))


def sent_segmentation(text, segmented_review_txt_filepath, max_len=50):
    """
    segments the docs in the inputed list of docs (text)
    adds punctuation and returns the new text
    """
    prev_i = 0
    new_txt = ""
    for parsed_review in nlp.pipe(text):
        for sent in parsed_review.sents:
            if len(sent) > max_len:
                added_sent = []
                for i, t in enumerate(sent):
                    if i != 0:

                        if t.pos_ == 'PRON' \
                                and (sent[i - 1].pos_ not in ['ADP', 'PRON']) \
                                and (sent[i - 1].text.lower() not in ['ne', "n'", "n", 'pas']):
                            added_sent = added_sent + [sent[prev_i:i]]
                            prev_i = i
                new_txt += ". ".join(map(str, added_sent)) + ". "
            else:
                new_txt += sent.text
        new_txt += u'\n'

    with codecs.open(segmented_review_txt_filepath, 'w', encoding='utf_8') as f:
        f.write(new_txt)


if __name__ == '__main__':
    # ouput filename
    segmented_review_txt_filepath = os.path.join(PATH, "data", "preprocess_output", "segmented_doc", "review_txt.txt")

    # Load database as a dataframe
    database = pd.read_excel(os.path.join(PATH, 'data', 'params', 'database.xlsx'), encoding='utf_8')
    ReviewText_col = pd.Series(database.ReviewText.astype('unicode').values)
    text = list(ReviewText_col)
    sent_segmentation(text, segmented_review_txt_filepath)
