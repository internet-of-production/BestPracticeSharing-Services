
import numpy as np
import sqlite3

from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import pandas as pd
import random as rd
import MicroserviceBackend.RecommendationService.VotingService.voting as vt
import MicroserviceBackend.DataImportService.initialdataimport as di
import MicroserviceBackend.DataImportService.datapreparation as dp
from DatabaseIO.config import *

def generate_Data(silent = False):
    if silent == True:   print("+ generateData")

    (seed, samples, features, centers, std, randomNumberOfVotes) = generateRandomData()
    # global seed
    # global samples
    # global features
    # global centers
    # global std
    # print(seed)
    # seed = seed * 2
    # samples = rand.randint(10, 50)
    # features = rand.randint(2, 10)
    # centers = rand.randint(3, 10)
    # std = rand.randint(1, 10)
    # print(seed)

    # #############################################################################
    random = 1
    X, labels_true = make_blobs(n_samples = samples,
                                n_features = features,
                                centers = centers,
                                cluster_std = std,
                                random_state = random)

    X = StandardScaler().fit_transform(X)

    print("Features:", features)
    print("Centers:", centers)
    print("std:", std)
    #print(X)
    #print(labels_true)

    df = pd.DataFrame(X)
    df["label"] = labels_true
    #print(df)
    df.to_excel('featuresinputexcel.xlsx', sheet_name='sheet1', index=False)

    # #############################################################################
    # Compute DBSCAN
    # db = DBSCAN(eps=0.9, min_samples=5).fit(X)
    # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    # core_samples_mask[db.core_sample_indices_] = True
    # labels = db.labels_

    #print(labels)

    # #############################################################################
    # Plot result
    # import matplotlib.pyplot as plt
    #
    # # Black removed and is used for noise instead.
    # unique_labels = set(labels)
    # colors = [plt.cm.Spectral(each)
    #           for each in np.linspace(0, 1, len(unique_labels))]
    # for k, col in zip(unique_labels, colors):
    #     if k == -1:
    #         # Black used for noise.
    #         col = [0, 0, 0, 1]
    #
    #     class_member_mask = (labels == k)
    #
    #     xy = X[class_member_mask & core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #              markeredgecolor='k', markersize=14)
    #
    #     xy = X[class_member_mask & ~core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #              markeredgecolor='k', markersize=6)

    if silent == True:   print("- generateData")
    return (df, seed, samples, features, centers, std, randomNumberOfVotes)


def build_feedback(df):

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    sql = 'DELETE FROM Feedback'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    print("Writing Feedback to table...")

    #    print(df)
    c = 0
    d = 0
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
#            print(index1)
#            print(row1["label"])
            if row1["label"] == row2["label"]:
 #                 print(index1, index2, "upvote")
                vt.writeVotingResult(index1, index2, "upvote", silent = True)
                c = c +1
            else:
#                print(index1, row2, "downvote")
                vt.writeVotingResult(index1, index2, "downvote", silent = True)
                d = d +1


    print("Written", c, "Upvotes")
    print("Written", d , "Downvotes")
    print("Written", c+d , "Votes")

    # x1, x2, vote
#

    return 0


def delete_feedback():

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    sql = 'DELETE FROM Feedback'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    return 0

### inefficient
def write_specific_feedback(df,r1,r2, silent = True):

    if not silent: print("Writing Feedback to table...")

    #    print(df)
    c = 0
    d = 0
    for index1, row1 in df.iterrows():
        if index1 == r1:
            for index2, row2 in df.iterrows():
                if index2 == r2:
        #            print(index1)
        #            print(row1["label"])
                    if row1["label"] == row2["label"]:
         #                 print(index1, index2, "upvote")
                        vt.writeVotingResult(index1, index2, "upvote", silent = True)
                        c = c +1
                    else:
        #                print(index1, row2, "downvote")
                        vt.writeVotingResult(index1, index2, "downvote", silent = True)
                        d = d +1


    if not silent: print("Written", c, "Upvotes")
    if not silent: print("Written", d , "Downvotes")
    if not silent: print("Written", c+d , "Votes")

    # x1, x2, vote
#

    return 0


def importData():

    di.writeDataFromExcelToDatabase()
    dp.writeTransformedData()


#df = generate_Data()
#build_feedback(df)
#importData()