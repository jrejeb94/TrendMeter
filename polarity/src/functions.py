
import matplotlib.pyplot as plt
from src.afinnmaster.afinn import Afinn
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
import plotly
import pandas as pd

plotly.offline.init_notebook_mode()


def computeScores(df):
    print("Computing scores")
    print(" - Afinn score")
    # score using Afinn
    af = Afinn(language = "fr")
    afinn_scores = [af.score(article) for article in df.Review]

    print(" - Afinn score computed")
    print(" - Polarity & Objectivity")
    # score using Blobber
    tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    blobber_scores = [tb(article).sentiment for article in df.Review]
    polarity       = [pl[0] for pl in blobber_scores]
    objectivity    = [pl[1] for pl in blobber_scores]

    # merging the results to the dataframe
    df['AfinnScore']  = afinn_scores
    df['Polarity']    = polarity
    df['Objectivity'] = objectivity

    print(" - All scores computed")
    return(df)

def quickPlot(x, y, title_x, title_y):
    fig =  {
        'data': [
        {
            'x': x,
            'y': y,
            'name': "Product", 'mode': 'markers',
        }
    ],
    'layout': {
        'xaxis': {'title': title_x},
        'yaxis': {'title': title_y},
        'width' : 400,
        'height' : 400
        }
    }
    plotly.offline.iplot(fig)

def quick3Plot(x, y, z, title_x, title_y, title_z):
    fig =  {
        'data': [
        {
            'x': x,
            'y': y,
            'z': z,
            'name': "Product", 'mode': 'markers',
            'type': 'scatter3d'
        }
    ],
    'layout': {
        'xaxis': {'title': title_x},
        'yaxis': {'title': title_y}
        }
    }
    plotly.offline.iplot(fig)


def splitComments(db, symbol):
    n_df = pd.DataFrame(columns = db.columns)
    nrow = db.shape[0]
    print(nrow)
    for i in range(0, nrow):
        row = pd.DataFrame(db.loc[[i]])
        comment = row['Review'][i]
        #print(comment[[0]])
        splitted = comment.split(symbol)

        # adding to the new dataframe
        for j in range(0, len(splitted)):
            if len(splitted[j]) > 0:
                n_comment = row.copy()
                n_comment['Review'][[i]] = splitted[j]
                n_df = n_df.append(n_comment, ignore_index = True)

    return n_df

def loadTopicsFile(file):
    print("Loading topic file...")
    df = pd.read_csv(file, sep = ";", encoding="latin-1")
    # df = df.drop(columns=['Unnamed: 0'])
    df = df.rename(index=str, columns={"documents" : "Review"})
    for i in range(len(df.columns)-1):
        df = df.rename(index=str, columns={"{}".format(i):"Topic{}".format(i)})

    print(" - File loaded {}".format(file))
    return df.dropna()

def selectTopic(db):
    print("Selecting topic for each comment")
    # df = pd.DataFrame(columns=['Review', 'Topic'])
    ntopic = len(db.columns) 
    i = 0
    dict = {}
    for row in db.iterrows():
        index, data = row
        ranges = data.tolist()[1:ntopic]
        topic = ranges.index(max(ranges))
        #df = df.append({'Review' : data['Review'], 'Topic' : topic}, ignore_index = True)
        dict[i] = {'Review' : data['Review'], 'Topic' : topic}
        i = i+1
        if i % 50000 == 0:
            print(" -- Row {} out of {}".format(i, len(db)))

    df = pd.DataFrame.from_dict(dict, "index")
    print(" - Topics selected")
    return df
