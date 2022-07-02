import math
import operator

class TrainPrediction:
    def __init__(self):
        pass
    
    def normalize_data(self, dlist):
        ndlist= []
        for liist in dlist:
            nliist = []
            for i in range(len(liist)):
                try:
                    elem = float(liist[i])
                    mmin = min([float(x[i]) for x in dlist])
                    mmax = max([float(x[i]) for x in dlist])
                    nliist.append(float(elem - mmin) / float(mmax-mmin))
                except Exception as e:
                    nliist.append(liist[i])          
            ndlist.append(nliist)
        return ndlist

    def euclideanDistance(self, instance1, instance2, length):
        distance = 0
        for x in range(1, length):
            if type(instance1[x]) == str: continue
            distance += pow((instance1[x] - instance2[x]), 2)
        return math.sqrt(distance)

    def getNeighbors(self, trainingSet, testInstance, k):
        distance = []
        length = len(testInstance) - 1
        for x in range((len(trainingSet))):
            dist = self.euclideanDistance(testInstance, trainingSet[x], length)
            distance.append((trainingSet[x], dist))
        distance.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(k):
            neighbors.append(distance[x][0])
        return neighbors

    def getResponse(self, neighbors):
        classVotes = {}
        for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
        sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
        return sortedVotes[0][0]

    def getAccuracy(self, testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
            if testSet[x][-1] == predictions[x]:
                correct += 1
        return (correct/float(len(testSet))) * 100.0

    def change(self, today, yest):
        if today > yest:
            return 1
        return 0

    def PAGR(self, testInstance, trainingSet, k):
        neighbors = self.getNeighbors(trainingSet, testInstance, k)
        return self.getResponse(neighbors)