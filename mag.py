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
from netaddr import IPAddress
from MobilitySwitch import MobilitySwitch
from MySwitch import MySwitch
from random import randint
from RyuRestClient import RyuRestClient
import csv
import random
import requests
import json
import time

class NetworkManager():

    def __init__(self):
        self.apQueue = []
        self.accessPoints = {}
        self.apFreePort = {}
        self.gatewayIP = ''
        self.numberOfUsers = 50

        random.seed( 10 )

    def createServer( self, net ):
        host = net.addHost('h' + str(self.nextHostIndex), mac='00:00:00:00:00:01')
        self.gatewayIP = str(IPAddress(167772160 + self.nextHostIndex))
        print '***  Creating main server on network root %s' % self.gatewayIP
        
        rootSwitch = net.get('s1')
        net.addLink(host, rootSwitch)#, delay="200ms")
        heth, seth = host.connectionsTo( rootSwitch )[ 0 ]
        self.gatewayMAC = '00:00:00:00:00:01'
        self.gatewayID = self.nextHostIndex
        host.cmd('python simple_server.py &')
        
        self.nextHostIndex += 1

    def addAccessPoints( self, net, mySwitch, depth, buildingName):
        accessPoints = []
        for ap in self.apsByBuildings[buildingName]:
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
            print "S" + str(mySwitch.getId()) + " -> " + buildingName + "APS (" +ap['APname'] + " "+ str(child.getId()) + ""
            break

        self.currentBuilding += 1
        return accessPoints

    def createTree(self, net, span, depth, parentIndex=0):
        mySwitch = MySwitch(self.nextSwitchIndex, depth=depth)
        s = net.addSwitch('s%d' % self.nextSwitchIndex)
        if parentIndex > 0:
            net.addLink(s, net.get('s%d' % parentIndex))           

        self.nextSwitchIndex += 1            
        
        if depth >= self.maxDepth:
            mySwitch.setChildren(self.addAccessPoints(net, mySwitch, depth, self.buildingNames[self.currentBuilding]))
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
        aps = mySwitch.getAccessPoints()
        k = 0
        for i in range(self.nextHostIndex, self.nextHostIndex + self.numberOfUsers + 1):
            sw = random.choice(aps)
            h = net.addHost('h%d' % i, ip='10.0.%d.1' % i, mac='00:00:00:00:00:%s' % ((hex(i))[-2:]))
            s = net.get('s%d' % sw.getId())
            net.addLink(h, s)
            self.hostSwitchMap[i] = sw.getId()
            self.occupyFreePort(sw.getId(), i)
            k = i
        self.nextHostIndex = k + 1


    def addCacheServers( self, net):
        for i in range(1, self.nextSwitchIndex):
            s = net.get('s%d' % i)
            cache = net.addHost('h%d' % (i + 1), ip='10.0.0.%d' % (i + 1), mac='00:00:00:00:%s:00' % ((hex(i + 1))[-2:]))
            net.addLink(cache, s)
            self.startSquid(cache, i + 1)
        
        self.nextHostIndex = self.nextSwitchIndex + 1

    def startSquid( self, cache, cacheId):
        cache.cmd('sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3128 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('sudo iptables -t nat -A POSTROUTING -j MASQUERADE 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('/home/ubuntu/mag/squid/run-squid.sh ' + str(cacheId))

    def networkFromCLusters( self, clusters, linkage, size, apsByBuildings, buildingNames ):
        net = Mininet( controller=None, switch=MobilitySwitch )
        ryu_controller = net.addController( 'c0', controller=RemoteController, ip="0.0.0.0", port=6633)
        #Controller is from http://sdnhub.org/releases/sdn-starter-kit-ryu/

        self.nextHostIndex = 1
        self.nextSwitchIndex = 1
        self.currentBuilding = 0
        self.buildingNames = buildingNames
        self.apsByBuildings = apsByBuildings
        self.maxDepth = 3

        #buildingIndex = 0
        #links = [linkage[len(linkage) - 1,0], linkage[len(linkage) - 1,1]]
        print '*** Creating topology\n'
        tree = self.createTree(net, 2, 0)

        print '*** Creating gateway host and starting web server\n'
        self.createServer(net)

        print '*** Adding cache servers\n'
        self.addCacheServers(net)

        print '*** Adding hosts from h%d to h%d' % (self.nextHostIndex, self.nextHostIndex + self.numberOfUsers)
        self.firstHostIndex = self.nextHostIndex
        self.addHosts( net, tree)

        print '*** Starting network\n'        
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

    def makeRequest(self, host, item, cacheIp=''):
        cacheStr = ''
        if cacheIp != '':
            cacheStr = '-p http://' + cacheIp + ':8080'
        return host.cmd("curl --connect-timeout 2 -so /dev/null -w '%{http_code},%{time_total}' " + cacheStr + " http://" + self.gatewayIP + "/helloworld")# + picture)

    def simulation( self, net, tree ):
        print '*** Simulation started'

        #self.cacheAllTheThings(tree)
        limit = 50 
        requestCount = 0
        fieldnames = ['timestamp', 'hostIndex', 'AP']

        with open('/data/movement.csv', 'rb') as csvfile:
            userRequests = csv.DictReader(csvfile, fieldnames, delimiter=',')
            totalDelay = 0.0
            failedRequests = 0
            for req in userRequests:
                #WARNING: mapping multiple users into one.

                hostIndex = (int(req['hostIndex']) % self.numberOfUsers) + self.firstHostIndex
                #print hostIndex
                if req['AP'] in self.accessPoints:
                    hostCurrentlyOn = self.hostSwitchMap[hostIndex]
                    host = net.get('h%d' % hostIndex)

                    #If we need to move host
                    APIndex = self.accessPoints[req['AP']]
                    if hostCurrentlyOn != APIndex:
                        print "h%d is moving from s%d to s%d" % (hostIndex, hostCurrentlyOn, APIndex)
                        oldSwitch = net.get('s%d' % hostCurrentlyOn)
                        newSwitch = net.get('s%d' % APIndex)
                        self.hostSwitchMap[hostIndex] = APIndex
                        self.freeOccupiedPort(APIndex, hostIndex)
                        newPort = self.occupyFreePort(APIndex, hostIndex)
                        print newPort
                        host = self.moveHost(net, host, hostIndex, oldSwitch, newSwitch, newPort=newPort )
                        CLI(net)

                    print "H%d  %s" % (hostIndex, host.MAC())

                    picture = str(randint(1,78))
                    #result = host.cmd("curl --connect-timeout 2 -so /dev/null -w '%{http_code},%{time_total}' http://" + self.gatewayIP + "/helloworld")# + picture)
                    result = self.makeRequest(host, picture)
                    code, delay = result.split(',')

                    if int(code) != 200:
                        failedRequests += 1
                    else:
                        totalDelay += float(delay[2:])
   
                    requestCount = requestCount + 1
                    if requestCount > 10 and requestCount == failedRequests:
                        break

                    if requestCount > limit:
                        break
            print "Total requests: %d  Failed requests: %d "  % (requestCount, failedRequests)
            print "Delay sum: " + str(totalDelay)

        print requestCount

    def moveHost( self, net, host, hostIndex, oldSwitch, newSwitch, newPort=None ):
        "Move a host from old switch to new switch"

        hintf, sintf = host.connectionsTo( oldSwitch )[ 0 ]
        oldSwitch.moveIntf( sintf, newSwitch, port=newPort, rename=False )
        #oldSwitch.cmd('sudo arp -d ' + host.IP())

        return host

if __name__ == '__main__':
    setLogLevel( 'info' )
    tp = TopologyGenerator('/home/ubuntu/Downloads/APlocations_clean.csv')
    networkManager = NetworkManager()
    buildings, apsByBuildings, buildingNames = tp.computeBuildingAverages()
    linkage = tp.computeLinkage(printDendogram = False)
    clusters = tp.computeClusters()
    net, tree = networkManager.networkFromCLusters(clusters, linkage, len(buildings), apsByBuildings, buildingNames)
    
    print '*** Getting requests data'
    #movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/', '/data/movement.csv')
    #movementParser.getMovementInfo()
    networkManager.simulation(net, tree)
    CLI( net )
    net.stop()
    #createNetwork(4,2) #2^4 hosts

