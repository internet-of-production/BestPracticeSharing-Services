
import MicroserviceBackend.DataImportService.dataimport as di
import pandas as pd
import sqlite3

# transform data
def transformData():
    print("- transformData")

    df1 = di.readInputDataFromDatabase()
    df1.columns = ['xValue', 'yValue', 'Label']

    print("+ transformData")
    return df1

# write data to data mart
def writeTransformedData():
    print("- writeTransformedData")

    df1 = transformData()

    #    conn = sqlite3.connect('/Users/stefanbraun/PycharmProjects/BPS Flask/BestPracticeSharing.sqlite')
    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1.to_sql('TransformedData', con=conn, if_exists='replace', index_label='id')
    conn.commit()
    conn.close()

    print("+ writeTransformedData")

    return 0

# read data from data mart
def readTransformedData():
    print("- readTransformedData")

    #    conn = sqlite3.connect('/Users/stefanbraun/PycharmProjects/BPS Flask/BestPracticeSharing.sqlite')
    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label FROM TransformedData").fetchall())
    conn.close()
    df1.columns = ['xValue', 'yValue', 'Label']

    X = df1[['xValue','yValue']]
    y = df1[['Label']].to_numpy().flatten()

    return X, y