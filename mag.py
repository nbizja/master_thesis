#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, RemoteController
from mininet.topolib import TreeNet
from mininet.net import Mininet
from mininet.log import output, warn
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from TopologyGenerator import TopologyGenerator
from MovementDataParser import MovementDataParser
from netaddr import IPAddress
from MobilitySwitch import MobilitySwitch
from MySwitch import MySwitch
from random import randint
import csv
import random

class NetworkManager():

    def __init__(self):
        self.apQueue = []
        self.accessPoints = {}
        self.apFreePort = {}
        self.gatewayIP = ''
        self.numberOfUsers = 50

    def createServer( self, net ):
        print '***  Creating main server on network root\n'
        host = net.addHost('h' + str(self.nextHostIndex))
        self.gatewayIP = str(IPAddress(167772160 + self.nextHostIndex))
        print self.gatewayIP
        rootSwitch = net.get('s1')
        net.addLink(host, rootSwitch)
        heth, seth = host.connectionsTo( rootSwitch )[ 0 ]
        self.gatewayMAC = host.MAC(heth)
        self.gatewayID = self.nextHostIndex
        host.cmd('python simple_server.py &')
        
        self.nextHostIndex += 1

    def addAccessPoints( self, net, mySwitch, depth, buildingName):

        #print "Adding access points " + buildingName
        accessPoints = []
        for ap in self.apsByBuildings[buildingName]:
            child = MySwitch(self.nextSwitchIndex, depth, APName=ap['APname'], isAP=True)
            accessPoints.append(child)
            s = net.addSwitch('s' + str(self.nextSwitchIndex))
            net.addLink( s , net.get('s%d' % mySwitch.getId()))

            self.accessPoints[ap['APname']] = self.nextSwitchIndex
            self.apFreePort[self.nextSwitchIndex] = 3
            self.nextSwitchIndex += 1
            print "S" + str(mySwitch.getId()) + " -> " + buildingName + "APS (" +ap['APname'] + " "+ str(child.getId()) + ""
            break

        self.currentBuilding += 1
        return accessPoints

    def createTree(self, net, span, depth, parentIndex=0):
        #print "Switch " + str(self.nextSwitchIndex) + " from parent " + str(parentIndex)
        mySwitch = MySwitch(self.nextSwitchIndex, depth=depth)
        s = net.addSwitch('s%d' % self.nextSwitchIndex)
        if parentIndex > 0:
            net.addLink(s, net.get('s%d' % parentIndex))           

        self.nextSwitchIndex += 1            
        #print "adding S%d" % mySwitch.getId()
        
        if depth >= self.maxDepth:
            mySwitch.setChildren(self.addAccessPoints(net, mySwitch, depth, self.buildingNames[self.currentBuilding]))
            return mySwitch
        else:
            for i in range(1, span + 1):  
                mySwitch.addChild(self.createTree(net, span, depth + 1, parentIndex=mySwitch.getId()))
                
            return mySwitch
    

    def addHosts( self, net, mySwitch ):
        self.hostSwitchMap = {}
        aps = mySwitch.getAccessPoints()
        k = 0
        for i in range(self.nextHostIndex, self.nextHostIndex + self.numberOfUsers + 1):
            sw = random.choice(aps)
            h = net.addHost('h%d' % i)
            s = net.get('s%d' % sw.getId())
            net.addLink(h, s)
            self.hostSwitchMap[i] = sw.getId()
            self.apFreePort[sw.getId()] += 1
            k = i
        self.nextHostIndex = k + 1


    def addCacheServers( self, net):
        for i in range(1, self.nextSwitchIndex):
            s = net.get('s%d' % i)
            cache = net.addHost('h%d' % i)
            net.addLink(cache, s)
            self.startSquid(cache, i)
            self.nextHostIndex = i + 1

    def startSquid( self, cache, cacheId):
        cache.cmd('sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3128 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('sudo iptables -t nat -A POSTROUTING -j MASQUERADE 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('/home/ubuntu/mag/squid/run-squid.sh ' + str(cacheId))

    def networkFromCLusters( self, clusters, linkage, size, apsByBuildings, buildingNames ):
        net = Mininet( controller=None, switch=MobilitySwitch, cleanup=True )
        ryu_controller = net.addController( 'c0', controller=RemoteController, ip="0.0.0.0", port=6633)
        #Controller is from http://sdnhub.org/releases/sdn-starter-kit-ryu/
        
        si = 2
        #mySwitch = MySwitch(1, depth=0)
        #net.addSwitch('s1')
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
        print '*** Adding cache servers\n'

        #self.addCacheServers(net)
        print '*** Creating gateway host and starting web server\n'
        self.createServer(net)
        #CLI(net)
        self.firstHostIndex = self.nextHostIndex
        self.addHosts( net, tree)

        print '*** Starting network\n'

        net.start()

        return net, tree

    def debug( self, tree, depth):
        if depth < 4:
            txt = "S%d has: " % tree.getId()
            for c in tree.getChildren():
                txt += " S%d" % c.getId()
            print txt
            for c in tree.getChildren():
                self.debug(c, depth + 1)

    def simulation( self, net ):
        print '*** Simulation started'

        limit = 500 
        requestCount = 0
        fieldnames = ['timestamp', 'hostIndex', 'AP']
        CLI(net)
        with open('/data/movement.csv', 'rb') as csvfile:
            requests = csv.DictReader(csvfile, fieldnames, delimiter=',')
            totalDelay = 0.0
            for req in requests:
                #WARNING: mapping multiple users into one.

                hostIndex = (int(req['hostIndex']) % self.numberOfUsers) + self.firstHostIndex
                #print hostIndex
                if req['AP'] in self.accessPoints:
                    hostCurrentlyOn = self.hostSwitchMap[hostIndex]
                    host = net.get('h%d' % hostIndex)

                    #If we need to move host
                    APIndex = self.accessPoints[req['AP']]
                    if hostCurrentlyOn != APIndex :
                        #print "host " + str(hostIndex) + " currently on %d" % hostCurrentlyOn
                        #self.debug(net, host)
                        #CLI(net)
                        oldSwitch = net.get('s%d' % hostCurrentlyOn)
                        newSwitch = net.get('s%d' % APIndex)
                        self.hostSwitchMap[hostIndex] = APIndex
                        self.moveHost(net, host, oldSwitch, newSwitch, newPort=self.apFreePort[APIndex] )
                        self.apFreePort[hostCurrentlyOn] -= 1
                        self.apFreePort[APIndex] += 1

                    for i in range(1, self.nextSwitchIndex):
                        net.get('s%d' % i).cmd('ovs-ofctl del-flows s%d dl_dst=%s' % (i, host.MAC()))
                        net.get('s%d' % i).cmd('sudo arp -d ' + host.IP())
                    
                    host.cmd('sudo arp -d ' + self.gatewayIP)
                    net.get('h%d' % self.gatewayID).cmd('sudo arp -d ' + host.IP())
                    #TODO: move host to target AP, request random content, measure delay
                    #print "Foo %d" % hostIndex
                    #if APIndex == 8:
                    #    CLI(net)
                    print "H%d  %s" % (hostIndex, host.MAC())
                    picture = str(randint(1,78))
                    delay = host.cmd("curl --no-keepalive -so /dev/null -w '%{time_total}\n' http://" + self.gatewayIP +'/helloworld') #+ picture + "/")
                    #CLI(net)
                    totalDelay += float(delay[2:])
                    print str(totalDelay)
                    #host.cmd('wget -qO- ' + self.gatewayIP + '/' + picture +' &> /dev/null')
                    #print "Bar"
                    requestCount = requestCount + 1
                #else:
                #    print "Request not in APS"
                if requestCount > limit:
                    break
            print "Delay sum: " + str(totalDelay)

        print requestCount

    def moveHost( self, net, host, oldSwitch, newSwitch, newPort=None ):
        "Move a host from old switch to new switch"

        #for sw in net.switches:
        #    print 'del-flows dl_dst=' + host.MAC(hintf)
        #    print sw.dpctl( 'del-flows dl_dst=' + host.MAC(hintf) )

        hintf, sintf = host.connectionsTo( oldSwitch )[ 0 ]
        oldSwitch.moveIntf( sintf, newSwitch, port=newPort, rename=False )
        #oldSwitch.cmd('sudo arp -d ' + host.IP())
        #oldSwitch.setARP(host.IP(), host.MAC(hintf))
        #CLI(net)
        #net.get('h%d' % self.gatewayID).setARP(host.IP(), host.MAC(hintf))
        return hintf, sintf
    
    def clearClientArps( self, net):
        for i in range(1, self.hostCount + 1):
            net.get('h' + str(i)).cmd('sudo arp -d ' + self.gatewayIP)

if __name__ == '__main__':
    setLogLevel( 'info' )
    tp = TopologyGenerator('/home/ubuntu/Downloads/APlocations_clean.csv')
    networkManager = NetworkManager()
    buildings, apsByBuildings, buildingNames = tp.computeBuildingAverages()
    linkage = tp.computeLinkage(printDendogram = False)
    clusters = tp.computeClusters()
    net, tree = networkManager.networkFromCLusters(clusters, linkage, len(buildings), apsByBuildings, buildingNames)
    
    print '*** Getting requests data'
    movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/', '/data/movement.csv')
    movementParser.getMovementInfo()
    networkManager.simulation(net)
    CLI( net )
    net.stop()
    #createNetwork(4,2) #2^4 hosts

