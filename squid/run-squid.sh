#!/bin/bash

echo "include /home/ubuntu/mag/squid/squid-base.conf
pid_filename /var/run/squid$1.pid
cache_log /var/log/squid/cache$1.log
access_log /var/log/squid/access$1.log
cache_dir ufs /data/squid$1 64 16 128" > /home/ubuntu/mag/squid/squid.conf;

sudo rm /var/run/squid$1.pid;

if [ ! -d "/var/cache/squid$1/00" ]; then
    #printf "Creating files... \n"
    sudo touch /var/log/squid/cache$1.log;
    sudo touch /var/log/squid/access$1.log;
    sudo mkdir /var/cache/squid$1;
    sudo chown -R proxy:proxy /var/cache/squid$1;
    #sudo chmod -R 777 /var/cache/squid$1;
    sudo chown proxy:proxy /var/log/squid/cache$1.log;
    sudo chown proxy:proxy /var/log/squid/access$1.log;
    sudo squid -z -f /home/ubuntu/mag/squid/squid$1.conf;
fi
printf "Starting squid $1 \n";

sudo squid -N -d 1 -f /home/ubuntu/mag/squid/squid$1.conf &