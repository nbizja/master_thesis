#!/usr/bin/python

from TopologyGenerator import TopologyGenerator
from MovementDataParser import MovementDataParser
from mag import NetworkManager
from CacheManager import CacheManager
import sys

if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    tp = TopologyGenerator('/home/ubuntu/Downloads/APlocations_clean.csv')
    networkManager = NetworkManager()
    buildings, apsByBuildings, buildingNames = tp.computeBuildingAverages()
    linkage = tp.computeLinkage(printDendogram = False)
    clusters = tp.computeClusters()
    net, tree = networkManager.networkFromCLusters(clusters, linkage, len(buildings), apsByBuildings, buildingNames)
    
    print '*** Getting requests data'
    #movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/', '/data/movement.csv')
    #movementParser.getMovementInfo()

    cacheManager = CacheManager(tree)


    userMovement = {
        1: {'AcadBldg10AP10': 10, 'AcadBldg19AP1': 10} #Result should be S!
    }
    cacheManager.computeKMedianCaches(k=1, userId=1, userMovement=userMovement)
    #networkManager.simulation(net)
    #CLI( net )
    #net.stop()

