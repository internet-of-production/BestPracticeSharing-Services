
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
#import metric_learn
from metric_learn import ITML

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

#    print("X")
#    print(X)
#    print("y")
#    y = [1 if x == 2 else x for x in y]
#    print(y)

    X2 = X.iloc[:, 0:].values

#    print("X2")
#    print(X2)


    upvotes = [X2[0],X2[1]]
    upvotes = [[[1.2, 7.5], [1.3, 1.5]]]
#    downvotes =
    print(upvotes)
    upvotes = [[X2[0],X2[1]],[X2[1],X2[2]]]
    print(upvotes)
    a = [1,-1]
    print(a)

    classif = OneVsRestClassifier(LinearSVC(random_state=0))
    classif.fit(X2, y)
    a = classif.predict(X2)
    writeClassificationResult(X, a)

#    itml = ITML()
#    itml.fit(upvotes, a)
#    writeClassificationResult(X, y)

    return 1
# Add choice to use clustering or classification as input


def writeMetricLearningResult(X, labels, labels_true, core_samples_mask):
    return 1


# TODO: Lernt gerade auf allen Datenpunkten, sollte nur auf Trainingsset lernen, nicht auf Testset
def doMetricLearning(X = None, y = None):
    itml = ITML()
    itml.fit(X, y)
#    itml.
    return 1
