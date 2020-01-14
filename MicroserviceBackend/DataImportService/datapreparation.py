
import MicroserviceBackend.DataImportService.initialdataimport as di
import sqlite3

# transform data
def transformData(silent = True):
    if not silent:  print("- transformData")

    df1 = di.readInputDataFromDatabase()
#    df1.columns = ['xValue', 'yValue', 'Label']

#    print(df1)

    if not silent:  print("+ transformData")
    return df1


# write data to data mart
def writeTransformedData(silent = True):
    if not silent:  print("- writeTransformedData")

    df1 = transformData()

    #    conn = sqlite3.connect('/Users/stefanbraun/PycharmProjects/BPS Flask/BestPracticeSharing.sqlite')
    conn = sqlite3.connect('BestPracticeSharing.sqlite')
    c = conn.cursor()
    df1.to_sql('TransformedData', con=conn, if_exists='replace')
    conn.commit()
    conn.close()

    if not silent:  print("+ writeTransformedData")

    return 0

