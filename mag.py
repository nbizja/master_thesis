#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, RemoteController
from mininet.topolib import TreeNet
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import output, warn
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from TopologyGenerator import TopologyGenerator
from MovementDataParser import MovementDataParser
from CacheManager import CacheManager
from netaddr import IPAddress
from MobilitySwitch import MobilitySwitch
from MySwitch import MySwitch
from random import randint
from RyuRestClient import RyuRestClient
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import requests
import json
import time
import subprocess

class NetworkManager():

    def __init__(self, seed):
        self.apQueue = []
        self.accessPoints = {}
        self.apFreePort = {}
        self.gatewayIP = ''
        self.numberOfUsers = 50

        random.seed( seed )
        np.random.seed( seed )

    def createServer( self, net ):
        host = net.addHost('h' + str(self.nextHostIndex), mac='00:00:00:00:00:01')
        self.gatewayIP = str(IPAddress(167772160 + self.nextHostIndex))
        #print '***  Creating main server on network root %s' % self.gatewayIP
        
        rootSwitch = net.get('s1')
        net.addLink(host, rootSwitch, delay='50ms')#, delay="200ms")
        heth, seth = host.connectionsTo( rootSwitch )[ 0 ]
        self.gatewayMAC = '00:00:00:00:00:01'
        self.gatewayID = self.nextHostIndex
        host.cmd('python simple_server.py &')
        
        self.nextHostIndex += 1

    def addAccessPoints( self, net, mySwitch, depth, buildingName):
        accessPoints = []
        aps = self.apsByBuildings.values()

        for i in range(0,2):
            ap = aps[self.nextAPIndex][0]

            child = MySwitch(self.nextSwitchIndex, depth, APName=ap['APname'], isAP=True)
            accessPoints.append(child)
            s = net.addSwitch('s' + str(self.nextSwitchIndex))
            net.addLink( s , net.get('s%d' % mySwitch.getId()))

            self.accessPoints[ap['APname']] = self.nextSwitchIndex
            freePorts = [0 for i in range(50)]
            freePorts[0] = -1
            freePorts[1] = -1
            freePorts[2] = -1

            self.apFreePort[self.nextSwitchIndex] = freePorts
            self.nextSwitchIndex += 1
            self.nextAPIndex += 1
            #print "S" + str(mySwitch.getId()) + " -> " + buildingName + "APS (" +ap['APname'] + " "+ str(child.getId()) + ""
            if i == 1:
                break
            #if self.nextSwitchIndex >= self.maxAps:
            #    break

        self.currentBuilding += 1
        return accessPoints

    def createTree(self, net, span, depth, parentIndex=0):
        mySwitch = MySwitch(self.nextSwitchIndex, depth)
        s = net.addSwitch('s%d' % self.nextSwitchIndex)
        if parentIndex > 0:
            net.addLink(s, net.get('s%d' % parentIndex), delay='2ms')           

        self.nextSwitchIndex += 1            
        
        if depth >= self.maxDepth or self.nextSwitchIndex >= self.maxAps:
            mySwitch.setChildren(self.addAccessPoints(net, mySwitch, depth + 1, self.buildingNames[self.currentBuilding]))
            return mySwitch
        else:
            for i in range(1, span + 1):  
                mySwitch.addChild(self.createTree(net, span, depth + 1, parentIndex=mySwitch.getId()))
                
            return mySwitch
    

    def occupyFreePort(self, switchIndex, hostIndex):
        portIndex = 0
        for fp in self.apFreePort[switchIndex]:
            if fp == 0:
                self.apFreePort[switchIndex][portIndex] = hostIndex
                return portIndex + 1
            portIndex += 1

    def freeOccupiedPort(self, switchIndex, hostIndex):
        portIndex = 0
        for fp in self.apFreePort[switchIndex]:
            if fp == hostIndex:
                self.apFreePort[switchIndex][portIndex] = 0
                return portIndex + 1
            portIndex += 1

    def addHosts( self, net, mySwitch ):
        self.hostSwitchMap = {}
        i = self.nextHostIndex

        for ap in self.accessPoints.values():
            h = net.addHost('h%d' % i, ip='10.0.%d.1' % i, mac='00:00:00:00:00:%s' % ((hex(i))[-2:]))
            s = net.get('s%d' % ap)
            net.addLink(h, s)
            self.hostSwitchMap[ap] = i
            i += 1

        self.nextHostIndex = i


    def addCacheServers( self, net):
        #s = net.get('s1')
        #cache = net.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:02:00')
        #net.addLink(cache, s)
        #self.startSquid(cache, 2)

        #self.nextHostIndex = 3

        #i = 2
        self.cacheOnAp = {}
        #for ap in self.accessPoints.values():
        for i in range(1, self.nextSwitchIndex):
            print "Adding cache server to s%d" % i
            s = net.get('s%d' % i)
            cache = net.addHost('h%d' % (i + 1), ip='10.0.0.%d' % (i + 1), mac='00:00:00:00:%s:00' % ((hex(i + 1))[-2:]))
            
            net.addLink(cache, s)
            self.cacheOnAp[i] = i + 1
            self.startSquid(cache, i + 1)
            #cache.cmd('sudo arp -i h%d-eth0 10.0.0.1 00:00:00:00:00:01' % (i+1))
            self.nextHostIndex += 1
           
        #self.nextHostIndex = self.nextSwitchIndex + 1

    def startSquid( self, cache, cacheId):
        cache.cmd('sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3128 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('sudo iptables -t nat -A POSTROUTING -j MASQUERADE 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('/home/ubuntu/mag/squid/run-squid.sh ' + str(cacheId) + ' ' + self.experiment)

    def networkFromCLusters( self, expName, clusters, linkage, size, apsByBuildings, buildingNames ):
        net = Mininet( controller=None, switch=MobilitySwitch, link=TCLink, autoStaticArp = True )
        ryu_controller = net.addController( 'c0', controller=RemoteController, ip="0.0.0.0", port=6633)
        #Controller is from http://sdnhub.org/releases/sdn-starter-kit-ryu/
        self.experiment = expName
        self.nextHostIndex = 1
        self.nextSwitchIndex = 1
        self.currentBuilding = 0
        self.buildingNames = buildingNames
        self.apsByBuildings = apsByBuildings
        self.nextAPIndex = 0
        self.maxDepth = 1
        self.maxAps = size

        #buildingIndex = 0
        #links = [linkage[len(linkage) - 1,0], linkage[len(linkage) - 1,1]]
        #print '*** Creating topology\n'
        tree = self.createTree(net, 2, 0)

        #print '*** Creating gateway host and starting web server\n'
        self.createServer(net)

        #print '*** Adding cache servers\n'
        self.addCacheServers(net)

        #print '*** Adding hosts from h%d to h%d' % (self.nextHostIndex, self.nextHostIndex + self.numberOfUsers)
        self.firstHostIndex = self.nextHostIndex
        self.addHosts( net, tree)

        #print '*** Starting network\n'        
        net.start()

        #print "*** Adding static flows"
        #self.setupStaticFlows(net)

        return net, tree

    def debug( self, tree, depth):
        if depth < 4:
            txt = "S%d has: " % tree.getId()
            for c in tree.getChildren():
                txt += " S%d" % c.getId()
            print txt
            for c in tree.getChildren():
                self.debug(c, depth + 1)

    def setupStaticFlows(self, net):
        #for i in range(2, self.nextSwitchIndex):
        #    net.get('s%d' % i).cmd('sudo arp -i s%d-eth1 -s %s %s ' % (i, self.gatewayIP, self.gatewayMAC))
        #    net.get('s%d' % i).cmd('ovs-ofctl add-flow s%d priority=100,idle_timeout=20,dl_type=0x800,nw_dst=%s,action=output:1' % (i, self.gatewayIP))
        
        #net.get('s1').cmd('ovs-ofctl add-flow s1 priority=100,idle_timeout=20,in_port=1,nw_dst=%s,action=output:3' % self.gatewayIP)
        #net.get('s1').cmd('ovs-ofctl add-flow s1 priority=100,idle_timeout=20,in_port=2,nw_dst=%s,action=output:3' % self.gatewayIP)

        for j in range(2, self.nextHostIndex):
            net.get('h%d' % j).cmd('sudo arp -i h%d-eth0 -s %s %s' % (j, self.gatewayIP, self.gatewayMAC))

    def cacheAllTheThings(self, tree):
        apsIds = list(map((lambda ap: ap.getId()), tree.getAccessPoints()))
        ryuClient = RyuRestClient('127.0.0.1', '6633', apsIds)
        ryuClient.addCacheRoute(net.get('h70'), net.get('h3'))
        print "Cached all the things"

    def makeRequest(self, host, item, cacheId=0):
        cacheStr = ''
        if cacheId != 0:
            cacheStr = '-x http://10.0.0.' + str(cacheId) + ':8080'
        #time_starttransfer
        cmd = "curl --connect-timeout 3 -so /dev/null -w '%{http_code},%{time_starttransfer}' " + cacheStr + " http://" + self.gatewayIP + "/" + str(item)

        return host.cmd(cmd)

    def simulation( self, net, tree, limit ):
        #print '*** Simulation started'
        #bwmTxt = 's1'
        #for i in range(2, self.nextSwitchIndex):
        #    bwmTxt = ',s' + str(i)
        #subprocess.call('bwm-ng --output csv --unit bytes -T sum -F /home/ubuntu/mag/experiments/'+expName+'.csv --interfaces %%lo,eth0,docker0,ovs-system,'+bwmTxt+' --sumhidden 0 --daemon 1')

        #self.cacheAllTheThings(tree)
        cacheManager = CacheManager(tree)

        requestCount = 0
        fieldnames = ['timestamp', 'hostIndex', 'AP']

        content = range(1, 4001)

        users = range(1,51)
        userContent = []
        for u in users:
            userContent.append(random.sample(range(1, 4001), 200))

        paretoDist = np.random.pareto(0.5, limit * 10) + 1
        #contentChoice = np.around(np.array(paretoDist[paretoDist < 200][:(limit + 1)]), 0).astype(int)
        contentChoice = random.sample(range(1, 4001), 100)
        with open('/data/example.csv', 'rb') as csvfile:
            userRequests = csv.DictReader(csvfile, fieldnames, delimiter=',')
            totalDelay = 0.0
            failedRequests = 0

            #medians = cacheManager.computeKMedianCaches(k=2, userId=24)#CacheManager.ALL_USERS)
            #print "user requests"
            #print userRequests

            hostCache = {}

            #for api in self.accessPoints.values():
            #    distances = []
            #    for median in medians[24]:
            #        distances.append(cacheManager.distance(tree, api, median))
            #    mi, minDist = min(enumerate(distances), key=itemgetter(1))
            #    hostCache[api] = medians[24][mi] #host to cache connection


            hostCache['SocBldg2AP1'] = 3
            hostCache['SocBldg3AP1'] = 3
            hostCache['AcadBldg22AP2'] = 5
            hostCache['LibBldg4AP3'] = 5
            targetDelayList = []
            targetDelayAvg = []
            targetDelay = 0.0

            targetReqCount = 1


            #CLI(net)
            #print self.accessPoints
            #print cacheIds.keys()
            for req in userRequests:
                #WARNING: mapping multiple users into one.

                #hostIndex = (int(req['hostIndex']) % self.numberOfUsers) + self.firstHostIndex
                #print hostIndex
                #hi = (int(req['hostIndex']) % 50) + 1
                hi = int(req['hostIndex'])

                if req['AP'] in self.accessPoints and hi == 24:
                    APIndex = self.accessPoints[req['AP']]

                    host = net.get('h%d' % self.hostSwitchMap[APIndex])

                    cacheId = hostCache[req['AP']] #self.cacheOnAp[int(medians[hi])]
                    picture = random.sample(range(1, 201), 1)[0] #userContent[hi - 1][contentChoice[requestCount]]

                    #print str(requestCount) + "H%d requests img%d from %s (H%d) via h%d" % (hi, picture, req['AP'], self.hostSwitchMap[APIndex], cacheId)
               
                    result = self.makeRequest(host, picture, cacheId = cacheId ) #caching on the edge
                    code = result[0:3]
                    delay = result[4:9]
                    #print "Delay " + str(delay)
                    if self.hostSwitchMap[APIndex] == 11:
                        targetDelay += float(delay)
                        targetDelayList.append(float(delay))
                        targetDelayAvg.append(targetDelay/float(targetReqCount))
                        targetReqCount += 1




                    if int(code) != 200:
                        failedRequests += 1
                    else:
                        totalDelay += float(delay)
   
                    requestCount += 1
                    if requestCount > 10 and requestCount == failedRequests:
                        print "fail!"
                        break

                    if requestCount > 1500:
                        break
            #print "Total requests: %d  Failed requests: %d "  % (requestCount - 1, failedRequests)
            #print "Delay sum: " + str(totalDelay)

            #print "\nTarget delay list:"
            #print targetDelayList

            #print "\nTarget avg delay:"
            #print targetDelayAvg

            #print "\nTotal delay:"
            return targetDelayList, totalDelay

            #print "\nTotal avg delay:"
            #print targetDelay/float(targetReqCount)

            #plt.plot(range(1,len(targetDelayAvg) + 1), targetDelayAvg, 'r--')
            #plt.axis(range(1, 20, 21))
            #plt.show()


    def moveHost( self, net, host, hostIndex, oldSwitch, newSwitch, newPort=None ):
        "Move a host from old switch to new switch"

        hintf, sintf = host.connectionsTo( oldSwitch )[ 0 ]
        oldSwitch.moveIntf( sintf, newSwitch, port=newPort, rename=False )
        #oldSwitch.cmd('sudo arp -d ' + host.IP())

        return host

if __name__ == '__main__':
    setLogLevel( 'info' )
    expName = raw_input("Enter experiment name: ")
    sumDelay = [0.0 for k in range(0,160)]
    delays = []
    totalDelay = []

    for i in range(0, 10):
        print i
        i = 3
        tp = TopologyGenerator('/home/ubuntu/Downloads/APlocations_clean.csv')
        networkManager = NetworkManager((i + 1) * 123)
        apsByBuildings, buildingNames = tp.getSample()
        linkage = {}#tp.computeLinkage(printDendogram = True) #
        clusters = {}#tp.computeClusters() #{}
        net, tree = networkManager.networkFromCLusters(expName, clusters, linkage, 30, apsByBuildings, buildingNames)
        
        #print '*** Getting requests data'
        #movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/', '/data/movement.csv')
        #movementParser.getMovementInfo()
        CLI( net )
        delay, td = networkManager.simulation(net, tree, 2000)
        delays.append(delay)
        totalDelay.append(td)
        sumDelay = [x + y for x, y in zip(sumDelay, delay)]
        CLI( net )
        net.stop()
        break
      #createNetwork(4,2) #2^4 hosts
    avgDelay = [x / float(len(sumDelay)) for x in sumDelay]

    print "All delays"
    print delays

    print "Avg Delay"
    print avgDelay

    print "Total delays"
    print totalDelay



