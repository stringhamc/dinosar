#!/usr/bin/env bash

docker run -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/home/user\
       -it -e LOCAL_USER_ID=`id -u $USER` dinosar:dinosar
