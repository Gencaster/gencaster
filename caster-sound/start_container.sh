#!/bin/sh

docker build -t caster_sound .

docker run \
    --rm \
    --name caster_sound \
    --ulimit rtprio=75:75 \
    --ulimit memlock=256000:256000 \
    -p 8089:8089 \
    -p 8088:8088 \
    caster_sound
