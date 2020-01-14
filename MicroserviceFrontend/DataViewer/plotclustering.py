
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import DatabaseIO.readDatabase as rd
import seaborn as sns
from pandas.plotting import parallel_coordinates
import os

def plotClustering(Inputdata = "Clustereddata", output = "website", currentIteration = "", silent = True):
    if not silent:  print("- plotClustering")

##### Scatter plot
    if (Inputdata == "Clustereddata"):
        X, labels, core_samples_mask = rd.readClusteredData()
    else:
        X, labels = rd.readTransformedData()
        core_samples_mask = [0] * len(labels)

    X["label"] = labels
    X["label"] = X["label"].apply(str)

    colnum = len(X.columns)
    cols = range(1,colnum)#[1, 2, 3]

    #plot noise in black
    elem = -1
    if elem in labels:
        print("Noise existing. Assigning color black.")
        current_palette = sns.color_palette()
        sns.set_palette(
            ["#000000"] + current_palette[1:]
        )

#    print(sns.color_palette())
#    sns.set(style="ticks", color_codes=True)
    pp = sns.pairplot(data = X, vars = cols, hue = "label")#, palette="husl"

    fig = pp.fig
    fig.subplots_adjust(top=0.93, wspace=0.3)
    subt = 'Pairwise Plots: ' + Inputdata
    t = fig.suptitle(subt, fontsize=14)

    #
    #
    # # Cast 1/0 to bool
    # core_samples_mask = np.ma.make_mask(core_samples_mask)
    #
    # f = plt.figure(figsize=(8, 6))
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
    #     xy = xy.iloc[:,0:].values
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=8)
    #
    #     xy = X[class_member_mask & ~core_samples_mask]
    #     xy = xy.iloc[:,0:].values
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)
    #
    # plt.title('Clustering. Estimated number of clusters: %d' % len(unique_labels))
    #
    # f.savefig("clustering.pdf", bbox_inches='tight')
    if output == "website":
        img = BytesIO()
        plt.savefig(img)
    #    plt.show()
        img.seek(0)
        if not silent:  print("+ plotClustering")
        return img
    else:
        filename = str(currentIteration) + "_clusteringplot.pdf"
        plt.savefig(filename, bbox_inches='tight')
        plt.show()
        if not silent:  print("+ plotClustering")
        return 0

#os.chdir("/Users/stefanbraun/PycharmProjects/BestPracticeSharing-Services/")
#plt = plotClustering(Inputdata = "")