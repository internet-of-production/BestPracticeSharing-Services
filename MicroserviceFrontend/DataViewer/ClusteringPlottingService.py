#!flask/bin/python
from flask import Flask, flash
import MicroserviceFrontend.DataViewer.plotclustering as pclust

app = Flask(__name__)

@app.route('/')
def index():
    pclust.plotClustering()
    return "You have just executed the Clustering Plotting Service!"


if __name__ == '__main__':
    app.run(debug=True, port=5002)

