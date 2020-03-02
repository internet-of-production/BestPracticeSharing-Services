
from io import BytesIO
import matplotlib.pyplot as plt
import DatabaseIO.readDatabase as rd
#import plotly.express as px
#import plotly
from matplotlib import ticker
import colorsys


import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


def get_N_HexCol(N=5):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out


def plotCoordinatesPlot(Inputdata = "Clustereddata", X = None, labels = None, core_samples_mask = None, axis = [1,2]):
    print("- plotClustering")


    if (Inputdata == "Clustereddata"):
        df2 = rd.readClusteredDataDF()
        axis.append("Label")
        axis.append("Clustercore")
        df2 = df2[axis]

    else:
        X, labels = rd.readTransformedData()
        core_samples_mask = [0] * len(labels)

    df2 = df2.drop('Clustercore', axis = 'columns')
    df2[0] = df2['Label']+2
    df2 = df2.drop('Label', axis = 'columns')
    df2 = df2.rename(columns={0:'Label'})
    df = df2

#    d = {'Label': [2,4,3,2,5,3], 1: [70,23,53,53,12,85], 2: [23,45,23,90,35,12] , 3: [12,34,15,23,56,23], 4: [223,423,125,125,125,522], 5: [2,3,2,3,4,5]}
#    df = pd.DataFrame(data=d)

#    df[1] = pd.to_numeric(df[1].replace('?', np.nan))
    array_to_use = list(set(df['Label']))
    array_to_use.insert(0, min(df['Label'])-1)
    df['Label'] = pd.cut(df['Label'],array_to_use)

    plt.figure()

    cols = list(x for x in df.columns)
    cols.remove("Label")
    x = [i for i, _ in enumerate(cols)]
#    colours = ['#2e8ad8', '#cd3785', '#c64c00', '#889a00']
#    colours = ['red', 'blue', 'green', 'yellow', 'black']

    # create dict of categories: colours
    colours = get_N_HexCol(len(df['Label'].cat.categories))
    colours = {df['Label'].cat.categories[i]: colours[i] for i, _ in enumerate(df['Label'].cat.categories)}

    # Create (X-1) subplots along x axis
    fig, axes = plt.subplots(1, len(x) - 1, sharey=False, figsize=(15, 5))

    # Get min, max and range for each column
    # Normalize the data for each column
    min_max_range = {}
    for col in cols:
        min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
        ### Normalize on/off
        df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))

    # Plot each row
    if len(cols) == 2:
        for idx in df.index:
            Label_category = df.loc[idx, 'Label']
            axes.plot(x, df.loc[idx, cols], colours[Label_category])
        axes.set_xlim([x[0], x[0 + 1]])
    else:
        for i, ax in enumerate(axes):
            for idx in df.index:
                Label_category = df.loc[idx, 'Label']
                ax.plot(x, df.loc[idx, cols], colours[Label_category])
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

    if len(cols) == 2:
            axes.xaxis.set_major_locator(ticker.FixedLocator([0]))
            set_ticks_for_axis(0, axes, ticks=6)
            axes.set_xticklabels([cols[0]])
            axes.xaxis.set_major_locator(ticker.FixedLocator([1]))
            set_ticks_for_axis(1, axes, ticks=6)
            axes.set_xticklabels([cols[1]])
    else:
        for dim, ax in enumerate(axes):
            ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
            set_ticks_for_axis(dim, ax, ticks=6)
            ax.set_xticklabels([cols[dim]])

    # Move the final axis' ticks to the right-hand side
    if not len(cols) == 2:
        ax = plt.twinx(axes[-1])
        dim = len(axes)
        ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
        set_ticks_for_axis(dim, ax, ticks=6)
        ax.set_xticklabels([cols[-2], cols[-1]])
    else:
        axes.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
        set_ticks_for_axis(1, axes, ticks=6)
        axes.set_xticklabels([cols[-2], cols[-1]])

    # Remove space between subplots
    plt.subplots_adjust(wspace=0)

    legends = list(range(1,len(colours)+1))

    # Add legend to plot
    plt.legend(
        [plt.Line2D((0, 1), (0, 0), color=colours[cat]) for cat in df['Label'].cat.categories],
        legends,
        bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=-1.5)

    img = BytesIO()
    plt.savefig(img)
    #    plt.show()
    img.seek(0)
    plt.close()
    return img
#    plt.show()





