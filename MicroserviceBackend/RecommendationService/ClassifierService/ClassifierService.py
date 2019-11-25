#!flask/bin/python
from flask import Flask
import MicroserviceBackend.RecommendationService.ClassifierService.classificaton as cf

app = Flask(__name__)

@app.route('/')
@app.route('/classificationonclustering/')
def onclustering():

    cf.doClassification('Clustering')

    return "You have just executed the Classifier Service!"


@app.route('/classificationonclassification/')
def onclassification():

    cf.doClassification('Classification')

    return "You have just executed the Classifier Service!"


if __name__ == '__main__':
    app.run(debug=True, port=5004)

