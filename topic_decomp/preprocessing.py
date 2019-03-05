# coding: utf-8

"""
This file contains the text processing functions such as Tokenizing, StopWords, Stemming ..
"""
from __future__ import unicode_literals

import os
import codecs
import pandas as pd
import re

from gensim.models import Phrases
from gensim.models.word2vec import LineSentence
import spacy

from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
from spacy_lefff import POSTagger

nlp = spacy.load('fr')
# pos = POSTagger()
# nlp.add_pipe(pos, name='pos', after='parser')

PATH = os.path.abspath(os.path.join(os.getcwd()))

# INPUT

## params
stopword_filepath = os.path.join(PATH, "stopwords.csv")
database_xlsx = os.path.join(PATH, "data.csv")
review_txt_filepath = os.path.join(PATH, "review_txt.txt")

# OUTPUT

# # params
# # The process was considered during the test phase in order to test several preprocessing pipelines
process = "process2_b"

# # pre_pre_process
# separate glued words && delete number-letters mix
pre_pre_preprocess_filepath = os.path.join(PATH, 'preprocess_output', "pre_pre_preprocess.txt")

# # Preproccess files
pos_tagged_review_txt_filepath = os.path.join(PATH, 'preprocess_output', "pos_tagged_review_txt.txt")

lower_review_txt_filepath = os.path.join(PATH, 'preprocess_output', "lower_review_txt.txt")

no_stopwords_review_txt_filepath = os.path.join(PATH, 'preprocess_output', "no_stopwords_review_txt.txt")

lemmatized_review_txt_filepath = os.path.join(PATH, 'preprocess_output', "lemmatized_review_txt.txt")

final_review_txt_filepath = os.path.join(PATH, 'preprocess_output', "final_review_txt.txt")

bigram_sentences_filepath = os.path.join(PATH, 'preprocess_output', "bigram_sentences.txt")

bigram_model_filepath = os.path.join(PATH, 'preprocess_output', "bigram_model")


def save_review_col_to_txt(column, review_txt_filepath):
    """
    Saving columns of the data frame in review_txt.txt
    """

    with codecs.open(review_txt_filepath, 'w', encoding='utf_8') as f:
        n = 0
        for sentence in column:
            n += 1
            f.write(str(sentence) + '\n')
        f.close()
    print('Created ==> {}'.format(review_txt_filepath))


def read_line_review_txt(filename):
    """
    generator function to read in reviews from the file
    and un-escape the original line breaks in the text
    """
    with codecs.open(filename, encoding='utf_8') as f:
        for review in f:
            yield review.replace('\\n', '\n')


def pre_pre_process(column):
    """
    Pre-process Step 1:
    separate glued words,
    delete number-letters mix
    replace brands by 'distributeur'
    """

    # Separate glued words such as "performancesAlors" or "performances,alors"
    column = pd.Series(column.apply(lambda s: re.sub(r'([a-zéàèùêîç])([A-Z])',
                                                     r'\1 \2', s)).values)
    column = pd.Series(column.apply(lambda s: re.sub(r'([a-zéàèùêîç])([.!?$%&\\()*+,-/:;<=>@^_])+?([A-Z])',
                                                     r'\1\2 \3', s)).values)
    # Delete mixtures of words and number
    column = pd.Series(column.apply(lambda s: re.sub(r'(\d\w+)+|(\w+\d\w*)+', '', s)).values)

    # Delete mixtures of words and number
    column = pd.Series(column.apply(lambda s: re.sub(r'([\\])([a-z])', ' ', s)).values)

    # Spec. preprocess for french: replace the "J'" by "Je " in order to be understood (and removed by the stopwds step)
    # column = pd.Series(column.apply(lambda s: re.sub(r"([A-Za-zç])('|’)([\w\s])",
    #                                                 r'\1e \3', s)).values)

    return column


def print_too_long_words(column):
    """
    prints words longer than 20 characters
    and containing only letters
    """
    for line in column:
        for w in line.split():
            if len(w) > 20 and w.isalpha():
                print(w)

def convert_pos(pos_tag):
    """
    converts the pos tag from spacy_lefff POS tagger to spacy POS tagger
    :param pos_tag: spacy_lefff POS tag
    :return: spacy (default) POS tag
    """
    if pos_tag == "ADJ":
        return 'a'
    elif pos_tag == "NC":
        return 'n'
    elif pos_tag == "NOUN":
        return 'n'
    elif pos_tag == "VERB" or pos_tag == "VINF":
        return 'v'
    elif pos_tag == "ADV":
        return 'r'
    else:
        return 'n'


def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """
    return token.is_punct or token.is_space

#
# def lemmatized_sentence_corpus(filename):
#     """
#     generator function to use spaCy to parse reviews,
#     lemmatize the text, and yield sentences
#     """
#     lemmatizer = FrenchLefffLemmatizer()
#     for parsed_review in nlp.pipe(read_line_review_txt(filename), batch_size=10000, n_threads=4):
#         yield (u' '.join(
#             # [lemmatizer.lemmatize(str(token)) for token in parsed_review]) + u'\r')
#             [token.lemma_ for token in parsed_review]) + u'\r')


def lemmatized_sentence_corpus(filename):
    """
    generator function to use spaCy to parse reviews,
    lemmatize the text, and yield sentences
    """
    lemmatizer = FrenchLefffLemmatizer()
    for parsed_review in nlp.pipe(read_line_review_txt(filename), batch_size=10000, n_threads=4):
        yield (u' '.join(
            [lemmatizer.lemmatize(token.text, convert_pos(token.pos_)) for token in parsed_review]) + u'\r')


