#!/usr/bin/python


from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, RemoteController
from mininet.topolib import TreeNet
from mininet.net import Mininet
from mininet.log import output, warn
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

def createNetwork(depth, fanout):
    "A simple test of mobility"
    print '* Simple mobility test'
    net = TreeNet( depth=depth, fanout=fanout, controller=None)
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
    net.get('s1').attach('s1-eth3')
    net.get(hostname).setIP('10.' + host)
    print '* Gateway host ' + hostname + ' with ip ' + '10.' + host
    print '* Creating server on a gateway host...'
    createServer(net.get(hostname))

def createServer( host ):
    host.cmd('python simple_server.py &')

def simulation( net ):
    print '* h1 requesting video1'
    net.get('h1').cmd('wget 10.0.0.17:8080/video1.mp4')
    print '* success'

if __name__ == '__main__':
    setLogLevel( 'info' )
    createNetwork(4,2) #2^4 hosts
