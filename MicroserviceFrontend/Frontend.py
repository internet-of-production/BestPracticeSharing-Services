#!flask/bin/python
from flask import Flask, send_file, render_template, flash, redirect, request
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix
import urllib.request
import DatabaseIO.readDatabase as rd
import MicroserviceFrontend.DataViewer.plotclassification as pclass
import MicroserviceFrontend.DataViewer.plotclustering as pclust
import MicroserviceFrontend.DataViewer.coordinatesplot as cs
import MicroserviceBackend.RecommendationService.VotingService.voting as vs
from DatabaseIO.config import *
import time
import pandas as pd


app = Flask(__name__)

app.config['REVERSE_PROXY_PATH'] = '/bps'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
ReverseProxyPrefixFix(app)

origin = "clustering"
current_process = 0


def return_origin():
    return (main_clusterresult())


@app.route('/bps/')
@app.route('/')
def index():
    return render_template('main.html', clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')
#    return render_template('main.html', clusteringPage = 'Ergebnis Clustering')


@app.route('/dataimportredirect')
def dataimportredirect():
    flash("You have just successfully executed the Data Import Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5000/dataimport/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/dataimport/")
    return(index())

@app.route('/manipulationredirect')
def manipulationredirect():
    flash("You have just successfully executed the Manipulation Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5003/manipulate/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/manipulate/")
    return(return_origin())

@app.route('/clusteringredirect')
def clusteringredirect():
    flash("You have just successfully executed the non-initial Clustering Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5001/clustering/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/clustering/")
    return(return_origin())

@app.route('/clusteringredirect_initial')
def clusteringredirect_initial():
    flash("You have just successfully executed the initial Clustering Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5001/clustering_initial/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/clustering_initial/")
    return(return_origin())

@app.route('/classficationonclusteringredirect')
def classficationonclusteringredirect():
    flash("You have just successfully executed the Clustering Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5004/classificationonclustering/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/classificationonclustering/")
    return(return_origin())

@app.route('/classficationonclassificationredirect')
def classficationonclassificationredirect():
    flash("You have just successfully executed the Clustering Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5004/classificationonclassification/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/classificationonclassification/")
    return(return_origin())

@app.route('/schedulerredirect')
def schedulerredirect():
    flash("You have just successfully executed the Scheduling Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5006/scheduler/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/scheduler/")
    return(return_origin())


@app.route('/bps/clusteringresult')
@app.route('/clusteringresult')
def main_clusterresult():
    global origin
    origin = "clustering"
    df1 = rd.readClusteredDataDFWithID()
    processes = [list(x) for x in df1.values]
    for x in processes:
        x[-2] = int(x[-2])
        x[0] = int(x[0])

    print(processes)
    return render_template('pages/clusteringresult.html', processes=processes, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


@app.route('/bps/specificclusteringresult/<int:procid>', methods=['GET'])
@app.route('/specificclusteringresult/<int:procid>', methods=['GET'])
def main_specificclusterresult(procid):
    global current_process
    current_process = procid
    global origin
    origin = "clustering"
    df1 = rd.readClusteredDataDFWithID()
    allprocesses = [list(x) for x in df1.values]
    for x in allprocesses:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    print(allprocesses)
    reference_process = [list(x) for x in df1.loc[[procid]].values]
    for x in reference_process:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    df1 = df1[df1['Label'] == int(df1['Label'].loc[[procid]])]
    df1 = df1.drop([procid], axis = 0)
    processes = [list(x) for x in df1.values]
    for x in processes:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    return render_template('pages/specificclusteringresult.html', processes=processes, reference_process=reference_process, allprocesses=allprocesses, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


@app.route('/bps/upvotepair/<int:procid>', methods=['GET'])
@app.route('/upvotepair/<int:procid>', methods=['GET'])
def main_upvote(procid):
    flash("You have successfully upvoted the corresponding pair!")
    global origin
    origin = "clustering"
    # Voting part start
    global current_process
    print("current_process", current_process)
    print("procid", procid)
    x1 =  current_process
    x2 =  procid
    vs.writeVotingResult(x1, x2, "upvote")
    # Voting part end
    df1 = rd.readClusteredDataDFWithID()
    reference_process = [tuple(x) for x in df1.loc[[current_process]].values]
    df1 = df1[df1['Label'] == int(df1['Label'].loc[[current_process]])]
    df1 = df1.drop([current_process], axis = 0)
    processes = [tuple(x) for x in df1.values]
    return render_template('pages/specificclusteringresult.html', processes=processes, reference_process=reference_process, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


@app.route('/bps/downvotepair/<int:procid>', methods=['GET'])
@app.route('/downvotepair/<int:procid>', methods=['GET'])
def main_downvote(procid):
    flash("You have successfully downvoted the corresponding pair!")
    global origin
    origin = "clustering"
    # Voting part start
    global current_process
    print("current_process", current_process)
    print("procid", procid)
    x1 =  current_process
    x2 =  procid
    vs.writeVotingResult(x1, x2, "downvote")
    # Voting part end
    df1 = rd.readClusteredDataDFWithID()
    reference_process = [tuple(x) for x in df1.loc[[current_process]].values]
    df1 = df1[df1['Label'] == int(df1['Label'].loc[[current_process]])]
    df1 = df1.drop([current_process], axis = 0)
    processes = [tuple(x) for x in df1.values]
    return render_template('pages/specificclusteringresult.html', processes=processes, reference_process=reference_process, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


@app.route('/bps/classificationresult')
@app.route('/classificationresult')
def main_classificationresult():
    global origin
    origin = "classification"
    df1 = rd.readClassificationDataDFWithID()
    processes = [tuple(x) for x in df1.values]
    return render_template('classificationresult.html', processes=processes, clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/bps/specificclassificationresult/<int:procid>', methods=['GET'])
@app.route('/specificclassificationresult/<int:procid>', methods=['GET'])
def main_specificclassificationresult(procid):
    global origin
    origin = "classification"
    df1 = rd.readClassificationDataDFWithID()
    allprocesses = [list(x) for x in df1.values]
    for x in allprocesses:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    reference_process = [list(x) for x in df1.loc[[procid]].values]
    for x in reference_process:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    print("ref_process",reference_process)
    df1 = df1[df1['Label'] == int(df1['Label'].loc[[procid]])]
    df1 = df1.drop([procid], axis = 0)
    processes = [list(x) for x in df1.values]
    for x in processes:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    return render_template('specificclassificationresult.html', processes=processes, reference_process=reference_process, allprocesses=allprocesses, clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/bps/clusteringresult.png')
@app.route('/clusteringresult.png')
def main_plot_clustering():
    img = pclust.plotClustering()
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/bps/clusteringresult2D.png')
@app.route('/clusteringresult2D.png')
def main_plot_clustering2D():
    time.sleep(1)
    img = pclust.plotClustering2D()
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/bps/clusteringresult1D.png/<int:axis>', methods=['GET'])
@app.route('/clusteringresult1D.png/<int:axis>', methods=['GET'])
def main_plot_clustering1D(axis):
    time.sleep(axis*2)
    img = pclust.plotClustering1D()
#    img = pclust.plotClustering1D(axis)
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/bps/clusteringresult_real.png')
@app.route('/clusteringresult_real.png')
def main_plot_clustering_real():
    print("real")
    time.sleep(5)
    img2 = pclust.plotClustering(Inputdata = "")
    return send_file(img2, mimetype='image/png', cache_timeout=0)


@app.route('/bps/classificationresult.png')
@app.route('/classificationresult.png')
def main_plot_classification():
    img = pclass.plotClassification()
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/detailsSimilarityanalysisPage')
def detailsSimilarityanalysisPage():
    d = {'Merkmale': ["Technologie", "Herstellkosten", "Material"]}
    df1 = pd.DataFrame(data=d)
    liste = [tuple(x) for x in df1.values]
    d = ["Prozess 1", "Prozess 6", "Prozess 7", "Prozess 8", "Prozess 9", "Prozess 10"]
    activities = d
    print(activities)
    return render_template('pages/detailsSimilarity.html', list=liste, activities=activities)


@app.route('/detailsComparison')
def detailsComparison():
    d = {'Merkmale': ["Technologie", "Herstellkosten", "Material", "Gewicht", "Geometrie"]}
    df1 = pd.DataFrame(data=d)
    liste = [tuple(x) for x in df1.values]
    d = {'Merkmale': ["Prozess 1", "Prozess 2", "Prozess 3", "Prozess 4"]}
    df2 = pd.DataFrame(data=d)
    liste2 = [tuple(x) for x in df2.values]
    d = ["Prozess 1", "Prozess 6", "Prozess 7", "Prozess 8", "Prozess 9", "Prozess 10"]
    activities = d
    print(activities)
    return render_template('pages/detailsComparison.html', list=liste, list2=liste2, activities=activities)


@app.route('/konfigurator')
def konfigurator():
    return render_template('main.html', clusteringPage = 'Ergebnis Clustering', classificationPage = 'Ergebnis Classification')


@app.route('/bps/coordinatesplot/')
@app.route('/coordinatesplot')
@app.route('/plotcoordinates')
@app.route('/bps/plotcoordinates')
def plotcoordinates():
#    img = pclust.plotClustering1D(axis)
    img = cs.plotCoordinatesPlot()
#    return img
    return send_file(img, mimetype='image/png', cache_timeout=0)
def main_coordinatesplot():
#    img = pclust.plotClustering1D(axis)
    img = cs.plotCoordinatesPlot()
#    return img
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/bps/specificclusteringresult_popup/<int:procid>', methods=['GET'])
@app.route('/specificclusteringresult_popup/<int:procid>', methods=['GET'])
def main_specificclusterresult_popup(procid):
    global current_process
    current_process = procid
    global origin
    origin = "clustering"
    df1 = rd.readClusteredDataDFWithID()
    allprocesses = [list(x) for x in df1.values]
    for x in allprocesses:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    print(allprocesses)
    reference_process = [list(x) for x in df1.loc[[procid]].values]
    for x in reference_process:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    df1 = df1[df1['Label'] == int(df1['Label'].loc[[procid]])]
    df1 = df1.drop([procid], axis = 0)
    processes = [list(x) for x in df1.values]
    for x in processes:
        x[-2] = int(x[-2])
        x[0] = int(x[0])
    return render_template('pages/specificclusteringresult_popup.html', processes=processes, reference_process=reference_process, allprocesses=allprocesses, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')



#
# def plotcoordinates():
#     cs.plotCoordinatesPlot()
#     return return_origin()



# @app.route('/plotcoordinates')
# def plotcoordinates():
#     img = cs.plotCoordinatesPlot()
#     return send_file(img, mimetype='image/png', cache_timeout=0)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
