
import numpy as np
import matplotlib.pyplot as plt
import MicroserviceBackend.RecommendationService.ClusteringService.clustering as cl

def plotClustering(X = None, labels = None, core_samples_mask = None):
    print("- plotClustering")

    if (X == None and labels == None and core_samples_mask == None):
        X, labels, core_samples_mask = cl.readClusteredData()

    # Cast 1/0 to bool
    core_samples_mask = np.ma.make_mask(core_samples_mask)

    f = plt.figure(figsize=(8, 6))

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        xy = xy.iloc[:,0:].values
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=8)

        xy = X[class_member_mask & ~core_samples_mask]
        xy = xy.iloc[:,0:].values
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

    plt.title('Clustering. Estimated number of clusters: %d' % len(unique_labels))
    plt.show()

#    f.savefig("/Users/stefanbraun/PycharmProjects/BPS Flask/clustering.pdf", bbox_inches='tight')
    f.savefig("clustering.pdf", bbox_inches='tight')

    return 1