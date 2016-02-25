#!/bin/sh

./cyclictest -l 10000 -t -p99 &
P=$!

stress --cpu 8 --io 4 --vm 2 --vm-bytes 128M --timeout 10s

kill $P
wait $P
