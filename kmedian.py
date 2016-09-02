#!/usr/bin/python

from TopologyGenerator import TopologyGenerator
from MovementDataParser import MovementDataParser
from mag import NetworkManager
from CacheManager import CacheManager
import sys

if __name__ == '__main__':
    userMovement = {
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

    tp = TopologyGenerator('/home/ubuntu/Downloads/APlocations_clean.csv')
    networkManager = NetworkManager()
    apsByBuildings, buildingNames = tp.getSample()
    linkage = {} #tp.computeLinkage(printDendogram = False)
    clusters = {} #tp.computeClusters()
    net, tree = networkManager.networkFromCLusters('test', clusters, linkage, len(buildingNames), apsByBuildings, buildingNames)
    
    print '*** Getting requests data'
    #movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/', '/data/movement.csv')
    #movementParser.getMovementInfo()

    cacheManager = CacheManager(tree)



    print cacheManager.computeKMedianCaches(k=2, userId=24, userMovement=userMovement)
    #networkManager.simulation(net)
    #CLI( net )
    #net.stop()

