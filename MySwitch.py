#!/usr/bin/python

class MySwitch():

    def __init__(self, id, depth, APName='', children=[], isAP=False):
        self.id = id
        self.children = children
        self.depth = depth
        self.isAP = isAP
        self.APName = APName
        self.hosts = []

    def getId(self):
        return self.id

    def getChildren(self):
        return self.children

    def getDepth(self):
        return self.depth

    def getAccessPoints(self):
        if self.isAP:
            return [self]
        
        if not self.children:
            return []
        
        aps = []
        for child in self.children:
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
        self.children = children

    def setIsAP(self, isAP):
        self.isAP = isAP

    def findPathToAP(self, APName):
        if self.APName == APName:
            return [self]
        if self.isAP:
            return []
        
        path = []
        for child in self.children:
            path += child.findPathToAP(APName)
        return path

