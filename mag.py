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
import csv
import random

class MobilitySwitch( OVSSwitch ):
    "Switch that can reattach and rename interfaces"

    def delIntf( self, intf ):
        "Remove (and detach) an interface"
        port = self.ports[ intf ]
        del self.ports[ intf ]
        del self.intfs[ port ]
        del self.nameToIntf[ intf.name ]

    def addIntf( self, intf, rename=False, **kwargs ):
        "Add (and reparent) an interface"
        OVSSwitch.addIntf( self, intf, **kwargs )
        intf.node = self
        if rename:
            self.renameIntf( intf )

    def attach( self, intf, isNew=False ):
        "Attach an interface and set its port"
        if isNew:
            super(MobilitySwitch, self).attach(intf)
        else:
            port = self.ports[ intf ]
            if port:
                if self.isOldOVS():
                    self.cmd( 'ovs-vsctl add-port', self, intf )
                else:
                    self.cmd( 'ovs-vsctl add-port', self, intf,
                              '-- set Interface', intf,
                              'ofport_request=%s' % port )
                self.validatePort( intf )

    def validatePort( self, intf ):
        "Validate intf's OF port number"
        ofport = int( self.cmd( 'ovs-vsctl get Interface', intf,
                                'ofport' ) )
        if ofport != self.ports[ intf ]:
            warn( 'WARNING: ofport for', intf, 'is actually', ofport,
                  '\n' )

    def renameIntf( self, intf, newname='' ):
        "Rename an interface (to its canonical name)"
        intf.ifconfig( 'down' )
        if not newname:
            newname = '%s-eth%d' % ( self.name, self.ports[ intf ] )
        intf.cmd( 'ip link set', intf, 'name', newname )
        del self.nameToIntf[ intf.name ]
        intf.name = newname
        self.nameToIntf[ intf.name ] = intf
        intf.ifconfig( 'up' )

    def moveIntf( self, intf, switch, port=None, rename=True ):
        "Move one of our interfaces to another switch"
        self.detach( intf )
        self.delIntf( intf )
        switch.addIntf( intf, port=port, rename=rename )
        switch.attach( intf )


class NetworkManager():

    def __init__(self):
        self.accessPoints = {}
        self.gatewayIP = ''
        self.numberOfUsers = 50

    def moveHost( self, host, oldSwitch, newSwitch, newPort=None ):
        "Move a host from old switch to new switch"
        hintf, sintf = host.connectionsTo( oldSwitch )[ 0 ]
        oldSwitch.moveIntf( sintf, newSwitch, port=newPort )
        return hintf, sintf

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
        host.cmd('python simple_server.py &')
        
        return hostIndex + 1

    def addAccessPoints( self, net, switch, buildingIndex, nextSwitchIndex, apsByBuildings, buildingNames ):
        buildingName = buildingNames[buildingIndex]
        nsi = nextSwitchIndex
        for ap in apsByBuildings[buildingName]:
            s = net.addSwitch('s' + str(nsi))
            net.addLink( s , switch)
            self.accessPoints[ap['APname']] = nsi
            nsi = nsi + 1

        return nsi

    def addHosts( self, net, nextHostIndex ):
        hostIndex = nextHostIndex
        lastHost = nextHostIndex + self.numberOfUsers
        while hostIndex <= lastHost:
            si = random.choice(self.accessPoints.values())
            h = net.addHost('h%d' % hostIndex)
            s = net.get('s%d' % si)
            net.addLink(h, s)
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
        net = Mininet( controller=None, cleanup=True )
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
                parentSwitch = net.get('s' + str(si - 1))
                tempSwitch1 = linkage[li, 0] - size
                tempSwitch2 = linkage[li, 1] - size

                if (tempSwitch1 >= 0):
                    s = net.addSwitch('s' + str(si))
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch1, 0] >= size):
                        lnks.append(linkage[tempSwitch1, 0])
                    else:
                        si = self.addAccessPoints(net, s, buildingIndex, si, apsByBuildings, buildingNames)
                        buildingIndex = buildingIndex + 1

                    s = net.addSwitch('s' + str(si))
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch1, 1] >= size):
                        lnks.append(linkage[tempSwitch1, 1])
                    else:
                        si = self.addAccessPoints(net, s, buildingIndex, si, apsByBuildings, buildingNames)
                        buildingIndex = buildingIndex + 1                

                else:
                    s = net.addSwitch('s' + str(si))
                    si = si + 1
                    net.addLink( s, parentSwitch )

                if (tempSwitch2 >= 0):
                    s = net.addSwitch('s' + str(si))
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch2, 0] >= size):
                        lnks.append(linkage[tempSwitch2, 0])
                    else:
                        si = self.addAccessPoints(net, s, buildingIndex, si, apsByBuildings, buildingNames)
                        buildingIndex = buildingIndex + 1 

                    s = net.addSwitch('s' + str(si))
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    if (linkage[tempSwitch2, 1] >= size):
                        lnks.append(linkage[tempSwitch2, 1])
                    else:
                        si = self.addAccessPoints(net, s, buildingIndex, si, apsByBuildings, buildingNames)
                        buildingIndex = buildingIndex + 1 

                else:
                    s = net.addSwitch('s' + str(si))
                    si = si + 1
                    net.addLink( s, parentSwitch )
                    si = self.addAccessPoints(net, s, buildingIndex, si, apsByBuildings, buildingNames)
                    buildingIndex = buildingIndex + 1 

            links = lnks

        print '*** Adding cache servers\n'
        nextHostIndex = self.addCacheServers( net, nextHostIndex, si)
        print '*** Creating gateway host and starting web server\n'
        nextHostIndex = self.createServer(net, nextHostIndex)
        nextHostIndex = self.addHosts( net, nextHostIndex)

        print '*** Starting network\n'
        net.start()

        return net

    def simulation( self, net ):
        print '*** Simulation started'

        limit = 500 
        requestCount = 0
        fieldnames = ['timestamp', 'hostIndex', 'AP']
        with open('/data/movement.csv', 'rb') as csvfile:
            requests = csv.DictReader(csvfile, fieldnames, delimiter=',')
            for req in requests:
                if req['AP'] in self.accessPoints and int(req['hostIndex']) <= self.numberOfUsers:
                    net.get('h' + req['hostIndex']).cmd('wget -qO- ' + self.gatewayIP + '/ryu &> /dev/null')
                    requestCount = requestCount + 1
                if requestCount > limit:
                	break

        print requestCount

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

