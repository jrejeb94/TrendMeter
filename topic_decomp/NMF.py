# coding: utf-8
"""
This file contains the NMF approach for topic modelling
"""

import os
from sklearn import decomposition
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import get_doc_topic_matrix, get_word_topic_matrix
import codecs

PATH = os.path.abspath(os.path.join(os.getcwd()))


def create_tfidf(txt):
    """
    Creates the tf-idf representation of the text
    """
    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 1), max_features=None, norm='l2') #max_features entre 300 et 500 (jusqu'à 1000)
    tfidf = vectorizer.fit_transform(txt)
    feature_names = vectorizer.get_feature_names()
    print("Created document-term matrix of size %d x %d" % (tfidf.shape[0], tfidf.shape[1]))
    return tfidf, feature_names


def create_NMF(tfidf, nb_topics):
    """
    Creates the NMF model
    :param tfidf: TF-IDF representation of the text
    :param nb_topics: number of topics to distinguish
    :return: the nmf model, the word_topic matrix and the doc_topic matrix
    """
    nmf = decomposition.NMF(init='nndsvda', n_components=nb_topics, max_iter=200)
    W = nmf.fit_transform(tfidf)
    H = nmf.components_
    print("Generated factor W of size %s and factor H of size %s" % (str(W.shape), str(H.shape)))
    return W, H, nmf


def get_top_doc(top, documents, topic_index, W):
    top_indices = np.argsort(W[:, topic_index])[::-1]
    top_documents = []
    for doc_index in top_indices[0:top]:
        top_documents.append(documents[doc_index])
    return top_documents


if __name__ == '__main__':

    # params
    nb_topics = 30

    # INPUT files :Please change your file paths
    review_txt_filepath = os.path.join(PATH, "review_txt.txt")
    process_filepath = os.path.join(PATH, "preprocess_output", "final_review_txt.txt")

    review_txt = codecs.open(review_txt_filepath, 'r', encoding='utf-8').readlines()
    lemmatized_review_txt = codecs.open(process_filepath, 'r', encoding='utf-8').readlines()

    # OUTPUT files :Please change your file paths
    word_topic_matrix_filepath = os.path.join(PATH, "NMF_output", "k_" + str(nb_topics), "word_topic_matrix.csv")
    doc_topic_matrix_filepath = os.path.join(PATH, "NMF_output", "k_" + str(nb_topics), "doc_topic_matrix.csv")
    #    doc_topic_matrix_filepath = os.path.join(PATH, "data", "NMF_output",
    #                                             str(nb_topics) + custom_name + "doc_topic_matrix.csv")

    # Create TFIDF matrix
    tfidf, feature_names = create_tfidf(lemmatized_review_txt)

    # Create the NMF model
    model = decomposition.NMF(init='nndsvda', n_components=nb_topics, max_iter=200)
    print("Generating the NMF model...")

    # Create W, H matrix
    dtm = get_doc_topic_matrix('nmf', tfidf, model, review_txt_filepath, doc_topic_matrix_filepath)
    wtm = get_word_topic_matrix('nmf', model, feature_names, word_topic_matrix_filepath)
    print("Generated factor W of size %s and factor H of size %s" % (str(wtm.shape), str(dtm.shape)))
