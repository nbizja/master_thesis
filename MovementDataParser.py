#!/usr/bin/python

import csv
from os import listdir
from os.path import isfile
import pickle

class MovementDataParser():

    def __init__(self, path, resultPath):
        self.path = path
        self.sortedRequestsPath = resultPath

    def getMovementInfo( self ):
        if isfile(self.sortedRequestsPath):
            return True

        start = 986990247
        end = 1047790796
        requests = []
        apsByBuildings = {}
        buildingNames = []
        fieldnames = ['timestamp', 'AP']
        hostIndex = 1
        for f in listdir(self.path):
            with open(self.path + f, 'rb') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames, delimiter='\t')
                for row in reader:
                    if row['AP'] != 'OFF':
                        requests.append([row['timestamp'], str(hostIndex), row['AP']])
            hostIndex = hostIndex + 1

        sortedRequests = sorted(requests,key=lambda l:l[0])

        with open(self.sortedRequestsPath, 'wb') as f:
            for s in sortedRequests:
                f.write(','.join(s) + '\n')
        
        return sortedRequests

    def saveResults( self, requests ):
        #save computation
        test = 0
    

if __name__ == '__main__':
    movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/')
    movementParser.computeBuildingAverages()
