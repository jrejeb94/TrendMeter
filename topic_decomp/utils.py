import pandas as pd
import codecs


def get_doc_topic_matrix(algo, term_document_matrix, model, review_txt_filepath, doc_topic_matrix_filepath):
    dtm = None
    if algo.lower().__contains__('lda'):   # for gensim: lda.show_topic(topic_number, topn)
        dtm = model.transform(term_document_matrix)
    elif any(i in algo.lower() for i in ['nmf','lsi']):
        dtm = model.fit_transform(term_document_matrix)

    documents = pd.DataFrame({'documents': codecs.open(review_txt_filepath, 'r', encoding='utf_8').readlines()})
    documents.documents = documents.documents.apply(lambda x:x.strip())
    dtm = pd.DataFrame(dtm)
    dtm_df = pd.concat([documents, dtm], axis=1)
    dtm_df.to_csv(path_or_buf=doc_topic_matrix_filepath, sep=';', na_rep=0, encoding='utf_8')
    dtm_df.to_clipboard()
    return dtm_df


def get_word_topic_matrix(algo, model, feature_names, word_topic_matrix_filepath):

    wtm = None
    if algo.lower().__contains__('lda'):   # for gensim: lda.show_topic(topic_number, topn)
        wtm = model.topic_word_
    elif any(i in algo.lower() for i in ['nmf','lsi']):
        wtm = model.components_
    feature_names = pd.DataFrame({'term': feature_names})
    wtm = pd.DataFrame(wtm).transpose()
    wtm_df = pd.concat([feature_names, wtm], axis=1)
    wtm_df.to_csv(path_or_buf=word_topic_matrix_filepath, sep=';', na_rep=0, encoding='utf_8')
    return wtm_df


def get_top_words_in_topic(n_top_words, wtm):
    """
    print top words in each topic
    """
    for topic_idx, topic in enumerate(wtm.iloc[:, 1:]):
        print("Topic #%d: " % topic_idx)
        print(" ".join([wtm.iloc[i, 0] for i in wtm[topic].argsort()[:-n_top_words - 1:-1]]))
