
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
from scipy import stats
import time

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

#    g = sns.FacetGrid(X, col = cols, hue="label")
#    g.map(plt.scatter, "total_bill", "tip", s=50, alpha=.7, linewidth=.5, edgecolor="white")
#    g.add_legend()

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


def plotClustering2D(Inputdata = "Clustereddata", output = "website", currentIteration = "", silent = True, axis = [1,2]):
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
    cols = axis
    #plot noise in black
    elem = -1
    if elem in labels:
        print("Noise existing. Assigning color black.")
        current_palette = sns.color_palette()
        sns.set_palette(
            ["#000000"] + current_palette[1:]
        )


    f = plt.figure(figsize=(15, 15))

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
#    print(1,unique_labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    fig = plt.figure()
    #        fig.subplots_adjust()
    ax1 = fig.add_subplot(111)

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

#        xy = X[class_member_mask & core_samples_mask]
#        xy = xy.iloc[:,0:].values
#        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=2)

        xy = X[class_member_mask]
        xy = xy.iloc[:,0:].values
#        print(xy)

#        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=20)

        ax1.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=20)
        ax1.set_xlabel('Merkmal 1')
        ax1.set_ylabel('Merkmal 2')

    #    plt.title('Clustering. Estimated number of clusters: %d' % len(unique_labels))

#    f.savefig("clustering.pdf", bbox_inches='tight')

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



def plotClustering1D(Inputdata = "Clustereddata", output = "website", currentIteration = "", silent = True, axis = 1):
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
    cols = axis
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
#    print(2,unique_labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    fig2 = plt.figure()
    #        fig.subplots_adjust()

#    fig2.suptitle('This is a somewhat long figure title', fontsize=16)
    fig2.constrained_layout=True
    ax1 = fig2.add_subplot(212)
    ax1.set_title('Merkmal 2')
#    print(X)
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        #        xy = X[class_member_mask & core_samples_mask]
        #        xy = xy.iloc[:,0:].values
        #        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=2)

        xy = X[class_member_mask]
        xy = xy.iloc[:, 0:].values
#        print(xy)

        ax1 = sns.kdeplot(xy[:, 0], shade=True)
        ax1.set_ylabel('%')
#        ax1.set_xlabel('value')
#        ax1.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=20)
#        ax1.set_xlabel('Merkmal 1')
#        ax1.set_ylabel('Merkmal 2')

    ax2 = fig2.add_subplot(211)
    ax2.set_title('Merkmal 1')
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        #        xy = X[class_member_mask & core_samples_mask]
        #        xy = xy.iloc[:,0:].values
        #        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=2)

        xy = X[class_member_mask]
        xy = xy.iloc[:, 0:].values
#        print(xy)

        ax2 = sns.kdeplot(xy[:, 1], shade=True)
        ax2.set_ylabel('%')
#        ax2.set_xlabel('value')
#        ax1.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=20)
#        ax1.set_xlabel('Merkmal 1')
#        ax1.set_ylabel('Merkmal 2')



    fig2.subplots_adjust(top=0.93, wspace=0.3)
#    subt = '1D Plot: ' + Inputdata
#    t = fig2.suptitle(subt, fontsize=14)

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


def coordinatesplot():
    print("1")


def plotClustering1Dbak(Inputdata = "Clustereddata", output = "website", currentIteration = "", silent = True, axis = 1):
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
    cols = axis
    #plot noise in black
    elem = -1
    if elem in labels:
        print("Noise existing. Assigning color black.")
        current_palette = sns.color_palette()
        sns.set_palette(
            ["#000000"] + current_palette[1:]
        )

    sns.set(color_codes=True)
    x = np.random.normal(size=np.random.randint(51,100))
    if axis == 1:
        x = np.random.normal(size=np.random.randint(25,50))
    else:
        x = np.random.normal(size=np.random.randint(51,100))
    fig2 = plt.figure()
#    ax = fig2.add_subplot(111)
#    ax = sns.distplot(x, shade=True)
    ax = sns.kdeplot(x, shade=True)

    fig2.subplots_adjust(top=0.93, wspace=0.3)
#    subt = '1D Plot: ' + Inputdata
#    t = fig2.suptitle(subt, fontsize=14)

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