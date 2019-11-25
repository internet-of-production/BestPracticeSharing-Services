
import pandas as pd
import sqlite3


# read data from data mart
def readTransformedData():
    print("- readTransformedData")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label FROM TransformedData").fetchall())
    conn.close()
    df1.columns = ['xValue', 'yValue', 'Label']

    X = df1[['xValue','yValue']]
    y = df1[['Label']].to_numpy().flatten()

    return X, y


# read clustering result from data mart
def readClusteredData():
    print("- readClusteredData")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label, Clustercore FROM ClusteredData").fetchall())
    conn.close()
    df1.columns = ['xValue', 'yValue', 'Label', 'Clustercore']

    X = df1[['xValue','yValue']]
    y = df1[['Label']].to_numpy().flatten()
    clustercore = df1[['Clustercore']].to_numpy().flatten()

    print("+ readClusteredData")
    return X, y, clustercore


def readClusteredDataDF():
    print("- readClusteredDataDF")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label, Clustercore FROM ClusteredData").fetchall())
    conn.close()
    df1.columns = ['xValue', 'yValue', 'Label', 'Clustercore']

    print("+ readClusteredDataDF")
    return df1


def readClusteredDataDFWithID():
    print("- readClusteredDataDF")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT id, xValue, yValue, Label, Clustercore FROM ClusteredData").fetchall())
    conn.close()

    df1.columns = ['id', 'xValue', 'yValue', 'Label', 'Clustercore']

    print("+ readClusteredDataDF")
    return df1


def readClassificationData():
    print("- readClassificationData")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label FROM ClassifiedData").fetchall())
    conn.close()
    df1.columns = ['xValue', 'yValue', 'Label']

    X = df1[['xValue','yValue']]
    y = df1[['Label']].to_numpy().flatten()

    print("+ readClassificationData")
    return X, y


def readClassificationDataDF():
    print("- readClassificationDataDF")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label FROM ClassifiedData").fetchall())
    conn.close()
    df1.columns = ['xValue', 'yValue', 'Label']

    print("+ readClassificationDataDF")
    return df1


def readClassificationDataDFWithID():
    print("- readClassificationDataDF")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT id, xValue, yValue, Label FROM ClassifiedData").fetchall())
    conn.close()
    df1.columns = ['id', 'xValue', 'yValue', 'Label']

    print("+ readClassificationDataDF")
    return df1