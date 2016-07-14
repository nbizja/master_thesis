#!/bin/bash

echo
"include /home/ubuntu/mag/squid/squid-base.conf

pid_filename /var/run/squid$1.pid
cache_log /var/log/squid/cache$1.log
access_log /var/log/squid/access$1.log
cache_dir ufs /var/cache/squid$1 1048 128 512 max-size=16777216" > /home/ubuntu/mag/squid/squid.conf;

if [ ! -f "/var/cache/squid$1.txt" ]; then
    sudo touch /var/log/squid/cache$1.log;
    sudo touch /var/log/squid/access$1.log;
    sudo mkdir /var/cache/squid$1;
    sudo chown proxy:proxy /var/log/squid/cache$1.log;
    sudo chown proxy:proxy /var/log/squid/access$1.log;
    sudo squid -z -N -d 8 -f /home/ubuntu/mag/squid/squid.conf 2> /home/ubuntu/mag/errors.txt
else
    sudo squid -N -d 8 -f /home/ubuntu/mag/squid/squid.conf 2> /home/ubuntu/mag/errors.txt
fi

