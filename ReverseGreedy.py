from operator import itemgetter
from copy import deepcopy

class ReverseGreedy():
    
    def getAlternativePaths(self, pathIndex, paths):
        alternativePaths = []

        median = paths[pathIndex][-1]

        for i in range(0, len(paths)):
            if i == pathIndex:
                continue

            for hop in paths[i]:
                if median.getId() == hop.getId():
                    alternativePaths.append(i)
                    break

        return alternativePaths 

    def getMediansFromPath(self, paths):
        return list(map((lambda path: path[-1]), paths)) #list of ids of switches

    def computeCost(self, median, toDepth, fromDepth, isMerge):
        cost = 0.0
        numOfRequests = median.getNumOfReq()
        reqDepths = median.getReqDepth()
        #print "len(numOfRequests) %d" % len(numOfRequests)

        if isMerge:
            for depth in range(toDepth, fromDepth):
                for i in range(0, len(numOfRequests)):
                    cost += float(numOfRequests[i]) / float(depth + 1)

        else:
            for i in range(0, len(numOfRequests)):
                cost += float(numOfRequests[i]) / float((abs(toDepth - reqDepths[i]) + 1 ))



        return cost

    def merge(self, medianIndex, paths, altPathsIds):
        "Merging median with other median on same path to root"
        mergeCosts = []
        altPaths= [ paths[j] for j in altPathsIds]

        median = paths[medianIndex][-1]

        for path in altPaths:
            for hop in path:
                if len(hop.getNumOfReq()) > 0 and hop.getId() != median.getId():
                    print "Hop %d depth %d, med %d depth %d " % (hop.getId(), hop.getDepth(), median.getId() ,median.getDepth())
                    merged = deepcopy(hop).mergeMedian(median)
                    cost = self.computeCost(median, median.getDepth(), hop.getDepth(), True)
                    mergeCosts.append(cost)
                    break

        if len(mergeCosts) != len(altPaths):
            print "Merge not working."

        minCostIndex, minCost = min(enumerate(mergeCosts), key=itemgetter(1))

        altPaths[minCostIndex][-1].mergeMedian(median)

        return minCost, altPaths

    def moveUp(self, medianIndex, paths):
        "Moving median up the tree"

        if (len(paths[medianIndex]) == 1): #We can't move up anymore
            return 9999999, paths
        
        currentMedian = paths[medianIndex][-1]
        pths = paths
        pths[medianIndex][-2].mergeMedian(pths[medianIndex][-1])
        del pths[medianIndex][-1]
        print str(currentMedian.getId()) + " on depth %d" % currentMedian.getDepth()
        cost = self.computeCost(currentMedian, currentMedian.getDepth() - 1, 0, False)

        return cost, pths

    def reverseGreedy(self, lca, paths, k):
        #paths are oriented from lca to leaf
        totalCost = 0
        pathNum = 0
        print paths
        while len(paths) > k:
            removalCosts = []
            newPaths = []
            #print "1. )Len paths %d" % len(paths)
            for i in range(0, len(paths)):
            #    print "2. )Len paths %d" % len(paths)
                p = deepcopy(paths)
                altPathsIds = list(self.getAlternativePaths(i, p))
                mi = paths[i][-1].getId()
                if altPathsIds:
                    cost, np = self.merge(i, p, altPathsIds)
                    print " %d.) Cache %d is merged. Cost: %.3f" % (i, mi, cost)

                else:
                    cost, np = self.moveUp(i, p)
                    print "%d.) Cache %d is moved up. Cost: %.3f" % (i, mi, cost)


                removalCosts.append(cost)
                newPaths.append(deepcopy(np))

            minCostIndex, minCost = min(enumerate(removalCosts), key=itemgetter(1))
            #print "4. )Len paths %d" % len(paths)
            paths = newPaths[minCostIndex]
            #print "5. )Len paths %d" % len(paths)

            #print "Lowest cost: %.2f ,Action:%d  ,len(newmedians): %d" % (minCost,minCostIndex, len(paths)) 
            #print paths
            
            print "\n==================================================\n"

            
        return totalCost, paths