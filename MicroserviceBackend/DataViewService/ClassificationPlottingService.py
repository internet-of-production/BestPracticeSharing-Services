#!flask/bin/python
from flask import Flask
import MicroserviceBackend.DataViewService.plotclassification as pclass

app = Flask(__name__)

@app.route('/')
def index():

    pclass.plotClassification()

    return "You have just executed the Classification Plotting Service!"

if __name__ == '__main__':
    app.run(debug=True, port=5005)

