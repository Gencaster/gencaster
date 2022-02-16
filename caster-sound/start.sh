#!/bin/sh

echo "Start Jack"

jackd -r -d dummy -r 48000 & sleep 3

echo "Started jack!"

echo "Start SC"

sclang /home/sc/test.scd

sleep 10

echo "Finished recording?"
