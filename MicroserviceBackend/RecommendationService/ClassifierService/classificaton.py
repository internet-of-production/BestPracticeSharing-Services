
# perform svm classification

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import DatabaseIO.readDatabase as rd
import time
import datetime

def plot_hyperplane(clf, min_x, max_x, linestyle, label):
    # get the separating hyperplane
    w = clf.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(min_x - 0.5, max_x + 0.5)  # make sure the line is long enough
    yy = a * xx - (clf.intercept_[0]) / w[1]
    plt.plot(xx, yy, linestyle, label=label)


def writeClassificationResult(X, a):
    print("- writeClassificationResult")

    df1 = pd.DataFrame(X)
    df1['Label'] = a

    #    conn = sqlite3.connect('/Users/stefanbraun/PycharmProjects/BPS Flask/BestPracticeSharing.sqlite')
    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1.to_sql('ClassifiedData', con=conn, if_exists='replace', index_label='id')
    df1['ts'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    df1.to_sql('ClassifiedDataHistorisiert', con=conn, if_exists='append', index_label= 'id')
    conn.commit()
    conn.close()

    print("+ writeClassificationResult")
    return 1


# perform classification on the results (for similarity)
def doClassification(inputbase = 'Clustering', X = None, y = None):
    print("- doClassification")

    if (X == None and y == None):
        if inputbase == 'Clustering':
            X, y, core_samples_mask =  rd.readClusteredData()
        else:
            X, y =  rd.readClassificationData()

    X2 = X.iloc[:, 0:].values

    classif = OneVsRestClassifier(LinearSVC(random_state=0))
    classif.fit(X2, y)
    a = classif.predict(X2)

    writeClassificationResult(X, a)

    return 1
# Add choice to use clustering or classification as input