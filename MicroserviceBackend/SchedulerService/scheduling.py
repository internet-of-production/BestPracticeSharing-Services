
import time
import requests

def doScheduling():
    print("- doScheduling")

    print("executing Classification")
    requests.get(url="https://treibhaus.informatik.rwth-aachen.de/bps/classificationonclassification/")

    time.sleep(10)
    doScheduling()

    print("+ doScheduling")


