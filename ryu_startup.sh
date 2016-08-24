#!/bin/sh

export PYTHONPATH=$PYTHONPATH:.

/home/ubuntu/ryu/bin/ryu-manager --observe-links --verbose ryu.app.ofctl_rest ryu.app.sdnhub_apps.stateless_lb_rest ryu.app.sdnhub_apps.learning_switch  #--observe-links  
