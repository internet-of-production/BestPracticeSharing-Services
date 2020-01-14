
from io import BytesIO
import matplotlib.pyplot as plt
import DatabaseIO.readDatabase as rd
import plotly.express as px

def plotCoordinatesPlot(X = None, labels = None, core_samples_mask = None):
    print("- plotClustering")

    if (X == None and labels == None and core_samples_mask == None):
        X, labels, core_samples_mask = rd.readClusteredData()
    X["label"] = labels
#    X["label"] = X["label"].apply(str)
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

    fig = px.parallel_coordinates(X, dimensions=cols, color = "label")
    fig.show()

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    print("+ plotClustering")
    return img
