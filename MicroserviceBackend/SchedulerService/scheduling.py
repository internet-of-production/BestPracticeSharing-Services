
import time
import requests

def doScheduling():
    print("- doScheduling")

    print("executing Classification")
    requests.get(url="http://137.226.232.236:5004/")

    time.sleep(3600)
    doScheduling()

    print("+ doScheduling")


