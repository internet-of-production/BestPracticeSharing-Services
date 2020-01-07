# read data from input files

import pandas as pd
import sqlite3


def readInputDataFromDatabase():
    print("- readInputDataFromDatabase")

    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
#    df1 = pd.DataFrame(conn.execute("SELECT xValue, yValue, Label FROM RawData1").fetchall())
    df1 = pd.DataFrame(conn.execute("SELECT * FROM RawData1").fetchall())

#    print(df1)

    #df1 = df1.drop(columns=[0])
    df1 = df1.drop(df1.columns[0], axis = 1)

    colnum = len(df1.columns)
    df1 = df1.rename(columns={df1.columns[colnum-1]: "Label"})

#    print(df1)

    conn.close()

#    X = df1[[0,1]]
#    y = df1[[2]].to_numpy().flatten()

    print("+ readInputDataFromDatabase")
    return df1


def writeDataFromExcelToDatabase():
    print("- writeDataFromExcelToDatabase")

    df1 = pd.read_excel("featuresinputexcel.xlsx");
#    df2 = pd.read_excel("190905_PDM-Produktdatenbank_V06_rdn.xlsx");
#    df3 = pd.read_excel("190905_ERP-Arbeisplan_V06_rdn.xlsx");
#    df4 = pd.read_excel("190905_MDE-Arbeitsdatenbank_V06_rdn.xlsx");

    # sqlite
    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1.to_sql('RawData1', con=conn, if_exists='replace')
#    df2.to_sql('Produktdatenbank', con=conn, if_exists='replace', index_label='id')
#    df3.to_sql('Arbeisplan', con=conn, if_exists='replace', index_label='id')
#    df4.to_sql('Arbeitsdatenbank', con=conn, if_exists='replace', index_label='id')
    conn.commit()
    conn.close()

    print("+ writeDataFromExcelToDatabase")
    return 1
