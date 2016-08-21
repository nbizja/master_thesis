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
import csv
import random

class NetworkManager():

    def __init__(self):
        self.apQueue = []
        self.accessPoints = {}
        self.apFreePort = {}
        self.gatewayIP = ''
        self.numberOfUsers = 50

    def simulation_old( self, net ):
        print '* h1 requesting video1'
        #net.get('h1').cmd('wget 10.0.0.17:8080/video1.mp4')
        #print '* success'
        net.get('s5').attach('s5-eth4', True)
        h1, old = net.get( 'h1', 's4' )
        new = net[ 's5' ]
        port = 15
        print '* Moving', h1, 'from', old, 'to', new, 'port', port
        hintf, sintf = moveHost( h1, old, new, newPort=port )
        print '*', hintf, 'is now connected to', sintf
        print '* New network:'
        printConnections( net.switches )
        print '* Testing connectivity:'
        old = new

    def createServer( self, net, hostIndex ):
        print '***  Creating main server on network root\n'
        host = net.addHost('h' + str(hostIndex))
        self.gatewayIP = str(IPAddress(167772160 + hostIndex))
        print self.gatewayIP
        rootSwitch = net.get('s1')
        net.addLink(host, rootSwitch)
        heth, seth = host.connectionsTo( rootSwitch )[ 0 ]
        self.gatewayMAC = host.MAC(heth)
        self.gatewayID = hostIndex
        host.cmd('python simple_server.py &')
        
        return hostIndex + 1 

    def addAccessPoints( self, net, nextSwitchIndex, apsByBuildings, buildingNames):
        nsi = nextSwitchIndex
        for apGroup in self.apQueue:
            switch = net.get('s%d' % apGroup[0])
            buildingName = buildingNames[apGroup[1]]
            txt = "Switch " + str(apGroup[0]) + " has APS " 
            for ap in apsByBuildings[buildingName]:
                txt += " %d," % nsi
                s = net.addSwitch('s' + str(nsi))
                net.addLink( s , switch)
                self.accessPoints[ap['APname']] = nsi
                self.apFreePort[nsi] = 3
                nsi = nsi + 1

            print txt
        return nsi

    def addHosts( self, net, nextHostIndex ):
        hostIndex = nextHostIndex
        lastHost = nextHostIndex + self.numberOfUsers
        self.hostSwitchMap = {}
        while hostIndex <= lastHost:
            si = random.choice(self.accessPoints.values())
            h = net.addHost('h%d' % hostIndex)
            s = net.get('s%d' % si)
            net.addLink(h, s)
            self.hostSwitchMap[hostIndex] = si
            self.apFreePort[si] += 1
            hostIndex = hostIndex + 1


    def addCacheServers( self, net, nextHostIndex, switchCount ):
        print "**** Adding cache servers on every switch: h%d - h%d" % (nextHostIndex, nextHostIndex + switchCount - 1)
        nhi = nextHostIndex
        for i in range(1, switchCount):
            s = net.get('s' + str(i))
            cache = net.addHost('h' + str(nhi))
            net.addLink(cache, s)
            self.startSquid(cache, nhi)
            nhi = nhi + 1

        return nhi

    def startSquid( self, cache, cacheId):
        cache.cmd('sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3128 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('sudo iptables -t nat -A POSTROUTING -j MASQUERADE 2> /home/ubuntu/mag/errors.txt')
        cache.cmd('/home/ubuntu/mag/squid/run-squid.sh ' + str(cacheId))


    def networkFromCLusters( self, clusters, linkage, size, apsByBuildings, buildingNames ):
        net = Mininet( controller=None, switch=MobilitySwitch, cleanup=True )
        ryu_controller = net.addController( 'c0', controller=RemoteController, ip="0.0.0.0", port=6633)
        #Controller is from http://sdnhub.org/releases/sdn-starter-kit-ryu/
        
        si = 2
        net.addSwitch('s1')
        nextHostIndex = 1
        buildingIndex = 0
        links = [linkage[len(linkage) - 1,0], linkage[len(linkage) - 1,1]]
        print '*** Creating topology\n'
        while(len(links) != 0):
            lnks = []
            for li in links:
                li = li - size
                parentSwitchIndex = si - 1
                parentSwitch = net.get('s' + str(parentSwitchIndex))
                txt = "PS " + str(parentSwitchIndex)
                tempSwitch1 = linkage[li, 0] - size
                tempSwitch2 = linkage[li, 1] - size

                if (tempSwitch1 >= 0):
                    s = net.addSwitch('s' + str(si))
                    txt += " has children " + str(si)
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch1, 0] >= size):
                        lnks.append(linkage[tempSwitch1, 0])
                    else:
                        self.apQueue.append([si - 1, buildingIndex])
                        buildingIndex = buildingIndex + 1

                    s = net.addSwitch('s' + str(si))
                    txt += ", " + str(si)
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch1, 1] >= size):
                        lnks.append(linkage[tempSwitch1, 1])
                    else:
                        self.apQueue.append([si - 1, buildingIndex])
                        buildingIndex = buildingIndex + 1                

                else:
                    s = net.addSwitch('s' + str(si))
                    txt += " has children " + str(si)
                    si = si + 1
                    net.addLink( s, parentSwitch )

                if (tempSwitch2 >= 0):
                    s = net.addSwitch('s' + str(si))
                    txt += ", " + str(si)
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch2, 0] >= size):
                        lnks.append(linkage[tempSwitch2, 0])
                    else:
                        self.apQueue.append([si - 1, buildingIndex])
                        buildingIndex = buildingIndex + 1 

                    s = net.addSwitch('s' + str(si))
                    txt += ", " + str(si)
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch2, 1] >= size):
                        lnks.append(linkage[tempSwitch2, 1])
                    else:
                        self.apQueue.append([si - 1, buildingIndex])
                        buildingIndex = buildingIndex + 1 

                else:
                    s = net.addSwitch('s' + str(si))
                    txt += ", " + str(si)
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    self.apQueue.append([si - 1, buildingIndex])
                    buildingIndex = buildingIndex + 1

                print txt 
                si = self.addAccessPoints(net, si, apsByBuildings, buildingNames)

            links = lnks


        print '*** Adding cache servers\n'
        nextHostIndex = self.addCacheServers( net, nextHostIndex, si)
        print '*** Creating gateway host and starting web server\n'
        nextHostIndex = self.createServer(net, nextHostIndex)
        self.lastSwitch = si - 1
        self.firstHostIndex = nextHostIndex
        nextHostIndex = self.addHosts( net, nextHostIndex)

        print '*** Starting network\n'
        net.start()

        return net

    def debug( self, net, host):
        for i in range(1, 33):
            print host.connectionsTo(net.get('s%d' % i))

    def simulation( self, net ):
        print '*** Simulation started'

        limit = 500 
        requestCount = 0
        fieldnames = ['timestamp', 'hostIndex', 'AP']
        CLI(net)
        with open('/data/movement.csv', 'rb') as csvfile:
            requests = csv.DictReader(csvfile, fieldnames, delimiter=',')
            for req in requests:
                hostIndex = int(req['hostIndex']) + self.firstHostIndex
                if req['AP'] in self.accessPoints and hostIndex <= self.numberOfUsers:
                    hostCurrentlyOn = self.hostSwitchMap[hostIndex]
                    host = net.get('h%d' % hostIndex)

                    #If we need to move host
                    APIndex = self.accessPoints[req['AP']]
                    if hostCurrentlyOn != APIndex:
                        #print "host " + str(hostIndex) + " currently on %d" % hostCurrentlyOn
                        #self.debug(net, host)
                        #CLI(net)

                        oldSwitch = net.get('s%d' % hostCurrentlyOn)
                        newSwitch = net.get('s%d' % APIndex)
                        print APIndex
                        self.hostSwitchMap[hostIndex] = APIndex
                        self.moveHost(net, host, oldSwitch, newSwitch, newPort=self.apFreePort[APIndex] )
                        self.apFreePort[hostCurrentlyOn] -= 1
                        self.apFreePort[APIndex] += 1

                    #TODO: move host to target AP, request random content, measure delay
                    print "Foo %d" % hostIndex
                    #if APIndex == 8:
                    #    CLI(net)
                    host.cmd('wget -qO- ' + self.gatewayIP + '/ryu &> /dev/null')
                    print "Bar"
                    requestCount = requestCount + 1
                if requestCount > limit:
                	break

        print requestCount

    def moveHost( self, net, host, oldSwitch, newSwitch, newPort=None ):
        "Move a host from old switch to new switch"

        hintf, sintf = host.connectionsTo( oldSwitch )[ 0 ]
        oldSwitch.moveIntf( sintf, newSwitch, port=newPort, rename=True )

        for i in range(1, self.lastSwitch + 1):
            net.get('s%d' % i).cmd('sudo arp -d ' + host.IP())
        #oldSwitch.cmd('sudo arp -d ' + host.IP())
        #oldSwitch.setARP(host.IP(), host.MAC(hintf))
        host.cmd('sudo arp -d ' + self.gatewayIP)
        host.setARP(self.gatewayIP, self.gatewayMAC)
        net.get('h%d' % self.gatewayID).setARP(host.IP(), host.MAC(hintf))
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
    net = networkManager.networkFromCLusters(clusters, linkage, len(buildings), apsByBuildings, buildingNames)
    
    print '*** Getting requests data'
    movementParser = MovementDataParser('/home/ubuntu/Downloads/movement/2001-2003/', '/data/movement.csv')
    movementParser.getMovementInfo()
    networkManager.simulation(net)
    CLI( net )
    net.stop()
    #createNetwork(4,2) #2^4 hosts

