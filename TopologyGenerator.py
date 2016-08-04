import csv
# https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from numpy import array
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

class TopologyGenerator():
	def __init__(self, path):
		self.path = path

	def computeBuildingAverages( self ):

		np.set_printoptions(suppress=True)
		apsByBuildings = {}
		fieldnames = ['APname', 'x', 'y', 'floor']
		with open('/home/ubuntu/Downloads/APlocations_clean.csv', 'rb') as csvfile:
		#AP, x coordinate (-1 = unknown), y coordinate (-1 = unknown), z coordinate (floor, 99 = unknown)

		    reader = csv.DictReader(csvfile, fieldnames, delimiter=',')
		    for row in reader:
		        apPosition = row['APname'].find('AP')
		        buildingName = row['APname'][0:apPosition]
		        if buildingName in apsByBuildings:
		            apsByBuildings[buildingName].append(row)
		        else:
		            apsByBuildings[buildingName] = [row]



		buildingAverages = {}

		for buildingName, aps in apsByBuildings.iteritems():
		    x = 0.0
		    y = 0.0
		    size = 0.0
		    for ap in aps:
		        if ap['x'] != '-1':
		            x += float(ap['x'])
		            y += float(ap['y'])
		            size = size + 1

		    if size > 0.0:     
		        buildingAverages[buildingName] = [x/size, y/size]

		self.buildingAverages = buildingAverages
		return self.buildingAverages

	def computeLinkage( self, printDendogram = False ):
		# generate two clusters: a with 100 points, b with 50:
		#np.random.seed(4711)  # for repeatability of this tutorial
		#a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100,])
		#b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50,])
		#X = np.concatenate((a, b),)
		self.X = array( self.buildingAverages.values() )
		#print X  # 150 samples with 2 dimensions
		#plt.scatter(X[:,0], X[:,1])
		#plt.show()

		# generate the linkage matrix
		self.Z = linkage(self.X, 'ward')

		c, coph_dists = cophenet(self.Z, pdist(self.X))

		if (printDendogram):
			# calculate full dendrogram
			plt.figure(figsize=(25, 10))

			plt.title('Hierarchical Clustering Dendrogram (truncated)')
			plt.xlabel('sample index')
			plt.ylabel('distance')
			dendrogram(
			    self.Z,
			    truncate_mode='lastp',  # show only the last p merged clusters
			    p=20,  # show only the last p merged clusters
			    show_leaf_counts=False,  # otherwise numbers in brackets are counts
			    leaf_rotation=90.,
			    leaf_font_size=12.,
			    show_contracted=True,  # to get a distribution impression in truncated branches
			)
			plt.show()

		return self.Z

	def computeClusters( self ):
		clusters = []
		Xsize = len(self.X)
		i = 0

		Y = np.empty((Xsize, 100))
		Y.fill(-1)

		for link in self.Z:
			#print str(i) + ', ' + str(link[0]) + ', ' + str(link[1]) + ', ' + str(link[2]) + ', ' + str(link[3])

			if link[0] > Xsize:
				indices = Y[link[0]]
			else:
				indices = np.array([link[0]])

			if link[1] > Xsize:
				for val in Y[link[1]]:
					if val != -1:
						indices = np.concatenate(([val], indices))
			else:
				indices = np.concatenate(([link[1]], indices))

			if len(indices) < 50:
				indices = np.pad(indices, (0, 100-len(indices)), 'constant', constant_values=(-1))

			Y = np.vstack((Y,indices[0:100]))
			i = i + 1

		self.clusters = Y

		return self.clusters


#Y holds indices of buildings.
#last row holds all indices (aka root switch)


  











