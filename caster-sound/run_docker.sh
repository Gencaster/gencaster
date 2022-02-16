#!/bin/sh

docker run
    --ulimit rtprio=75:75
    --ulimit memlock=256000:256000
