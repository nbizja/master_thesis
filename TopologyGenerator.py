#!/usr/bin/python
import csv
# https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
#from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from numpy import array
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from subset import *

class TopologyGenerator():
    def __init__(self, path):
        self.path = path
        global subset
        self.subset = subset

    def getSample(self):
        userMovement2 = {
            24: {'SocBldg2AP1': 3, 'SocBldg2AP3': 1, 'AcadBldg22AP2': 4, 'LibBldg4AP3': 2,
            'ResBldg62AP4': 9, 'AdmBldg12AP1': 1, 'SocBldg1AP5': 6, 'AcadBldg21AP2': 2,
            'AcadBldg8AP1': 1, 'LibBldg2AP20': 2, 'SocBldg1AP1': 11, 'LibBldg2AP9': 8,
            'SocBldg1AP3': 1, 'SocBldg1AP2': 8, 'LibBldg2AP4': 1, 'LibBldg4AP2': 3,
            'AcadBldg19AP2': 3, 'SocBldg4AP21': 1, 'AcadBldg19AP5': 2, 'ResBldg93AP1': 2,
            'ResBldg25AP2': 6, 'LibBldg1AP5': 3, 'LibBldg1AP4': 1, 'LibBldg1AP7': 1,
            'LibBldg1AP8': 2, 'AcadBldg15AP5': 1, 'AcadBldg4AP4': 2, 'AcadBldg19AP1': 2,
            'LibBldg2AP1': 1, 'LibBldg4AP5': 3, 'LibBldg2AP14': 15, 'ResBldg84AP3': 2,
            'LibBldg2AP3': 1, 'SocBldg3AP2': 1, 'ResBldg80AP4': 22, 'LibBldg2AP21': 7, 
            'ResBldg15AP1': 2, 'SocBldg4AP1': 3, 'ResBldg80AP3': 61, 'ResBldg33AP2': 268, 
            'ResBldg33AP1': 252, 'ResBldg25AP1': 19, 'SocBldg11AP6': 15, 'SocBldg11AP5': 22, 
            'SocBldg11AP4': 1, 'SocBldg11AP3': 2, 'SocBldg11AP2': 1, 'ResBldg36AP2': 1, 
            'AcadBldg34AP4': 18, 'SocBldg4AP10': 5, 'SocBldg4AP13': 28, 'ResBldg36AP1': 3, 
            'ResBldg39AP1': 1, 'AcadBldg34AP2': 3, 'ResBldg66AP1': 3, 'ResBldg66AP2': 2, 
            'AdmBldg22AP1': 19, 'AcadBldg30AP3': 1, 'ResBldg82AP3': 3, 'AcadBldg8AP4': 14, 
            'LibBldg2AP19': 8, 'AcadBldg30AP1': 10, 'LibBldg2AP17': 13, 'LibBldg1AP17': 2, 
            'LibBldg2AP13': 2, 'LibBldg2AP10': 3, 'LibBldg2AP11': 3} 
        }
        userMovement = {
            24: {'SocBldg2AP1': 10, 'SocBldg3AP2': 8, 'AcadBldg22AP2': 1, 'LibBldg4AP3': 4}
        }
        apsByBuildings = {}
        buildingNames = []

        for ap in userMovement[24]:
                apPosition = ap.find('AP')
                buildingName = ap[0:apPosition]
                if buildingName in apsByBuildings:
                    apsByBuildings[buildingName].append({'APname': ap})
                else:
                    buildingNames.append(buildingName)
                    apsByBuildings[buildingName] = [{'APname': ap}]

        return apsByBuildings, buildingNames

    def computeBuildingAverages( self ):

        np.set_printoptions(suppress=True)
        apsByBuildings = {}
        buildingNames = []
        fieldnames = ['APname', 'x', 'y', 'floor']
        with open('/home/ubuntu/Downloads/APlocations_clean.csv', 'rb') as csvfile:
        #AP, x coordinate (-1 = unknown), y coordinate (-1 = unknown), z coordinate (floor, 99 = unknown)

            reader = csv.DictReader(csvfile, fieldnames, delimiter=',')
            for row in reader:
                apPosition = row['APname'].find('AP')
                buildingName = row['APname'][0:apPosition]
                #if buildingName in subset:
                if buildingName in apsByBuildings:
                    apsByBuildings[buildingName].append(row)
                else:
                    buildingNames.append(buildingName)
                    apsByBuildings[buildingName] = [row]



        buildingAverages = {}
        buildingLimits = 5
        bi = 1
        for buildingName, aps in apsByBuildings.iteritems():
            x = 0.0
            y = 0.0
            size = 0.0
            for ap in aps:
                if ap['x'] != '-1':
                    x += float(ap['x'])
                    y += float(ap['y'])
                    size = size + 1
                break #TESTING

            if size > 0.0 and buildingName in subset:     
                buildingAverages[buildingName] = [x/size, y/size]
            
            #if bi >= buildingLimits: #TESTING
            #    break
            bi = bi + 1 #TESTING

        self.buildingAverages = buildingAverages
        return self.buildingAverages, apsByBuildings, buildingNames

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


  











