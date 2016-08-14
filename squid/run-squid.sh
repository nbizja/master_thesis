#!/bin/bash

echo "include /home/ubuntu/mag/squid/squid-base.conf
pid_filename /var/run/squid$1.pid
cache_log /var/log/squid/cache$1.log
access_log /var/log/squid/access$1.log
cache_dir ufs /var/cache/squid$1 128 16 256" > /home/ubuntu/mag/squid/squid.conf;

if [ ! -d "/var/cache/squid$1" ]; then
    sudo touch /var/log/squid/cache$1.log;
    sudo touch /var/log/squid/access$1.log;
    sudo mkdir /var/cache/squid$1;
    sudo chown -R proxy:proxy /var/cache/squid$1;
    sudo chmod -R 777 /var/cache/squid$1;
    sudo chown proxy:proxy /var/log/squid/cache$1.log;
    sudo chown proxy:proxy /var/log/squid/access$1.log;
    sudo squid -z -N -d 2 -f /home/ubuntu/mag/squid/squid.conf;
    sudo squid -N -d 2 -f /home/ubuntu/mag/squid/squid.conf;
else
    sudo squid -N -d 2 -f /home/ubuntu/mag/squid/squid.conf;
fi

