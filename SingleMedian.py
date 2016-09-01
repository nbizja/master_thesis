import math

class SingleMedian():

    def getBestCost(self, lca, currentBest, bestCost, paths, userMovementPattern):
        cacheCandidates = currentBest.getChildren()
        #print "First best cost %d" % bestCost
        for cacheCandidate in cacheCandidates:
            cost = self.computeSingleMedian(lca, cacheCandidate, paths, userMovementPattern)
            #print "Cache candidate %d has cost of %d" % (cacheCandidate.getId(), cost)
            if cost < bestCost: #Minimiying the cost
                bestCost = cost
                median = cacheCandidate
                return self.getBestCost(lca, cacheCandidate, bestCost, paths, userMovementPattern)
                
        return bestCost, currentBest

    def computeSingleMedian(self, lca, candidate, paths, movementPattern):
        #lca is definitely in one of the paths
        #paths are oriented from lca to leaf
        totalCost = 0
        pathNum = 0
        for path in paths:
            pathCost = 0
            candidateOnPath = False
            APName = path[ -1 ].getAPName()
            numOfRequests = movementPattern[APName]
            for hop in reversed(path):
                if candidate.getId() != hop.getId():
                    pathCost += self.costFunction(numOfRequests, hop.getDepth()) #Cost function
                else:
                    candidateOnPath = True
                    break
            
            if not candidateOnPath:
                #print "Candidate %d not on path - depth %d" % (candidate.getId(), candidate.getDepth() - lca.getDepth()) 
                pathCost += self.costFunction(numOfRequests, candidate.getDepth() - lca.getDepth())

            #print "Path %d has cost %d" % (pathNum, pathCost)
            totalCost += pathCost
            pathNum += 1

        return totalCost

    def costFunction(self, numOfRequests, depth):
        return float(numOfRequests) / float(depth + 1) #math.pow(numOfRequests, -1 * (depth + 1))

    def lowestCommonAncestor(self, paths):
        #print "Computing lowest common ancestor"
        #print paths
    
        if len(paths) == 1:
            return paths[0][-1], len(paths[0]) - 1

        for depth in range(0, len(paths[0])):
            lcaCandidate = paths[0][depth]
            #print "Candidate id: %d" % lcaCandidate.getId()
            for path in paths:
                if path[depth].getId() != lcaCandidate.getId():
                    return paths[0][depth - 1], depth - 1 #return previous candidate

        return paths[0][0], 0