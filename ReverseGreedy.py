from operator import itemgetter
class ReverseGreedy():
    
    def getAlternativePaths(self, pathIndex, median, paths):
        alternativePaths = []
        pathIndex = 0
        for i in range(0, len(paths)):
            if i == pathIndex:
                continue

            for hop in paths[i]:
                if median.getId() == hop.getId():
                    alternativePaths.append(i)
                    break

        return alternativePaths 

    def merge(self, median, medianIndex, paths, altPathsIds):
        "Merging median with other median on same path to root"

        mergeCosts = []

        altPaths= [ paths[i] for i in altPathsIds]
        
        for path in altPaths:
            for hop in path:
                if len(hop.getNumOfReq()) > 0:
                    cost = self.computeCost(median, hop.getDepth())
                    mergeCosts.append(cost)

        if len(mergeCosts) != len(altPaths):
            print "Merge not working."

        minCostIndex, minCost = min(enumerate(mergeCosts), key=itemgetter(1))
        newMedians = self.getMediansFromPath(paths)
        newMedians[minCostIndex].mergeMedian(median)
        del newMedians[medianIndex]

        return minCost, newMedians

    def moveUp(self, median, medianIndex, paths):
        "Moving median up the tree"

        if (len(paths[medianIndex]) == 1): #We can't move up anymore
            return 9999999, newMedians
        
        currentMedian = paths[medianIndex][-1]
        del paths[medianIndex][-1]

        paths[medianIndex][-1].mergeMedian(currentMedian)
        newMedians = self.getMediansFromPath(paths)

        cost = self.computeCost(median, median.getDepth() - 1)
        return cost, newMedians

    def getMediansFromPath(self, paths):
        return list(map((lambda path: path[-1]), paths)) #list of ids of switches

    def computeCost(self, median, toDepth):
        cost = 0.0
        numOfRequests = median.getNumOfReq()
        reqDepths = median.getReqDepth()

        for i in range(0, len(numOfRequests)):
            cost += float(numOfRequests[i]) / float(reqDepths[i] + 1)

        return cost

    def reverseGreedy(self, lca, paths, userMovementPattern, k):
        #paths are oriented from lca to leaf
        totalCost = 0
        pathNum = 0
        medians = self.getMediansFromPath(paths)
        while len(medians) > k:
            removalCosts = []
            newStates = []
            for i in range(0, len(medians)):
                altPathsIds = self.getAlternativePaths(i, medians[i], paths)
                if altPathsIds:
                    cost, newMedians = self.merge(medians[i], i, paths, altPathsIds)
                else:
                    cost, newMedians = self.moveUp(medians[i], i, paths)

                removalCosts.append(cost)
                newStates.append(newMedians)

            minCostIndex, minCost = min(enumerate(removalCosts), key=itemgetter(1))
            medians = newStates[minCostIndex]
            

        return totalCost, medians