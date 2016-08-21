import csv

class CacheManager():
    def __init__(self, network):
        self.network = network
        self.maxDepth = 2

    def computeKMedianCaches(self, k=1, userId='All'):
        print "Computing k-median cache positions"

        userMovement = {}
        fieldnames = ['timestamp', 'hostIndex', 'AP']
        with open('/data/movement.csv', 'rb') as csvfile:
            movementData = csv.DictReader(csvfile, fieldnames, delimiter=',')
            for row in movementData:
                hi = int(row['hostIndex'])
                if hi < 30:
                    hi = 1
                if hi not in userMovement:
                    userMovement[hi] = {row['AP']: 1}
                else:
                    if row['AP'] not in userMovement[hi]:
                        userMovement[hi][row['AP']] = 1
                    else:
                        userMovement[hi][row['AP']] +=1

            if userId == 'All':
                for userId, userMovementPattern in userMovement.iteritems():
                    self.computeMedian(userMovementPattern)
            else:
                self.computeMedian(userMovement[userId])

    def computeMedian(self, userMovementPattern):
        print "Computing median"
        #get list of paths for all used access points
        paths = self.getPaths(userMovementPattern.keys())
        #Compute lowest common ancestor
        lca, depth = self.lowestCommonAncestor(paths)
        print depth
        print "name: " + lca.getAPName()

        #Move down the tree towards decreasing cost
        bestCost = self.computeCost(lca, lca, paths, userMovementPattern)

        bestCost, median = self.getBestCost(lca, lca, bestCost, paths, userMovementPattern )
        print "Best cost: " +str(bestCost)

    def getBestCost(self, lca, currentBest, bestCost, paths, userMovementPattern):
        cacheCandidates = currentBest.getChildren()
        for cacheCandidate in cacheCandidates:
            cost = self.computeCost(lca, cacheCandidate, paths, userMovementPattern)
            if cost < bestCost: #Minimiying the cost
                bestCost = cost
                median = cacheCandidate
                return self.getBestCost(lca, cacheCandidate, bestCost, paths, userMovementPattern)
                
        return bestCost, currentBest


    def getPaths(self, accessPoints):
        paths = []
        for ap in accessPoints:
            path = self.network.findPathToAP(ap)
            if path:
                paths.append(list(reversed(path)))

        return paths

    def computeCost(self, lca, candidate, paths, movementPattern):
        #lca is definitely in one of the paths
        #paths are oriented from lca to leaf
        totalCost = 0
        for path in paths:
            pathCost = 0
            candidateOnPath = False
            APName = path[ -1 ].getAPName()
            numOfRequests = movementPattern[APName]
            for hop in path:
                if candidate.getId() != hop.getId():
                    pathCost += self.costFunction(numOfRequests, hop.getDepth()) #Cost function
                else:
                    candidateOnPath = True
            
            if not candidateOnPath:
                pathCost += self.costFunction(numOfRequests, candidate.getDepth() - lca.getDepth())

            totalCost += pathCost

        return pathCost

    def costFunction(self, numOfRequests, depth):
        return float(numOfRequests) / (depth + 1)

    def lowestCommonAncestor(self, paths):
        print "Computing lowest common ancestor"
        
        if len(paths) == 1:
            return paths[0][-1], len(paths[0]) - 1

        for depth in range(0, len(paths[0])):
            lcaCandidate = paths[0][depth]
            for path in paths:
                if path[depth].getId() != lcaCandidate.getId():
                    return lcaCandidate, depth
        return paths[0][0], 0