def pos_to_keep(filename, list_pos):
    """
     keep only the listed Part-of-Speech
     https://spacy.io/usage/linguistic-features
     https://stackoverflow.com/questions/40288323/what-do-spacys-part-of-speech-and-dependency-tags-mean
    """
    # print(spacy.explain('pobj'))
    f = codecs.open(filename, 'r', encoding='utf_8').readlines()
    f = [re.sub(r'([:/\.\!\?,;*"])', r' \1 ', line) for line in f]  # add a space before any punct
    for parsed_review in nlp.pipe(f, batch_size=10000, n_threads=4):
        yield (u' '.join([token.text for token in parsed_review
                          if token.pos_ in list_pos and not token.is_punct]))


def delete_stop_words(review_filename, stopword_filepath, min_length=2):
    """
    generator function to use spaCy to parse reviews,
    delete stopwords, and yield sentences
        """
    stopwords = pd.read_csv(stopword_filepath, encoding='utf_8')['Stopwords'].drop_duplicates().values.tolist()
    for parsed_review in nlp.pipe(read_line_review_txt(review_filename), batch_size=10000, n_threads=4):
        yield (u' '.join([token.text for token in parsed_review if not (token.is_punct or token.is_space
                                                                        or token.text in stopwords
                                                                        or len(token.text) < min_length)]))


def main():
    # """   Getting data (to be changed with a read from HIVE)  """
    # complete_database = pd.read_excel(io=database_xlsx, column=['Source', 'ReviewDate',
    #                                                             'SKU_Seller', 'ReviewUser',
    #                                                             'ReviewRate', 'ReviewTitle',
    #                                                             'ReviewText'], na_values='')

    # """ Getting data on up-to-date database"""
    #
    # complete_database = pd.read_csv(database_xlsx,
    # #                                 usecols=['t2_all_fr_reviews.id_source', 't2_all_fr_reviews.reviewdate',
    # #                                          't2_all_fr_reviews.sku_seller', 't2_all_fr_reviews.reviewuser',
    # #                                          't2_all_fr_reviews.reviewrate', 't2_all_fr_reviews.reviewtitle',
    # #                                          't2_all_fr_reviews.reviewtext'],
    #                                 na_values='')
    #
    # complete_database.rename(
    #     columns={'review_txt': 'ReviewText'}, inplace=True)
    #
    # # database = complete_database.sample(n=100)
    # ReviewText = pd.Series(complete_database.ReviewText.unique()).astype(str)
    #
    # """     Saving ReviewText in review_txt.txt        """
    # save_review_col_to_txt(ReviewText, review_txt_filepath)
    # #
    # """  Pre-process Step 1: separate glued words, delete number-letters mix  """
    # ReviewText = pre_pre_process(ReviewText)
    # save_review_col_to_txt(ReviewText, pre_pre_preprocess_filepath)
    # print_too_long_words(ReviewText)
    #
    # """  POS TAGGING  """
    #
    # with codecs.open(pos_tagged_review_txt_filepath, 'w', encoding='utf_8') as f:
    #     for sentence in pos_to_keep(pre_pre_preprocess_filepath, ["PROPN", "NOUN", "VERB", "ADJ", "ADV"]):
    #         sentence = '\r' if sentence == 'nan\r' else sentence
    #         f.write(sentence.lower() + '\n')
    #     f.close()
    # print('Created ==> {}'.format(pos_tagged_review_txt_filepath))
    #
    # """  all to lower case """
    # with codecs.open(lower_review_txt_filepath, 'w', encoding='utf_8') as f:
    #     for sentence in codecs.open(pos_tagged_review_txt_filepath, 'r', encoding='utf_8').readlines():
    #         f.write(sentence.lower())
    #     f.close()
    # print('Created ==> {}'.format(lower_review_txt_filepath))

    """         Lemmatization  & outputing lemmatized_review_txt file        """
    with codecs.open(lemmatized_review_txt_filepath, 'w', encoding='utf_8') as f:
        for sentence in lemmatized_sentence_corpus(lower_review_txt_filepath):
            sentence = sentence.rstrip()
            sentence = 'NaN' if sentence == '' or sentence == 'nan' else sentence
            f.write(sentence + u'\r' + u'\n')
        f.close()
    print('Created ==> {}'.format(lemmatized_review_txt_filepath))

    """       delete stopwords   """
    with codecs.open(no_stopwords_review_txt_filepath, 'w', encoding='utf_8') as f:
        for sentence in delete_stop_words(lemmatized_review_txt_filepath, stopword_filepath):
            sentence = sentence.rstrip()
            sentence = 'NaN' if sentence == '' else sentence
            f.write(sentence + u'\r' + u'\n')
        f.close()
    print('Created ==> {}'.format(no_stopwords_review_txt_filepath))

    # """         Saving/Getting the bigram models  &&   bigram_sentences_file        """
    # unigram_sentences = LineSentence(no_stopwords_review_txt_filepath)
    # bigram_model = Phrases(unigram_sentences, min_count=20, threshold=20.0)
    # with codecs.open(bigram_sentences_filepath, 'w', encoding='utf_8') as f:
    #    for unigram_sentence in unigram_sentences:
    #        s = u' '.join(bigram_model[unigram_sentence]) if unigram_sentence != ['nan'] else ''
    #        f.write(s + u'\r' + u'\n')
    #    f.close()
    # print('Created ==> {}'.format(bigram_sentences_filepath))

    """ Final result"""
    with codecs.open(final_review_txt_filepath, 'w', encoding='utf_8') as f:
        for sentence in codecs.open(no_stopwords_review_txt_filepath, 'r', encoding='utf_8').readlines():
            sentence = sentence.rstrip()
            sentence = '' if sentence == 'NaN' else sentence
            f.write(sentence + u'\r' + u'\n')
        f.close()
    print('Created ==> {}'.format(final_review_txt_filepath))


if __name__ == '__main__':
    main()