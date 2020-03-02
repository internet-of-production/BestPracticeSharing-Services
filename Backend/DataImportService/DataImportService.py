#!flask/bin/python
from flask import Flask, redirect
import Backend.DataImportService.initialdataimport as di
import Backend.DataImportService.datapreparation as dp
from InputData.config import *

app = Flask(__name__)

@app.route('/dataimport/')
def index():
    di.writeDataFromExcelToDatabase()
    dp.writeTransformedData()
#
    if runlocally:
        return redirect("http://127.0.0.1:8000")
    else:
        return redirect("https://treibhaus.informatik.rwth-aachen.de/bps/")

if __name__ == '__main__':
    app.run(debug=True, port=5000)

