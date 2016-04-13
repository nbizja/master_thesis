#!/bin/bash

content_size=5
for (( filenum=1; filenum <= 10; filenum++ ))
do
    #Create file with specific content_size
    dd if=/dev/zero of=/home/ubuntu/mag/videos/video$filenum.mp4  bs=1M  count=$content_size

    case $filenum in
        4 )
            content_size=10 ;;
        7 )
            content_size=15 ;;
        9 )
            content_size=25 ;;
    esac


    
done
