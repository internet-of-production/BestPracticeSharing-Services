#!flask/bin/python
from flask import Flask
import MicroserviceBackend.RecommendationService.ClassifierService.classificaton as cf

app = Flask(__name__)

@app.route('/')
def index():

    cf.doClassification()

    return "You have just executed the Classifier Service!"

if __name__ == '__main__':
    app.run(debug=True, port=5004)

