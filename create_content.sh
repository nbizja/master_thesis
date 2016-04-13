#!/bin/bash

num_of_videos=100 #must be multiplier of 10
content_size=5
for (( filenum=1; filenum <= $num_of_videos; filenum++ ))
do
    #Create file with specific content_size
    dd if=/dev/zero of=/home/ubuntu/mag/videos/video$filenum.mp4  bs=1M  count=$content_size

    case $filenum in
        $((4*$num_of_videos/10)) )
            content_size=10 ;;
        $((7*$num_of_videos/10)) )
            content_size=15 ;;
        $((9*$num_of_videos/10)) )
            content_size=25 ;;
    esac


    
done
