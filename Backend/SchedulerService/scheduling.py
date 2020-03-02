import requests
from InputData.config import *

def doScheduling():
    print("- doScheduling")

    print("executing Clustering")

    if runlocally:
        requests.get("http://127.0.0.1:5001/clustering/")
    else:
        requests.get(url="https://treibhaus.informatik.rwth-aachen.de/bps/clusteringredirect/")

    time.sleep(10)
    doScheduling()

    print("+ doScheduling")


