
import MicroserviceBackend.DataImportService.dataimport as di
import MicroserviceBackend.DataImportService.datapreparation as dp
import MicroserviceBackend.RecommendationService.ClusteringService.clustering as cl
import MicroserviceBackend.RecommendationService.ClassifierService.classificaton as cf
import MicroserviceBackend.ManipulationService.manipulatelabels as ml
import MicroserviceBackend.DataViewService.plotclassification as pclass
import MicroserviceBackend.DataViewService.plotclustering as pclust

def runbackendOffline():

    di.writeDataFromExcelToDatabase()

    dp.writeTransformedData()
    dp.readTransformedData()

    cl.doClustering()
    pclust.plotClustering()

    ml.manipulateLabelExample()

    cf.doClassification()
    pclass.plotClassification()


runbackendOffline()