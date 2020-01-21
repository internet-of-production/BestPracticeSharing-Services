
from io import BytesIO
import matplotlib.pyplot as plt
import DatabaseIO.readDatabase as rd
#import plotly.express as px
#import plotly
from matplotlib import ticker


import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

#
# def plotCoordinatesPlotbak(X = None, labels = None, core_samples_mask = None):
#     print("- plotClustering")
#
#     if (X == None and labels == None and core_samples_mask == None):
#         X, labels, core_samples_mask = rd.readClusteredData()
#     X["label"] = labels
# #    X["label"] = X["label"].apply(str)
# #    print(X.dtypes)
# #    print(X)
# #    print(len(X))
# #    print(labels)
# #
#     colnum = len(X.columns)
#     cols = range(1,colnum)#[1, 2, 3]
# #    pp = sns.pairplot(X[cols], size=1.8, aspect=1.8,
# #                      plot_kws=dict(edgecolor="k", linewidth=0.5),
# #                      diag_kind="kde", diag_kws=dict(shade=True))
#
# #    fig = px.parallel_coordinates(X, dimensions=cols, color = "label")
# #    fig.show()
#
# #    return img
#
#     fig = plt.figure()
#     #        fig.subplots_adjust()
#
# #    fig2.suptitle('This is a somewhat long figure title', fontsize=16)
#     fig.constrained_layout=True
#     ax1 = fig.add_subplot(111)
#     ax1.set_title('Coordinates Plot')
#     ax1 = px.parallel_coordinates(X, dimensions=cols, color = "label")
# #    ax1.set_ylabel('%')
# #    print(X)
#
#
#
# #    fig.subplots_adjust(top=0.93, wspace=0.3)
# #    subt = '1D Plot: ' + Inputdata
# #    t = fig2.suptitle(subt, fontsize=14)
#
#     if True:
#         img = BytesIO()
# #        plt.savefig(img)
# #        plt.show()
#         img.seek(0)
#         plt.close()
#         print("+ plotClustering")
#         return img




def plotCoordinatesPlot(X = None, labels = None, core_samples_mask = None):
    print("- plotClustering")

    df = pd.read_csv('auto.csv')

    d = {'mpg': [2,4,3,2,5,3], 'Technologie': [70,23,53,53,12,85], 'Herstellkosten': [23,45,23,90,35,12] , 'Material': [12,34,15,23,56,23], 'Gewicht': [223,423,125,125,125,522], 'Geometrie': [2,3,2,3,4,5]}
    df = pd.DataFrame(data=d)
    print(df)
    df['Technologie'] = pd.to_numeric(df['Technologie'].replace('?', np.nan))
    df['mpg'] = pd.cut(df['mpg'], [1, 2, 3, 4, 5])

    plt.figure()






    cols = ['Technologie', 'Herstellkosten', 'Material', 'Gewicht', 'Geometrie']
    x = [i for i, _ in enumerate(cols)]
    colours = ['#2e8ad8', '#cd3785', '#c64c00', '#889a00']

    # create dict of categories: colours
    colours = {df['mpg'].cat.categories[i]: colours[i] for i, _ in enumerate(df['mpg'].cat.categories)}

    # Create (X-1) subplots along x axis
    fig, axes = plt.subplots(1, len(x) - 1, sharey=False, figsize=(15, 5))

    # Get min, max and range for each column
    # Normalize the data for each column
    min_max_range = {}
    for col in cols:
        min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
        df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))

    # Plot each row
    for i, ax in enumerate(axes):
        for idx in df.index:
            mpg_category = df.loc[idx, 'mpg']
            ax.plot(x, df.loc[idx, cols], colours[mpg_category])
        ax.set_xlim([x[i], x[i + 1]])

    # Set the tick positions and labels on y axis for each plot
    # Tick positions based on normalised data
    # Tick labels are based on original data
    def set_ticks_for_axis(dim, ax, ticks):
        min_val, max_val, val_range = min_max_range[cols[dim]]
        step = val_range / float(ticks - 1)
        tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]
        norm_min = df[cols[dim]].min()
        norm_range = np.ptp(df[cols[dim]])
        norm_step = norm_range / float(ticks - 1)
        ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
        ax.yaxis.set_ticks(ticks)
        ax.set_yticklabels(tick_labels)

    for dim, ax in enumerate(axes):
        ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
        set_ticks_for_axis(dim, ax, ticks=6)
        ax.set_xticklabels([cols[dim]])

    # Move the final axis' ticks to the right-hand side
    ax = plt.twinx(axes[-1])
    dim = len(axes)
    ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
    set_ticks_for_axis(dim, ax, ticks=6)
    ax.set_xticklabels([cols[-2], cols[-1]])

    # Remove space between subplots
    plt.subplots_adjust(wspace=0)

    legends = [1,2,3,4]

    # Add legend to plot
    plt.legend(
        [plt.Line2D((0, 1), (0, 0), color=colours[cat]) for cat in df['mpg'].cat.categories],
        legends,
    #df['mpg'].cat.categories,
        bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=-1.5)

    plt.title("Koordinatengraph")

    img = BytesIO()
    plt.savefig(img)
    #    plt.show()
    img.seek(0)
    plt.close()
    return img
#    plt.show()



    #
    # pd.tools.plotting.parallel_coordinates(
    #     df[['mpg', 'displacement', 'cylinders', 'horsepower', 'weight', 'acceleration']],
    #     'mpg')

#    pd.tools.plotting.parallel_coordinates(
#        df[['mpg', 'horsepower']], 'mpg')


#    plt.show()


#
#     #img = fig.to_image(format="png")
#     img = BytesIO()
#     plt.savefig(img)
# #    fig.write_image("coordinatesplot.jpeg")
#     img.seek(0)
#     print("+ plotClustering")
#    return img


#
# def plotCoordinatesPlotbak2(X = None, labels = None, core_samples_mask = None):
#     print("- plotClustering")
#
#     if (X == None and labels == None and core_samples_mask == None):
#         X, labels, core_samples_mask = rd.readClusteredData()
#     X["label"] = labels
# #    X["label"] = X["label"].apply(str)
# #    print(X.dtypes)
# #    print(X)
# #    print(len(X))
# #   print(labels)
# #
#     colnum = len(X.columns)
#     cols = range(1,colnum)#[1, 2, 3]
# #    pp = sns.pairplot(X[cols], size=1.8, aspect=1.8,
# #                      plot_kws=dict(edgecolor="k", linewidth=0.5),
# #                      diag_kind="kde", diag_kws=dict(shade=True))
#
#     fig = px.parallel_coordinates(X, dimensions=cols, color = "label")
# #    fig.show()
#
#     plotly.io.orca.config.executable = '/Users/stefanbraun/opt/anaconda3/envs/B3-I/'
#
#     #img = fig.to_image(format="png")
#     img = BytesIO()
#     plt.savefig(img)
# #    fig.write_image("coordinatesplot.jpeg")
#     img.seek(0)
#     print("+ plotClustering")
#     return img
