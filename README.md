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


Videos are served from ~/mag/videos (videos itself are not included).
Hello world example:
```
mininet-wifi> h1 wget 10.0.0.17:8080/helloworld
```

To run simulation (work in progress):
```
mininet-wifi> py execfile("simulation.py")
```

Statistics overview can be obtained on http://0.0.0.0:8080/web/stats.html 


Data in json from can be obtained for all switches: http://0.0.0.0:8080/stats/flow/{id_of_switch}

Most important fields used for our metric are **packet_count and **byte_count .





