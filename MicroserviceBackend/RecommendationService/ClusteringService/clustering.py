
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
#import metric_learn
from metric_learn import ITML


def writeClusteringResult(X, labels, labels_true, core_samples_mask, silent = True):
    if not silent:  print("- writeClusteringResult")

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    if not silent:  print('Estimated number of clusters: %d' % n_clusters_)
    if not silent:  print('Estimated number of noise points: %d' % n_noise_)
    if not silent:  print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    if not silent:  print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    if not silent:  print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    if not silent:  print("Adjusted Rand Index: %0.3f"
          % metrics.adjusted_rand_score(labels_true, labels))
    if not silent:  print("Adjusted Mutual Information: %0.3f"
          % metrics.adjusted_mutual_info_score(labels_true, labels,
                                               average_method='arithmetic'))
#    print("Silhouette Coefficient: %0.3f"
#          % metrics.silhouette_score(X, labels))

    df1 = pd.DataFrame(X)
#    df1.columns = ['xValue', 'yValue']
#    print(df1)
    df1['Label'] = labels
    df1['Clustercore'] = core_samples_mask
#    print(df1)

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    df1.to_sql('ClusteredData', con=conn, if_exists='replace')
#    df1['ts'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
#    df1.to_sql('ClusteredDataHistorisiert', con=conn, if_exists='append', index_label= 'id')
    conn.commit()
    conn.close()

    if not silent:  print("+ writeClusteringResult")
    return 1


# do a calculation of similar processes based on clustering
def doClustering(X = None, y = None, initial = False, silent = True):
    takekmeans = True
    takeoptics = False
    if not silent:  print("- doClustering")
    #
    # if (X == None and y == None):
    #     if initial == True:
    #         X, y = rd.readTransformedData()
    #     else:
    #         X, y, clustercore = rd.readClusteredData()
    #         votesX, votesY = rd.readFeedbackData()

    X, y = rd.readTransformedData()

    # metric learning

#    X2 = X.iloc[:, 0:].values

#    print("votesX")
#    print(votesX)
#    print("votesY")
#    print(votesY)

    X2 = X.iloc[:, 0:].values

#    print("X2")
#    print(X2)

#    print(itml.transform(X2))
    if initial == False:

        votesX, votesY = rd.readFeedbackData()
        pairs = []
        for index, row in votesX.iterrows():
            #        print("iterrow")
            #        print(row["id_punkt1"])
            #        print(row["id_punkt2"])
            pairs.append((X2[row["id_punkt1"]], X2[row["id_punkt2"]]))

#        print("pairs")
#        print(pairs)
        a = votesY
#        print(a)
        #    upvotes = [X2[0], X2[1]]
        #    upvotes = [[[1.2, 7.5], [1.3, 1.5]]]
        #    #    downvotes =
        #    print(upvotes)
        #    upvotes = [[X2[0], X2[1]], [X2[1], X2[2]]]
        #    print(upvotes)
        #    a = [1, -1]

        itml = ITML()
        itml.fit(pairs, a)
        if not silent:  print("Transform")
#        print(X2)

        X2 = itml.transform(X2)
#        X2 = X2 * 500
#        X2 = X2 * 500
#        print(X2)

#    X2 = X2 * 1000
#    print(X2)
#    print(X)

#    writeClusteringResult(X, y)

    if takekmeans == True:
        # Compute kMeans
        kmeans = KMeans(n_clusters=4 , random_state=0).fit(X2)
        labels = kmeans.labels_
        labels_true = y
        core_samples_mask = [0] * len(y)
    elif takeoptics == True:
        opt = OPTICS(min_samples=30, xi=.05)
#        opt = OPTICS(min_samples=50, xi=.05, min_cluster_size=.05)
        opt.fit(X2)
        labels = opt.labels_
        labels_true = y
        core_samples_mask = [0] * len(y)
    else:
        # Compute DBSCAN
    #    db = DBSCAN(eps=0.1, min_samples=10).fit(X2)
        db = DBSCAN(eps=0.6, min_samples=5).fit(X2)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        labels_true = y

    writeClusteringResult(X2, labels, labels_true, core_samples_mask)

    if not silent:  print("+ doClustering")
    return 1

