import csv

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
    size = 0
    for ap in aps:
        if ap['x'] != '-1':
            x += float(ap['x'])
            y += float(ap['y'])
            size = size + 1

    if size > 0:
        if (x/size) < 780000:
            print buildingName     
        buildingAverages[buildingName] = [x/size, y/size]
    else:
        #buildingAverages[buildingName] = [-1, -1]
    #print(buildingName + ': ' + str(buildingAverages[buildingName][0]) + ', ' + str(buildingAverages[buildingName][1]))






    
