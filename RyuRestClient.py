import requests
import json

class RyuRestClient():

    DELETE_FLOW_URL = 'stats/flowentry/delete'
    ADD_FLOW_URL = 'stats/flowentry/add'
    STATS_URL = 'stats/flow'

    IDLE_TIMEOUT = 60
    HARD_TIMEOUT = 70
    SERVER_IP = '10.0.0.1'

    def __init__(self, ip, port, APSids ):
        self.ip = ip
        self.port = port
        self.APSids = APSids

    def addCacheRoute(self, host, cache):
        #We add flows to all APs.
        for APid in self.APSids:
            for i in range(1, 51):
                self.post(self.ADD_FLOW_URL, self.answerARPonAPCommand(APid, host, cache, i))

    def post(self, url, body):
        return requests.post('http://localhost:8080/stats/flowentry/add', 
            headers = {'Content-Type': 'application/json'},
            data = json.dumps(body)
        )

    def get(self, url):
        return requests.get('http://localhost:8080/stats/flowentry/delete', 
            headers = {'Content-Type': 'application/json'},
            data = json.dumps(body)
        )

    def answerARPonAPCommand(self, targetSwitchId, host, cache, inPort):
        "This command should be run on all access points. It answers arp request with mac of a cache."
        
        return {
            "dpid": targetSwitchId,
            "idle_timeout": self.IDLE_TIMEOUT,
            "hard_timeout": self.HARD_TIMEOUT,
            "priority": 44444,
            "match":{
                "arp_spa": host.IP(),
                "arp_tpa": self.SERVER_IP,
                "eth_type": 2054,
                "in_port": inPort
            },
            "actions":[
                {
                    "type": "SET_FIELD",
                    "field": "eth_src",
                    "value": host.MAC(),
                    "eth_type": 2054,
                    "in_port": inPort
                },
                {
                    "type": "SET_FIELD",
                    "field": "eth_dst",
                    "value": host.MAC(),
                    "eth_type": 2054
                },
                {
                    "type": "SET_FIELD",
                    "field": "arp_tpa",
                    "value": host.IP(),
                    "eth_type": 2054
                },
                {
                    "type": "SET_FIELD",
                    "field": "arp_spa",
                    "value": self.SERVER_IP,
                    "eth_type": 2054
                },
                {
                    "type":"OUTPUT",
                    "port": inPort
                }
            ]
         }


######################## CURRENTLY NOT IN USE ###########################
    def getArpOutgoingFlow(self, targetSwitchId, host, cache):
        "Return ofctl command for rewriting ARP target (server ip -> cache ip)"
        outputPort = 1
        if cache.IP() == '10.0.0.2': #Cache on root switch
            outputPort = 4

        return {
            "dpid": targetSwitchId,
            "idle_timeout": IDLE_TIMEOUT,
            "hard_timeout": HARD_TIMEOUT,
            "priority": 44444,
            "match":{
                "arp_spa": host.IP(),
                "arp_tpa": SERVER_IP,
                "eth_type": 2054
            },
            "actions":[
                {
                    "type": "SET_FIELD",
                    "field": "arp_tpa",
                    "value": cache.IP(),
                    "eth_type": 2054
                },
                {
                    "type":"OUTPUT",
                    "port": outputPort
                }
            ]
         }  

    def getArpIncomingFlow(self, targetSwitchId, host, cache, outputPort):
        "Return ofctl command for rewriting ARP source (cache ip -> server ip)"
        return {
            "dpid": targetSwitchId,
            "idle_timeout": IDLE_TIMEOUT,
            "hard_timeout": HARD_TIMEOUT,
            "priority": 44444,
            "match":{
                "arp_spa": cache.IP(),
                "arp_tpa": host.IP(),
                "eth_type": 2054
            },
            "actions":[
                {
                    "type": "SET_FIELD",
                    "field": "arp_spa",
                    "value": SERVER_IP,
                    "eth_type": 2054
                },
                {
                    "type":"OUTPUT",
                    "port": outputPort
                }
            ]
         }  