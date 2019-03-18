
import matplotlib.pyplot as plt
from src.afinnmaster.afinn import Afinn
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
import plotly
import pandas as pd

plotly.offline.init_notebook_mode()


def loadFile(file):
    db = pd.read_csv(file, encoding='latin-1')
    db = pd.DataFrame({'Comment' : db.commentText,
                       'Likes' : db.likes})
    db = db.dropna()

    return db

def computeScores(df):
    # score using Afinn
    af = Afinn(language = "fr")
    afinn_scores = [af.score(article) for article in df.Comment]

    # score using Blobber
    tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    blobber_scores = [tb(article).sentiment for article in df.Comment]
    polarity       = [pl[0] for pl in blobber_scores]
    objectivity    = [pl[1] for pl in blobber_scores]

    # merging the results to the dataframe
    df['AfinnScore']  = afinn_scores
    df['Polarity']    = polarity
    df['Objectivity'] = objectivity

    return(df)

def ratioPositive(df):
    n_pos = len(df[df.Polarity > 0.0])
    n_row = len(df)


    return n_pos / n_row
