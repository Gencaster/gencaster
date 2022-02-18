#!/bin/sh

echo "Start Jack"

jackd -r -d dummy -r 48000 & sleep 3

echo "Started jack!"

echo "Start SC"

sclang /home/sc/sc.scd & sleep 5

echo "Started sclang"

echo "Start janus"

/opt/janus/bin/janus & sleep 3

echo "Start ffmpeg"

ffmpeg -f jack -i ffmpeg -quality realtime -ar 48000 -c:a libopus -vn -f rtp rtp://127.0.0.1:5002 > ffmpeg.log 2>&1 < /dev/null &

sleep 3

echo "Connect SuperCollider to ffmpeg via jack"

jack_connect SuperCollider:out_1 ffmpeg:input_1
# jack_connect SuperCollider:out_2 ffmpeg:in_2

# lol?
sleep 1000000000000000000