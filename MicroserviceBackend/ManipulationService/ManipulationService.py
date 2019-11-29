#!flask/bin/python
from flask import Flask
import MicroserviceBackend.ManipulationService.manipulatelabels as ml

app = Flask(__name__)

@app.route('/manipulate/')
def index():
    ml.manipulateLabelExample()
    return "You have just executed the Manipulation Service!"


if __name__ == '__main__':
    app.run(debug=True, port=5003)

