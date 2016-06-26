# Context prediction-based prefetching in software-defined wireless networks
## (Predpomnjenje v programsko definiranih brezžičnih omrežjih na podlagi predvidevanja konteksta)

Author: Nejc Bizjak

Mentor: doc. dr. Veljko Pejović



### Working with: 
* Mininet-wifi  (https://github.com/intrig-unicamp/mininet-wifi)
* Ryu SDN Controller (https://github.com/osrg/ryu/)
* Opencache - Experimental caching platform (https://github.com/broadbent/opencache)


### Running on: http://sdnhub.org/tutorials/sdn-tutorial-vm/


### Instructions

Download and run VM. Clone this repository in /home/ubuntu diretory. Run:

```
cd ~/ryu
./ryu/app/sdnhub_apps/run_sdnhub_apps.sh
```
This will start Ryu Controller on 0.0.0.0. Port 6633 is used for communication between mininet switches and the controller.
On http://0.0.0.0:8080 we can access Ryu GUI.

```
sudo python mag.py
```
This will start a mininet network in a tree topology with additional server on a root node.

Current settings are Tree topology with depth=4 and fanout=2 (16 + 1 hosts, 15 switches).


Run the cache server on host h17 (at the root of the tree topology) and modify the iptables
mininet> xterm h17

In the xterm "Node: h17" run te following commands:
```
root>  iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3128
root>  iptables -t nat -A POSTROUTING -j MASQUERADE
root>  squid3 -N -d 8 -f /home/ubuntu/mag/squid/squid2.conf
```

If we are running this for the first time, then cache store must be initialized by including "-z" option in the squid command.

To trigger redirection import and run the SquidRedirection.json in Postman (Chrome Rest client).
Then we have 30s before redirection rules expire.
In mininet we can test the caching with:
```
mininet> h1 wget http://10.0.0.16/ryu 
```


(this will send request for small ryu.png file which should be cached)
In seperate terminal we can observe cache behaviour:
```
ubuntu> tail /var/log/squid/access.log
```

We should see TCP_MISS for the first request:

10.0.0.1 TCP_MISS/200 51838 GET http://10.0.0.16/ryu - HIER_DIRECT/10.0.0.16 image/png

And TCP_HIT or TCP_MEMORY_HIT for next requests:
10.0.0.1 TCP_MEM_HIT/200 51843 GET http://10.0.0.16/ryu - HIER_NONE/- image/png
10.0.0.1 TCP_HIT/200 51846 GET http://10.0.0.16/ryu - HIER_NONE/- image/png


Alternatively we can use cache server without redirection, but we need to specify this explicitly:
```
mininet>  h1 wget -e use_proxy=yes -e http_proxy=10.0.0.17:8080 http://10.0.0.16:80/ryu
```

Statistics overview can be obtained on http://0.0.0.0:8080/web/stats.html 
Data in json from can be obtained for all switches: http://0.0.0.0:8080/stats/flow/{id_of_switch}
Most important fields used for our metric are **packet_count and **byte_count .





