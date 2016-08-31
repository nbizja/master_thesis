#!/bin/bash

if [[ "$1" == 2 ]]; then
	echo "include /home/ubuntu/mag/squid/squid-base.conf
	pid_filename /var/run/squid$1.pid
	cache_log /var/log/squid/cache$1.log
	access_log /var/log/squid/access$1.log
	cache_store_log /var/log/squid/exp$2/store$1.log
	cache_dir ufs /data/squid/$1 64 16 32" > /home/ubuntu/mag/squid/squid.conf;
else
	echo "include /home/ubuntu/mag/squid/squid-base.conf
	pid_filename /var/run/squid$1.pid
	cache_log /var/log/squid/exp$2/cache$1.log
	access_log /var/log/squid/exp$2/access$1.log
	cache_store_log /var/log/squid/exp$2/store$1.log
	cache_dir ufs /data/squid/$1 64 16 32" > /home/ubuntu/mag/squid/squid.conf;
fi


sudo rm /var/run/squid$1.pid;

sudo rm -R -f /data/squid/$1;

if [ ! -d "/var/log/squid/exp$2" ]; then
	sudo mkdir /var/log/squid/exp$2;
	sudo chown -R proxy:proxy /var/log/squid/exp$2;
	sudo chmod -R 777 /var/log/squid/exp$2;
fi


if [ ! -d "/data/squid/$1" ]; then
    #printf "Creating files... \n"
    sudo touch /var/log/squid/exp$2/cache$1.log;
    sudo touch /var/log/squid/exp$2/access$1.log;
    sudo touch /var/log/squid/exp$2/store$1.log;

    sudo mkdir /data/squid/$1;

    sudo chown -R proxy:proxy /data/squid/$1;
    sudo chmod -R 777 /data/squid/$1;

    sudo chown proxy:proxy /var/log/squid/exp$2/cache$1.log;
    sudo chown proxy:proxy /var/log/squid/exp$2/access$1.log;
    sudo chown proxy:proxy /var/log/squid/exp$2/store$1.log;

    sudo squid -z -f /home/ubuntu/mag/squid/squid.conf;
fi
printf "Starting squid $1 \n";

sudo squid -N -f /home/ubuntu/mag/squid/squid.conf &