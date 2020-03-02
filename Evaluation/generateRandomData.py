import sqlite3
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import pandas as pd
import Backend.RecommendationService.VotingService.voting as vt
import Backend.DataImportService.initialdataimport as di
import Backend.DataImportService.datapreparation as dp
from InputData.config import *

def generate_Data(silent = False):
    if silent == True:   print("+ generateData")

    (seed, samples, features, centers, std, randomNumberOfVotes) = generateRandomData()

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

    df = pd.DataFrame(X)
    df["label"] = labels_true
    df.to_excel('InputData/featuresinputexcel.xlsx', sheet_name='sheet1', index=False)

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


# build all available feedback
def build_feedback(df):

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    sql = 'DELETE FROM Feedback'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    print("Writing Feedback to table...")

    c = 0
    d = 0
    for index1, row1 in df.iterrows():
        for index2, row2 in df.iterrows():
            if row1["label"] == row2["label"]:
                vt.writeVotingResult(index1, index2, "upvote", silent = True)
                c = c +1
            else:
                vt.writeVotingResult(index1, index2, "downvote", silent = True)
                d = d +1

    print("Written", c, "Upvotes")
    print("Written", d , "Downvotes")
    print("Written", c+d , "Votes")

    return 0


### deletes all feedback
def delete_feedback():

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    sql = 'DELETE FROM Feedback'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    return 0


### inefficient because we iterate over the dataframe to find the data point to manipulate
def write_specific_feedback(df,r1,r2, silent = True):

    if not silent: print("Writing Feedback to table...")

    c = 0
    d = 0
    for index1, row1 in df.iterrows():
        if index1 == r1:
            for index2, row2 in df.iterrows():
                if index2 == r2:
                    if row1["label"] == row2["label"]:
                        vt.writeVotingResult(index1, index2, "upvote", silent = True)
                        c = c +1
                    else:
                        vt.writeVotingResult(index1, index2, "downvote", silent = True)
                        d = d +1

    if not silent: print("Written", c, "Upvotes")
    if not silent: print("Written", d , "Downvotes")
    if not silent: print("Written", c+d , "Votes")

    return 0


def importData():

    di.writeDataFromExcelToDatabase()
    dp.writeTransformedData()


#df = generate_Data()
#build_feedback(df)
#importData()