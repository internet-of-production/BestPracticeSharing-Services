#!flask/bin/python
from flask import Flask, send_file, render_template
import DatabaseIO.readDatabase as rd
import MicroserviceFrontend.DataViewer.plotclassification as pclass
import MicroserviceFrontend.DataViewer.plotclustering as pclust

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html', clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/clusteringresult')
def main_clusterresult():
    df1 = rd.readClusteredDataDFWithID()
    processes = [tuple(x) for x in df1.values]
    return render_template('clusteringresult.html', processes=processes, clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/specificclusteringresult/<int:procid>', methods=['GET'])
def main_specificclusterresult(procid):
    df1 = rd.readClusteredDataDFWithID()
    reference_process = [tuple(x) for x in df1.loc[[procid]].values]
    df1 = df1[df1['Label'] == int(df1['Label'].loc[[procid]])]
    df1 = df1.drop([procid], axis = 0)
    processes = [tuple(x) for x in df1.values]
    return render_template('specificclusteringresult.html', processes=processes, reference_process=reference_process, clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/classificationresult')
def main_classificationresult():
    df1 = rd.readClassificationDataDFWithID()
    processes = [tuple(x) for x in df1.values]
    return render_template('classificationresult.html', processes=processes, clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/specificclassificationresult/<int:procid>', methods=['GET'])
def main_specificclassificationresult(procid):
    df1 = rd.readClassificationDataDFWithID()
    reference_process = [tuple(x) for x in df1.loc[[procid]].values]
    df1 = df1[df1['Label'] == int(df1['Label'].loc[[procid]])]
    df1 = df1.drop([procid], axis = 0)
    processes = [tuple(x) for x in df1.values]
    return render_template('specificclassificationresult.html', processes=processes, reference_process=reference_process, clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/clusteringresult.png')
def main_plot_clustering():
    img = pclust.plotClustering()
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/classificationresult.png')
def main_plot_classification():
    img = pclass.plotClassification()
    return send_file(img, mimetype='image/png', cache_timeout=0)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
