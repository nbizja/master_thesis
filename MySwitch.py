#!/usr/bin/python

class MySwitch():

    def __init__(self, index, depth, APName='', isAP=False):
        self.index = index
        self.children = []
        self.depth = depth
        self.isAP = isAP
        self.APName = APName
        self.hosts = []

    def getId(self):
        return self.index

    def getChildren(self):
        return self.children

    def getDepth(self):
        return self.depth

    def getAccessPoints(self):
        if self.isAP:
            return [self]
        
        if len(self.children) == 0:
            return []
        
        aps = []
    
        for child in self.getChildren():
            raw_input("ID: " + str(self.index))

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

