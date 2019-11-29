
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import metrics
import sqlite3
import DatabaseIO.readDatabase as rd
import time
import datetime


def writeClusteringResult(X, labels, labels_true, core_samples_mask):
    print("- writeClusteringResult")

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    print("Adjusted Rand Index: %0.3f"
          % metrics.adjusted_rand_score(labels_true, labels))
    print("Adjusted Mutual Information: %0.3f"
          % metrics.adjusted_mutual_info_score(labels_true, labels,
                                               average_method='arithmetic'))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, labels))

    df1 = pd.DataFrame(X)
    df1['Label'] = labels
    df1['Clustercore'] = core_samples_mask

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    df1.to_sql('ClusteredData', con=conn, if_exists='replace', index_label='id')
    df1['ts'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    df1.to_sql('ClusteredDataHistorisiert', con=conn, if_exists='append', index_label= 'id')
    conn.commit()
    conn.close()

    print("+ writeClusteringResult")
    return 1


# do a calculation of similar processes based on clustering
def doClustering(X = None, y = None):
    print("- doClustering")

    if (X == None and y == None):
        X, y = rd.readTransformedData()

    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    labels_true = y

    writeClusteringResult(X, labels, labels_true, core_samples_mask)

    print("+ doClustering")
    return 1
