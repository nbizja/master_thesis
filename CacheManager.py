from SingleMedian import SingleMedian
from ReverseGreedy import ReverseGreedy
import csv
import operator

class CacheManager():

    REVERSE_GREEDY = 'reverse_greedy'
    ALL_USERS = 'All'

    def __init__(self, network):
        self.network = network
        self.maxDepth = 2

    def computeKMedianCaches(self, k=1, userId=ALL_USERS, userMovement={}):
        #print "Computing k-median cache positions"

        fieldnames = ['timestamp', 'hostIndex', 'AP']

        if not userMovement:
            userMovement = self.getMovementPattern()

        if userId == self.ALL_USERS:
            medians = {}
            for userId, userMovementPattern in userMovement.iteritems():
                if len(userMovementPattern) > 0:
                    medians[(userId % 50) + 1] = self.computeMedian(userMovementPattern, k)

            return medians
        else:
            return {userId: self.computeMedian(userMovement[userId], k)}

    def computeMedian(self, userMovementPattern, k=1, strategy=REVERSE_GREEDY):
        #print "Computing median"
        #get list of paths for all used access points
        paths = self.getPaths(userMovementPattern)
        print "Paths len %d " % len(paths)
        if len(paths) == 0:
            print "Should not happen!"
        #Compute lowest common ancestor
        singleMedian = SingleMedian()

        lca, depth = singleMedian.lowestCommonAncestor(paths)
        #print "LCA: S%d" % lca.getId()

        if k == 1:
            #Move down the tree towards decreasing cost
            bestCost = singleMedian.computeSingleMedian(lca, lca, paths, userMovementPattern)
            bestCost, median = singleMedian.getBestCost(lca, lca, bestCost, paths, userMovementPattern)
            #print "S%d is the best location." % median.getId()

            return median.getId()

        elif strategy == self.REVERSE_GREEDY:
            print "Starting reverse greedy"
            greedy = ReverseGreedy()
            bestCost, p = greedy.reverseGreedy(lca, paths, k)
            bestLocations = list(map((lambda path: path[-1].getId()), p))

            print " Best locations:"
            print bestLocations

            return bestLocations



    def getMovementPattern(self):
        userMovement = {}
        fieldnames = ['timestamp', 'hostIndex', 'AP']

        with open('/data/movement.csv', 'rb') as csvfile:
            movementData = csv.DictReader(csvfile, fieldnames, delimiter=',')
            for row in movementData:
                hi = int(row['hostIndex'])

                if hi not in userMovement:
                    userMovement[hi] = {row['AP']: 1}
                else:
                    if row['AP'] not in userMovement[hi]:
                        userMovement[hi][row['AP']] = 1
                    else:
                        userMovement[hi][row['AP']] +=1
        print userMovement[24]
        
        return userMovement


    def getPaths(self, movementPattern):
        accessPoints = movementPattern.keys()
        paths = []
        for ap in accessPoints:
            print "Getting path for " + ap
            path = self.findPathToAP(self.network, ap, movementPattern[ap])
            print path
            print ""
            if len(path):
                paths.append(path)

        return paths

    def findPathToAP(self, mySwitch, APName, numOfReq):
        #print mySwitch.getAPName() + " == " + APName + " ?"

        if mySwitch.getAPName() == APName:
            #print "S%d == %s" % (mySwitch.getId(), APName)
            mySwitch.setNumOfReq([numOfReq])
            mySwitch.setReqDepth([mySwitch.getDepth()])
            return [mySwitch]

        if mySwitch.isAP:
            return []

        for child in mySwitch.getChildren():
            #print "S%d has child s%d with path:" % (mySwitch.getId(), child.getId())
            childPath = self.findPathToAP(child, APName, numOfReq)
            #print childPath
            if len(childPath) > 0:
                return [mySwitch] + childPath
        
        return []


    def findPathToSwitch(self, mySwitch, targetSwitchId):
        if mySwitch.getId() == targetSwitchId:
            return [mySwitch.getId()]

        if mySwitch.isAP:
            return []

        for child in mySwitch.getChildren():
            childPath = self.findPathToSwitch(child, targetSwitchId)
            if len(childPath) > 0:
                return [mySwitch.getId()] + childPath
        
        return []

    def distance(self, root, s1Id, s2Id):
        "Calculates hop counts between two switches"
        path1 = self.findPathToSwitch(root, s1Id)
        path2 = self.findPathToSwitch(root, s2Id)
        print "\nDistance between s%d and s%d is " % (s1Id, s2Id)
        print path1
        print path2
        print len(list(set(path1 + path2)))
        return len(list(set(path1 + path2)))


