
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import OPTICS, cluster_optics_dbscan
from sklearn import metrics
import sqlite3
import DatabaseIO.readDatabase as rd
import time
import datetime
from metric_learn import ITML


def writeVotingResult(x1, x2, vote = "upvote", silent = False):
    if not silent: print("- writeVotringResult")

    # smaller value is always first entry in database
    if x1 > x2:
        x_temp = x2
        x2 = x1
        x1 = x_temp

    if not silent: print("Voting", x1, x2, vote)

    df1 = pd.DataFrame({'id_punkt1': [x1], 'id_punkt2': [x2]})
    if vote == "upvote":
        df1['feedback'] = 1
    else:
        df1['feedback'] = -1

#    print(df1)

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    df1.to_sql('Feedback', con=conn, if_exists='append')
    conn.commit()
    conn.close()

    if not silent: print("+ writeVotingResult")
    return 1

