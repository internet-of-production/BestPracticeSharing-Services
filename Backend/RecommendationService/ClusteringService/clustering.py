
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import OPTICS, cluster_optics_dbscan
from sklearn import metrics
import sqlite3
import DatabaseIO.readDatabase as rd
from metric_learn import ITML
from InputData.config import *


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
    df1['Label'] = labels
    df1['Clustercore'] = core_samples_mask

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    df1.to_sql('ClusteredData', con=conn, if_exists='replace')
#    df1['ts'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
#    df1.to_sql('ClusteredDataHistorisiert', con=conn, if_exists='append', index_label= 'id')
    conn.commit()
    conn.close()

    if not silent:  print("+ writeClusteringResult")
    return 1


# do a calculation of similar processes based on clustering
def doClustering(X = None, y = None, initial = False, silent = True, numClusters = 4):
    takekmeans = True
    takeoptics = False
    if not silent:  print("- doClustering")

    X, y = rd.readTransformedData()

    # metric learning

    X2 = X.iloc[:, 0:].values

    if initial == False:

        votesX, votesY = rd.readFeedbackData()
        pairs = []
        for index, row in votesX.iterrows():
            pairs.append((X2[row["id_punkt1"]], X2[row["id_punkt2"]]))

        a = votesY

        itml = ITML()
        itml.fit(pairs, a)
        if not silent:  print("Transform")

        X2 = itml.transform(X2)

    if takekmeans == True:
        # Compute kMeans
#        print("numCluster",numClusters)
#        number_clusters = numClusters
        kmeans = KMeans(n_clusters=numClusters , random_state=0).fit(X2)
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

