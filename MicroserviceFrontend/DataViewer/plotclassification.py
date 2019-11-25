
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import DatabaseIO.readDatabase as rd

def plotClassification(X = None, a = None):
    print("- plotClassification")

    if (X == None and a == None):
        X, a = rd.readClassificationData()

    X = X.iloc[:, 0:].values

    f = plt.figure(figsize=(8, 6))

    unique_labels = set(a)

    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (a == k)

        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

    plt.title('Classification. Number of clusters: %d' % len(unique_labels))

#    plt.show()

#    f.savefig("/Users/stefanbraun/PycharmProjects/BPS Flask/classification.pdf", bbox_inches='tight')
    f.savefig("classification.pdf", bbox_inches='tight')

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img
