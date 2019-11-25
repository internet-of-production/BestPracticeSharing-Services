#!flask/bin/python
from flask import Flask
import MicroserviceBackend.DataImportService.initialdataimport as di
import MicroserviceBackend.DataImportService.datapreparation as dp

app = Flask(__name__)

@app.route('/dataimport/')
def index():

    di.writeDataFromExcelToDatabase()
    dp.writeTransformedData()

    return "You have just executed the Data Import Service!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)

