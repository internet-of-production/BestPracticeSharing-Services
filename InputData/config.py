import random as rand
import time

# Local or Server version
runlocally = True

# Generate sample data
def generateRandomData():
    seed = time.time()
    rand.seed(seed)
    samples = rand.randint(20, 50)
    features = rand.randint(4, 4)
    centers = rand.randint(5, 5)
    std = rand.randint(1, 10)
    MaxNumberOfVotes = 150 #rand.randint(10,150)
    return (seed, samples, features, centers, std, MaxNumberOfVotes)

# Evaluation
evalIterations = 10 #1000
saveLocalPlotsForEachIteration = False

# Evaluated
NumberOfVotes = {}
UsedFeedback = {}
Scores = {}
