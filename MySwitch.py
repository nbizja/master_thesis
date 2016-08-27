#!/usr/bin/python

class MySwitch():

    def __init__(self, index, depth, APName='', isAP=False):
        self.index = index
        self.children = []
        self.depth = depth
        self.isAP = isAP
        self.APName = APName
        self.hosts = []

        self.numOfReq = []
        self.reqDepth = []


    def getId(self):
        return self.index

    def getChildren(self):
        return self.children

    def getDepth(self):
        return self.depth

    def getNumOfReq(self):
        return self.numOfReq

    def setNumOfReq(self, numOfReq):
        self.numOfReq = numOfReq

    def getReqDepth(self):
        return self.reqDepth

    def setReqDepth(self, reqDepth):
        self.reqDepth = reqDepth

    def getAccessPoints(self):
        if self.isAP:
            return [self]
        
        if len(self.children) == 0:
            return []
        
        aps = []
    
        for child in self.getChildren():
            aps += child.getAccessPoints()

        return aps

    def isAP(self):
        return isAP

    def setAPName(self, name):
        self.APName = name

    def getAPName(self):
        return self.APName

    def addChild(self, child):
        self.children.append(child)

    def setChildren(self, children):
        txt = "MySwitch %d has children: " % self.index
        for child in children:
            txt += str(child.getId()) + ", "

        self.children = children

    def setIsAP(self, isAP):
        self.isAP = isAP


    #### Algorithm
    def moveUp(self, path):
        upperHop = self
        for hop in path:
            if self.id == hop.getId():
                return upperHop
            upperHop = hop

        return upperHop


    def merge(self, path):
        for i in range(0, len(path)):
            if len(path[i].getNumOfReq) > 0:
                path[i].mergeRequests(self.numOfReq, reqDepth)
                break
        return path

    def mergeMedian(self, median):
        "Adds number of request and request depths to this node"
        self.numOfReq += median.getNumOfReq()
        self.reqDepth += median.getReqDepth()

    