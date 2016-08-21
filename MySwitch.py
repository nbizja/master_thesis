#!/usr/bin/python

class MySwitch():

    def __init__(self, id, children=[], isAP=False):
        self.id = id
        self.children = children
        self.isAP = isAP
        self.hosts = []

    def getId(self):
        return self.id

    def getChildren(self):
        return self.children

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

    def addChild(self, child):
        self.children.append(child)

    def setChildren(self, children):
        self.children = children

    def setIsAP(self, isAP):
        self.isAP = isAP
