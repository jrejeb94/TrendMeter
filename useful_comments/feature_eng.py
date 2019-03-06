# coding: utf-8

"""
This file contains the feature engineering part for useful commints classification
"""
from __future__ import unicode_literals

import os
import codecs
import pandas as pd
import numpy as np
import scipy as sp

from topic_decomp.NMF import create_tfidf
PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))

reviews_filepath = os.path.join(PATH, "topic_decomp", "review_txt.txt")
processed_reviews_filepath = os.path.join(PATH, "topic_decomp", "preprocess_output", "final_review_txt.txt")
reviews_txt = codecs.open(reviews_filepath, 'r', encoding='utf-8').readlines()
processed_reviews_txt = codecs.open(processed_reviews_filepath, 'r', encoding='utf-8').readlines()

tfidf, feature_names = create_tfidf(reviews_txt)
print('tfidf', tfidf.shape)
print('reviews', len(reviews_txt))

# #%% create pandas data frame for reviews/features

df = pd.DataFrame({"reviews": reviews_txt})
df = df.assign(len_review=[len(r.split()) for r in processed_reviews_txt])

len_review = [len(r.split()) for r in processed_reviews_txt]

tf = pd.DataFrame(tfidf.todense())
# from sklearn.pipeline import FeatureUnion
# test = FeatureUnion(tfidf, len_review)
# n = list(tfidf.toarray())
# n_features = np.vstack((n, len_review))
n_features = pd.concat(tf, len_review, axis='col')
# p = sp.sparse.hstack(tfidf, tfidf)
print()