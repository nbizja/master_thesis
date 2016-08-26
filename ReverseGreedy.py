class ReverseGreedy():
	
	def __init__(self):


	def hopOnOtherPaths(self, hop, otherPaths):
	    resultPath = []
	    pathIndex = 0
	    for path in otherPaths:
	        for otherHop in path:
	            if hop.getId() == otherHop.getId() and (len(path) < len(resultPath) or len(resultPath) == 0):
	                resultPath = path
	        pathIndex += 1

	    return resultPath, pathIndex

	def mergeToOtherPath(self, sharedPath, sharedPathIndex,  path):
	    mergedPathCost = []


	def reverseGreedy(self, lca, paths, userMovementPattern, k):
	    #paths are oriented from lca to leaf
	    totalCost = 0
	    pathNum = 0
	    medians = list(map((lambda path: path[-1].getId(), paths))) #list of ids of switches
	        
	    while len(medians) > k:
	        removalCosts = []
	        newStates = []
	        otherPaths = paths
	        for i in range(0, len(medians)):
	        	del otherPaths[i]
	        	pathGroup = self.hopOnOtherPaths(medians[i], otherPaths):
	        	if pathGroup:
	        		cost, newMedians = merge(mediana[i], pathGroup)
	        	else:
	        		cost, newMedians = moveUp(median[i], paths[i])

	        	removalCosts.append(cost)
	        	newStates.append(newMedians)

	        minCostIndex, minCost = min(enumerate(removalCosts), key=operator.itemgetter(1))
	        medians = newStates[minCostIndex]
	        

        return medians, totalCost