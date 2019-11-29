#!flask/bin/python
from flask import Flask
import MicroserviceBackend.RecommendationService.ClusteringService.clustering as cl

app = Flask(__name__)


@app.route('/clustering/')
def index():
    cl.doClustering()
    return "You have just successfully executed the Clustering Service!"


if __name__ == '__main__':
    app.run(debug=True, port=5001)

