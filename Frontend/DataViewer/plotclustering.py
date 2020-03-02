
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import DatabaseIO.readDatabase as rd
import seaborn as sns
from pandas.plotting import parallel_coordinates
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plotClustering2D(Inputdata = "Clustereddata", output = "website", currentIteration = "", silent = True, xAxis = 1, yAxis = 2):
    if not silent:  print("- plotClustering")

##### Scatter plot
    if (Inputdata == "Clustereddata"):
        X, labels, core_samples_mask = rd.readClusteredData()
    else:
        X, labels = rd.readTransformedData()
        core_samples_mask = [0] * len(labels)

    X["label"] = labels
    X["label"] = X["label"].apply(str)

    elem = -1
    if elem in labels:
        print("Noise existing. Assigning color black.")
        current_palette = sns.color_palette()
        sns.set_palette(
            ["#000000"] + current_palette[1:]
        )

    plt.figure(figsize=(15, 15))

    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask]
        xy = xy.iloc[:,0:].values

        ax1.plot(xy[:, xAxis-1], xy[:, yAxis-1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=20)
        ax1.set_xlabel(xAxis)
        ax1.set_ylabel(yAxis)

    if output == "website":
        img = BytesIO()
        plt.savefig(img)
    #    plt.show()
        img.seek(0)
        plt.close()
        if not silent:  print("+ plotClustering")
        return img
    else:
        filename = str(currentIteration) + "_clusteringplot.pdf"
        plt.savefig(filename, bbox_inches='tight')
        plt.show()
        plt.close()
        if not silent:  print("+ plotClustering")
        return 0



def plotClustering1D(Inputdata = "Clustereddata", output = "website", currentIteration = "", silent = True, xAxis = 1, yAxis = 2):
    if not silent:  print("- plotClustering")

##### Scatter plot
    if (Inputdata == "Clustereddata"):
        X, labels, core_samples_mask = rd.readClusteredData()
    else:
        X, labels = rd.readTransformedData()
        core_samples_mask = [0] * len(labels)

    X["label"] = labels
    X["label"] = X["label"].apply(str)

    #plot noise in black
    elem = -1
    if elem in labels:
        print("Noise existing. Assigning color black.")
        current_palette = sns.color_palette()
        sns.set_palette(
            ["#000000"] + current_palette[1:]
        )

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    fig2 = plt.figure()

    fig2.constrained_layout=True

    # first axis

    ax2 = fig2.add_subplot(211)
    ax2.set_title(yAxis)
    for k, col in zip(unique_labels, colors):

        class_member_mask = (labels == k)

        xy = X[class_member_mask]
        xy = xy.iloc[:, 0:].values

        sns.kdeplot(xy[:, yAxis-1], shade=True)

    # sceond axis

    ax1 = fig2.add_subplot(212)
    ax1.set_title(xAxis)

    for k, col in zip(unique_labels, colors):

        class_member_mask = (labels == k)

        xy = X[class_member_mask]
        xy = xy.iloc[:, 0:].values

        sns.kdeplot(xy[:, xAxis-1], shade=True)


    fig2.subplots_adjust(top=0.93, wspace=0.3)
    fig2.tight_layout()

    if output == "website":
        img = BytesIO()
        plt.savefig(img)
        img.seek(0)
        plt.close()
        if not silent:  print("+ plotClustering")
        return img
    else:
        filename = str(currentIteration) + "_clusteringplot.pdf"
        plt.savefig(filename, bbox_inches='tight')
        plt.show()
        plt.close()
        if not silent:  print("+ plotClustering")
        return 0
