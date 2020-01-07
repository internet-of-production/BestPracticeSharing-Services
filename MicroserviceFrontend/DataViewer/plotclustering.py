
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import DatabaseIO.readDatabase as rd
import seaborn as sns


def plotClustering(X = None, labels = None, core_samples_mask = None):
    print("- plotClustering")

    if (X == None and labels == None and core_samples_mask == None):
        X, labels, core_samples_mask = rd.readClusteredData()
    X["label"] = labels
    X["label"] = X["label"].apply(str)
    print(X.dtypes)
    print(X)
    print(len(X))
    print(labels)
#
    colnum = len(X.columns)
    cols = range(1,colnum)#[1, 2, 3]
#    pp = sns.pairplot(X[cols], size=1.8, aspect=1.8,
#                      plot_kws=dict(edgecolor="k", linewidth=0.5),
#                      diag_kind="kde", diag_kws=dict(shade=True))

    sns.set(style="ticks", color_codes=True)
    pp = sns.pairplot(data = X, vars = cols, hue = "label")#, palette="husl"

    fig = pp.fig
    fig.subplots_adjust(top=0.93, wspace=0.3)
    t = fig.suptitle('Pairwise Plots', fontsize=14)

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

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    print("+ plotClustering")
    return img
