# read data from input files

import pandas as pd
import sqlite3


def readInputDataFromDatabase():
    print("- readInputDataFromDatabase")

#    conn = sqlite3.connect('/Users/stefanbraun/PycharmProjects/BPS Flask/BestPracticeSharing.sqlite')
    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label FROM RawData1").fetchall())
    conn.close()

    X = df1[[0,1]]
    y = df1[[2]].to_numpy().flatten()

    print("+ readInputDataFromDatabase")
    return df1

def writeDataFromExcelToDatabase():
    print("- writeDataFromExcelToDatabase")

#    df1 = pd.read_excel("/Users/stefanbraun/PycharmProjects/BPS Flask/featuresinputexcel.xlsx");
    df1 = pd.read_excel("featuresinputexcel.xlsx");

    # sqlite
#    conn = sqlite3.connect('/Users/stefanbraun/PycharmProjects/BPS Flask/BestPracticeSharing.sqlite')
    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1.to_sql('RawData1', con=conn, if_exists='replace', index_label='id')
    conn.commit()
    conn.close()

    print("+ writeDataFromExcelToDatabase")
    return 1
