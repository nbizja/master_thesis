class CacheManager():
	def __init__(self, network):
		self.network = network

	def processMovementPattern(self, movementData):
		userMovement = {}
		fieldnames = ['timestamp', 'hostIndex', 'AP']
		for row in movementData:
			hi = int(row['hostIndex'])
			if hi not in userMovement:
				userMovement[hi] = {row['AP']: 1}
			else:
				if row['AP'] not in userMovement[hi]:
					userMovement[hi][row['AP']] = 1
				else:
					userMovement[hi][row['AP']] +=1


	def computeMedian(self, userMovement):
		#Compute lowest common ancestor


	def lowestCommonAncestor(self, accessPoints):
		paths = []
		for ap in accessPoints:
			paths.append(list(reverse(self.network.findPath(ap))))

		for depth in range(0, len(paths[0])):
			lcaCandidate = paths[0][depth]
			for path in paths:
				if path[depth].getId() != lcaCandidate.getId():
					return lcaCandidate, depth
		return paths[0][0], 0


