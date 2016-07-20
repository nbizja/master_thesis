import csv
# https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from numpy import array
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

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
        if (x/size) > 822000:
            print buildingName    
        buildingAverages[buildingName] = [x/size, y/size]
    else:
    	smth = 0
        #buildingAverages[buildingName] = [-1, -1]
    #print(buildingName + ': ' + str(buildingAverages[buildingName][0]) + ', ' + str(buildingAverages[buildingName][1]))



# generate two clusters: a with 100 points, b with 50:
#np.random.seed(4711)  # for repeatability of this tutorial
#a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100,])
#b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50,])
#X = np.concatenate((a, b),)
X = array( buildingAverages.values() )
#print X  # 150 samples with 2 dimensions
plt.scatter(X[:,0], X[:,1])
plt.show()

# generate the linkage matrix
Z = linkage(X, 'ward')

c, coph_dists = cophenet(Z, pdist(X))
print Z.shape

#idxs = [33, 68, 62]
#plt.figure()
#plt.scatter(X[:,0], X[:,1])  # plot all points
#plt.scatter(X[idxs,0], X[idxs,1], c='r')  # plot interesting points in red again
#plt.show()


# calculate full dendrogram
plt.figure(figsize=(25, 10))

plt.title('Hierarchical Clustering Dendrogram (truncated)')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    truncate_mode='lastp',  # show only the last p merged clusters
    p=12,  # show only the last p merged clusters
    show_leaf_counts=False,  # otherwise numbers in brackets are counts
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,  # to get a distribution impression in truncated branches
)
#plt.show()


