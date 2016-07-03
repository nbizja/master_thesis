#!/usr/bin/python

import requests

class CacheManager():
	def __init__(self):
		self.url = "http://localhost:8080/stats/flowentry/add"
		self.gatewayIp = "10.0.0.16"

	def changeRoute(self, clientId, cacheId):
		incomingRoute = requests.post(self.url, json =
			{
			    "dpid": 1,
			    "idle_timeout": 30,
			    "hard_timeout": 30,
			    "priority": 44444,
			    "match":{
			        "arp_spa": "10.0.0." + str(cacheId),
			        "arp_tpa": "10.0.0." + str(clientId),
			        "eth_type": 2054
			    },
			    "actions":[
			        {
			            "type": "SET_FIELD",
			            "field": "arp_spa",
			            "value": self.gatewayIp,
			            "eth_type": 2054
			        },
			        {
			            "type":"OUTPUT",
			            "port": 1
			        }
			    ]
			}
		)
		
		#print 'Changing incoming route. Status (' + incomingRoute.status_code + ') \n'

		outgoingRoute = requests.post(self.url, json =
			{
			    "dpid": 4,
			    "idle_timeout": 30,
			    "hard_timeout": 30,
			    "priority": 44444,
			    "match":{
			        "arp_spa": "10.0.0." + str(clientId),
			        "arp_tpa": self.gatewayIp,
			        "eth_type": 2054
			    },
			    "actions":[
			        {
			            "type": "SET_FIELD",
			            "field": "arp_tpa",
			            "value": "10.0.0." + str(cacheId),
			            "eth_type": 2054
			        },
			        {
			            "type":"OUTPUT",
			            "port": 3
			        }
			    ]
			}
		)

		#print 'Changing incoming route. Status (' + outgoingRoute.status_code + ') \n'