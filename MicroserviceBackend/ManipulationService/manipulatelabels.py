
import MicroserviceBackend.RecommendationService.ClusteringService.clustering as cl

# manipulate specific label (label vector, position to manipulate, new label)
def manipulateLabel(y, i, label):
    print("- manipulateLabel")

    y[i] = label

    print("+ manipulateLabel")

    return 1


def manipulateLabelExample():
    print("- manipulateLabelExample")

    X, labels, core_samples_mask = cl.readClusteredData()

    for i in range(300):
       manipulateLabel(labels,i,3)

    cl.writeClusteringResult(X, labels, labels, core_samples_mask)

    print("+ manipulateLabelExample")
    return 1



