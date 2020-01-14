import random as rand
import time

# Local or Server version
runlocally = True

# Generate sample data
def generateRandomData():
    seed = time.time()
    rand.seed(seed)
    samples = rand.randint(10, 50)
    features = rand.randint(2, 10)
    centers = rand.randint(3, 10)
    std = rand.randint(1, 10)
    randomNumberOfVotes = rand.randint(9,15)
    return (seed, samples, features, centers, std, randomNumberOfVotes)

# Evaluation
evalIterations = 1000
saveLocalPlotsForEachIteration = False

# Evaluated
NumberOfVotes = {}
UsedFeedback = {}
Scores = {}

#
# import random as rand
#
# # Local or Server version
# runlocally = True
#
# # Generate sample data
# seed = 1
# rand.seed(seed)
# samples = 30
# features = 3  # rd.randint(2, 10)
# centers = 5  # rd.randint(3, 8)
# std = 3 #rand.randint(1, 10)
# #randomNumberOfVotes = rand.randint(9,15)
#
# # Evaluation
# evalIterations = 100
# saveLocalPlotsForEachIteration = False
#
# # Evaluated
# NumberOfVotes = {}
# UsedFeedback = {}
# Scores = {}
