#!flask/bin/python
from flask import Flask, send_file, render_template, flash
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix
import urllib.request
import DatabaseIO.readDatabase as rd
import Frontend.DataViewer.plotclustering as pclust
import Frontend.DataViewer.coordinatesplot as cs
import Backend.RecommendationService.VotingService.voting as vs
from InputData.config import *
import time
import pandas as pd
from flask import request
from werkzeug.routing import BaseConverter

class IntListConverter(BaseConverter):
    regex = r'\d+(?:,\d+)*,?'

    def to_python(self, value):
        return [int(x) for x in value.split(',')]

    def to_url(self, value):
        return ','.join(str(x) for x in value)

app = Flask(__name__)
app.url_map.converters['int_list'] = IntListConverter

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
    return render_template('/startpage.html', clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')
#    return render_template('startpage.html', clusteringPage = 'Ergebnis Clustering')


@app.route('/dataimportredirect')
def dataimportredirect():
    flash("You have just successfully executed the Data Import Service!")
    if runlocally:
        urllib.request.urlopen("http://127.0.0.1:5000/dataimport/")
    else:
        urllib.request.urlopen("https://treibhaus.informatik.rwth-aachen.de/bps/dataimport/")
    return(index())

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
    return render_template('clusteringresult.html', processes=processes, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


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
    return render_template('specificclusteringresult.html', processes=processes, reference_process=reference_process, allprocesses=allprocesses, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


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
    return render_template('specificclusteringresult.html', processes=processes, reference_process=reference_process, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


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
    return render_template('specificclusteringresult.html', processes=processes, reference_process=reference_process, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


@app.route('/bps/clusteringresult.png')
@app.route('/clusteringresult.png')
def main_plot_clustering():
    img = pclust.plotClustering2D()
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/bps/clusteringresult2D.png/<int_list:axis>')
@app.route('/clusteringresult2D.png/<int_list:axis>')
def main_plot_clustering2D(axis):
    time.sleep(1)
    xAxis = int(axis[0])
    yAxis = int(axis[1])
    img = pclust.plotClustering2D(xAxis = xAxis, yAxis = yAxis)
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/bps/clusteringresult1D.png/<int_list:axis>', methods=['GET'])
@app.route('/clusteringresult1D.png/<int_list:axis>', methods=['GET'])
def main_plot_clustering1D(axis):
    time.sleep(axis[0]*2)
    print("axis",axis)
#   axis = str(axis)
    xAxis = int(axis[0])
    yAxis = int(axis[1])
    print(xAxis,yAxis)
    img = pclust.plotClustering1D(xAxis = xAxis, yAxis = yAxis)
    return send_file(img, mimetype='image/png', cache_timeout=0)


@app.route('/bps/clusteringresult_real.png')
@app.route('/clusteringresult_real.png')
def main_plot_clustering_real():
    print("real")
    time.sleep(5)
    img2 = pclust.plotClustering2D(Inputdata = "")
    return send_file(img2, mimetype='image/png', cache_timeout=0)

@app.route('/detailsSimilarityanalysisPage', methods=["GET", "POST"])
def detailsSimilarityanalysisPage():
    if request.method == "GET":
        print("get")
        dfTMP = rd.readClusteredDataDF()
        listeTMP = [x for x in dfTMP.columns]
        listeTMP = listeTMP[1:-2]
        d = {'Merkmale': listeTMP}
        df1 = pd.DataFrame(data=d)
        liste = [tuple(x) for x in df1.values]
        d = ["Prozess 1", "Prozess 6", "Prozess 7", "Prozess 8", "Prozess 9", "Prozess 10"]
        activities = d
        checked = [1,2]
        print(checked)
        return render_template('detailsSimilarity.html', list=liste, checked_boxes=checked, activities=activities)
    else:
        tickedBoxes = request.form.getlist("SimilariyPageMerkmaleKeys")
#        print(tickedBoxes)
        checked = [int(x[1]) for x in tickedBoxes]
        print(checked)
        dfTMP = rd.readClusteredDataDF()
        listeTMP = [x for x in dfTMP.columns]
        listeTMP = listeTMP[1:-2]
        d = {'Merkmale': listeTMP}
        df1 = pd.DataFrame(data=d)
        liste = [tuple(x) for x in df1.values]
        d = ["Prozess 1", "Prozess 6", "Prozess 7", "Prozess 8", "Prozess 9", "Prozess 10"]
        activities = d
        return render_template('detailsSimilarity.html', list=liste, checked_boxes=checked, activities=activities)


@app.route('/detailsComparison', methods=["GET", "POST"])
def detailsComparison():
    if request.method == "GET":
        dfTMP = rd.readClusteredDataDF()
        listeTMP = [x for x in dfTMP.columns]
        listeTMP = listeTMP[1:-2]
        d = {'Merkmale': listeTMP}
        df1 = pd.DataFrame(data=d)
        liste = [tuple(x) for x in df1.values]
        d = {'Merkmale': ["Prozess 1", "Prozess 2", "Prozess 3", "Prozess 4", "Prozess 5", "Prozess 6"]}
        df2 = pd.DataFrame(data=d)
        liste2 = [tuple(x) for x in df2.values]
        d = ["Prozess 1", "Prozess 6", "Prozess 7", "Prozess 8", "Prozess 9", "Prozess 10"]
        activities = d
        print(activities)
        checked = listeTMP
        return render_template('detailsComparison.html', list=liste, list2=liste2, checked_boxes=checked, activities=activities)
    else:
        tickedBoxes = request.form.getlist("ComparisonPageMerkmaleKeys")
        checked = [int(x[1]) for x in tickedBoxes]
        dfTMP = rd.readClusteredDataDF()
        listeTMP = [x for x in dfTMP.columns]
        listeTMP = listeTMP[1:-2]
        d = {'Merkmale': listeTMP}
        df1 = pd.DataFrame(data=d)
        liste = [tuple(x) for x in df1.values]
        d = {'Merkmale': ["Prozess 1", "Prozess 2", "Prozess 3", "Prozess 4", "Prozess 5", "Prozess 6"]}
        df2 = pd.DataFrame(data=d)
        liste2 = [tuple(x) for x in df2.values]
        d = ["Prozess 1", "Prozess 6", "Prozess 7", "Prozess 8", "Prozess 9", "Prozess 10"]
        activities = d
        print(activities)
        return render_template('detailsComparison.html', list=liste, list2=liste2, checked_boxes=checked, activities=activities)


@app.route('/konfigurator')
def konfigurator():
    return render_template('startpage.html', clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


@app.route('/bps/coordinatesplot/<int_list:axis>')
@app.route('/coordinatesplot/<int_list:axis>')
@app.route('/plotcoordinates/<int_list:axis>')
@app.route('/bps/plotcoordinates/<int_list:axis>')
def plotcoordinates(axis):
#    img = pclust.plotClustering1D(axis)
    img = cs.plotCoordinatesPlot(axis = axis)
#    return img
    return send_file(img, mimetype='image/png', cache_timeout=0)
def main_coordinatesplot(axis):
#    img = pclust.plotClustering1D(axis)
    img = cs.plotCoordinatesPlot(axis = axis)
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
    return render_template('PopUps/specificclusteringresult_popup.html', processes=processes, reference_process=reference_process, allprocesses=allprocesses, clusteringPage ='Ergebnis Clustering', classificationPage ='Ergebnis Classification')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
