#!/usr/bin/python

from TopologyGenerator import TopologyGenerator
from MovementDataParser import MovementDataParser
from mag import NetworkManager
from CacheManager import CacheManager

if __name__ == '__main__':
    tp = TopologyGenerator('/home/ubuntu/Downloads/APlocations_clean.csv')
    networkManager = NetworkManager()
    buildings, apsByBuildings, buildingNames = tp.computeBuildingAverages()
    linkage = tp.computeLinkage(printDendogram = False)
    clusters = tp.computeClusters()
    net, tree = networkManager.networkFromCLusters(clusters, linkage, len(buildings), apsByBuildings, buildingNames)
    
    print '*** Getting requests data'
    movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/', '/data/movement.csv')
    movementParser.getMovementInfo()

    cacheManager = CacheManager(tree)
    cacheManager.computeKMedianCaches(k=1, userId=1)
    #networkManager.simulation(net)
    #CLI( net )
    #net.stop()