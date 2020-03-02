#!flask/bin/python
from flask import Flask
import Backend.RecommendationService.ClusteringService.clustering as cl

app = Flask(__name__)


@app.route('/')
@app.route('/clustering/')
def index():
    cl.doClustering()
    return "You have just successfully executed the Clustering Service!"


@app.route('/clustering_initial/')
def index2():
    cl.doClustering(initial = True)
    return "You have just successfully executed the initial Clustering Service!"


if __name__ == '__main__':
    app.run(debug=True, port=5001)
