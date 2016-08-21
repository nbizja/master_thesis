#!/usr/bin/python

import csv
from os import listdir
from os.path import isfile
from subset import *
import pickle

class MovementDataParser():

    def __init__(self, path, resultPath):
        self.path = path
        self.sortedRequestsPath = resultPath
        global subset
        self.subset = subset

    def getMovementInfo( self , getSubset=False):
        if isfile(self.sortedRequestsPath) and not getSubset:
            return True

        start = 986990247
        end = 1047790796
        requests = []
        apsByBuildings = {}
        buildingNames = []
        fieldnames = ['timestamp', 'AP']
        hostIndex = 1
        usersByBuildings = {}
        for f in listdir(self.path):
            with open(self.path + f, 'rb') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames, delimiter='\t')
                for row in reader:
                    if row['AP'] != 'OFF':
                        requests.append([row['timestamp'], str(hostIndex), row['AP']])
                        apPosition = row['AP'].find('AP')
                        buildingName = row['AP'][0:apPosition]
                        if buildingName in self.subset:
                            if buildingName in usersByBuildings:
                                if hostIndex not in usersByBuildings[buildingName]:
                                    usersByBuildings[buildingName].append(hostIndex)
                            else:
                                usersByBuildings[buildingName] = [hostIndex]

            hostIndex = hostIndex + 1

        maxLengths = []

        if getSubset:
            for bld, users in usersByBuildings.iteritems():
                print len(users)
                if len(users) > 500:
                    maxLengths.append(bld)

            for bld in maxLengths[-30:]:
                print bld
            return True

        sortedRequests = sorted(requests,key=lambda l:l[0])
        
        with open(self.sortedRequestsPath, 'wb') as f:
            for s in sortedRequests:
                f.write(','.join(s) + '\n')
        
        return sortedRequests

    def saveResults( self, requests ):
        #save computation
        test = 0
    

if __name__ == '__main__':
    movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/' , '/data/movement.csv')
    movementParser.getMovementInfo()
