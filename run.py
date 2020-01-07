
import MicroserviceBackend.DataImportService.initialdataimport as di
import MicroserviceBackend.DataImportService.datapreparation as dp
import MicroserviceBackend.RecommendationService.ClusteringService.clustering as cl
import MicroserviceBackend.RecommendationService.ClassifierService.classificaton as cf
import MicroserviceBackend.ManipulationService.manipulatelabels as ml
import MicroserviceFrontend.DataViewer.plotclassification as pclass
import MicroserviceFrontend.DataViewer.plotclustering as pclust
import threading
import os
import MicroserviceBackend.SchedulerService.SchedulerService as scs
import MicroserviceFrontend.Frontend as fes

def startService(path):

#    os.system("python " + path)
    os.system("python ./MicroserviceBackend/DataImportService/DataImportService.py")

#thread = threading.Thread(target=startService("./MicroserviceFrontend/Frontend.py"), args=())
#thread.daemon = True
#thread.start()
print("You have just executed the Frontend Service!")
thread = threading.Thread(target=startService("./MicroserviceBackend/DataImportService/DataImportService.py"))
thread.daemon = True
thread.start()
print("You have just executed the Data Import Service Service!")
