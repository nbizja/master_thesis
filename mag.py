#!/usr/bin/python


from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, RemoteController
from mininet.topolib import TreeNet
from mininet.net import Mininet
from mininet.log import output, warn
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

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


def printConnections( switches ):
    "Compactly print connected nodes to each switch"
    for sw in switches:
        output( '%s: ' % sw )
        for intf in sw.intfList():
            link = intf.link
            if link:
                intf1, intf2 = link.intf1, link.intf2
                remote = intf1 if intf1.node != sw else intf2
                output( '%s(%s) ' % ( remote.node, sw.ports[ intf ] ) )
        output( '\n' )


def moveHost( host, oldSwitch, newSwitch, newPort=None ):
    "Move a host from old switch to new switch"
    hintf, sintf = host.connectionsTo( oldSwitch )[ 0 ]
    oldSwitch.moveIntf( sintf, newSwitch, port=newPort )
    return hintf, sintf
    
def createNetwork(depth, fanout):
	"A simple test of mobility"
	print '* Simple mobility test'
	net = TreeNet( depth=depth, fanout=fanout, switch=MobilitySwitch, controller=None)
	print '* Starting network:'

	ryu_controller = net.addController( 'c0', controller=RemoteController, ip="0.0.0.0", port=6633)
	#Controller is from http://sdnhub.org/releases/sdn-starter-kit-ryu/
	
	net.start()


	addGatewayHost(net, pow(fanout, depth))
	#print '* Testing network'
	#net.pingAll()
	simulation(net)
	CLI( net )
	net.stop()

def addGatewayHost( net, numberOFHosts ):
	host = str((numberOFHosts + 1))
	hostname = 'h' + host
	net.addHost(hostname)
	net.addLink(net.get('s1'), net.get(hostname))
	net.get('s1').attach('s1-eth3', True)
	net.get(hostname).setIP('10.' + host)
	print '* Gateway host ' + hostname + ' with ip ' + '10.' + host
	print '* Creating server on a gateway host...'
	createServer(net.get('h16'))

def createServer( host ):
	host.cmd('python simple_server.py &')

def simulation( net ):
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

if __name__ == '__main__':
	setLogLevel( 'info' )
	createNetwork(4,2) #2^4 hosts
