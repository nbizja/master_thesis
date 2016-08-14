import csv
from os import listdir
from os.path import isfile, join

class MovementDataParser():

    def __init__(self, path):
        self.path = path

    def getMovementInfo( self ):

        start = 986990247
        end = 1047790796
        requests = {}
        apsByBuildings = {}
        buildingNames = []
        fieldnames = ['timestamp', 'AP']
        for f in listdir(self.path):
            with open(self.path + f, 'rb') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames, delimiter='\t')
                for row in reader:
                    ts = int(row['timestamp'])
                    if ts in requests:
                        requests[ts].append(row['AP'])
                    else:
                        requests[ts] = [row['AP']]
            #break #TESTING

        return requests

    def saveResults( self, requests ):
        #save computation
    

if __name__ == '__main__':
    movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/')
    movementParser.computeBuildingAverages()
