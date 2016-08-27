from SingleMedian import SingleMedian
from ReverseGreedy import ReverseGreedy
import csv
import operator

class CacheManager():

    REVERSE_GREEDY = 'reverse_greedy'

    def __init__(self, network):
        self.network = network
        self.maxDepth = 2

    def computeKMedianCaches(self, k=1, userId='All', userMovement={}):
        print "Computing k-median cache positions"

        fieldnames = ['timestamp', 'hostIndex', 'AP']

        if not userMovement:
            userMovement = self.getMovementPattern

        if userId == 'All':
            for userId, userMovementPattern in userMovement.iteritems():
                self.computeMedian(userMovementPattern, k)
        else:
            self.computeMedian(userMovement[userId], k)

    def computeMedian(self, userMovementPattern, k=1, strategy=REVERSE_GREEDY):
        print "Computing median"
        #get list of paths for all used access points
        paths = self.getPaths(userMovementPattern)

        #Compute lowest common ancestor
        singleMedian = SingleMedian()

        lca, depth = singleMedian.lowestCommonAncestor(paths)

        if k == 1:
            #Move down the tree towards decreasing cost
            bestCost = singleMedian.computeSingleMedian(lca, lca, paths, userMovementPattern)
            bestCost, median = singleMedian.getBestCost(lca, lca, bestCost, paths, userMovementPattern)
            print "S%d is the best location." % median.getId()

        elif strategy == self.REVERSE_GREEDY:
            greedy = ReverseGreedy()
            bestCost, medians = greedy.reverseGreedy(lca, paths, userMovementPattern, k)
            print " Best locations:"
            print list(map((lambda median: median.getId()), medians))


        print "Best cost: " +str(bestCost)
        
        print "Depth: %d" % depth
        print "LCA: S%d" % lca.getId()

    def getMovementPattern(self):
        userMovement = {}
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
        return userMovement


    def getPaths(self, movementPattern):
        print "Getting paths"
        accessPoints = movementPattern.keys()
        paths = []
        for ap in accessPoints:
            print "Getting path for " + ap
            path = self.findPathToAP(self.network, ap, movementPattern[ap])
            if len(path):
                paths.append(path)

        return paths

    def findPathToAP(self, mySwitch, APName, numOfReq):
        if mySwitch.APName == APName:
            mySwitch.setNumOfReq([numOfReq])
            mySwitch.setReqDepth([mySwitch.getDepth()])

            return [mySwitch]
        if mySwitch.isAP:
            return []

        for child in mySwitch.getChildren():
            childPath = self.findPathToAP(child, APName, numOfReq)
            if len(childPath) > 0:
                return [mySwitch] + childPath
        
        return []