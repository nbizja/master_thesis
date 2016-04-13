#!/usr/bin/python

"""
> As I've mentioned before, you can use the Mininet.addHost() and
> Mininet.addLink() methods to add new hosts and links to a network, and then
> you can use Switch.attach() to connect the new switch port to the switch
> (you will also have to configure your new host.) You can disconnect a host
> from a switch either by bringing the host or switch interface down, or by
> using Switch.detach().
>
> This is easily demonstrated:
>
> $ sudo mn -v output
> mininet> py net.addHost('h3')
> <Host h3:  pid=3405>
> mininet> py net.addLink(s1, net.get('h3'))
> <mininet.link.Link object at 0x1737090>
> mininet> py s1.attach('s1-eth3')
> mininet> py net.get('h3').cmd('ifconfig h3-eth0 10.3')
> mininet> h1 ping -c1 10.3
> PING 10.3 (10.0.0.3) 56(84) bytes of data.
> 64 bytes from 10.0.0.3: icmp_req=1 ttl=64 time=1.91 ms
"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
from mininet.topolib import TreeNet
from mininet.net import Mininet
from mininet.log import output, warn
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

def createNetwork(depth, fanout):
    "A simple test of mobility"
    print '* Simple mobility test'
    net = TreeNet( depth=depth, fanout=fanout, switch=OVSSwitch )
    print '* Starting network:'
    net.start()
    addGatewayHost(net, pow(fanout, depth))
    print '* Testing network'
    #net.pingAll()

    CLI( net )
    net.stop()

def addGatewayHost( net, numberOFHosts ):
    host = str((numberOFHosts + 1))
    hostname = 'h' + host
    net.addHost(hostname)
    net.addLink(net.get('s1'), net.get(hostname))
    net.get('s1').attach('s1-eth3')
    net.get(hostname).setIP('10.' + host)
    print '* Gateway host ' + hostname + ' with ip ' + '10.' + host
    print '* Creating server on a gateway host...'
    createServer(net.get(hostname))

def createServer( host ):
    host.cmd('python simple_server.py &')

if __name__ == '__main__':
    setLogLevel( 'info' )
    createNetwork(4,2)
