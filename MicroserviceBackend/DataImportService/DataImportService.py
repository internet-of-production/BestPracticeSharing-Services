#!flask/bin/python
from flask import Flask, redirect, request, flash
import MicroserviceBackend.DataImportService.initialdataimport as di
import MicroserviceBackend.DataImportService.datapreparation as dp

app = Flask(__name__)

@app.route('/dataimport/')
def index():
    di.writeDataFromExcelToDatabase()
    dp.writeTransformedData()
    return redirect("https://treibhaus.informatik.rwth-aachen.de/bps/")


if __name__ == '__main__':
    app.run(debug=True, port=5000)

