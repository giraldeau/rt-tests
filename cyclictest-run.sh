#!/bin/sh

./cyclictest -l 1000 -t &
P=$!

stress --cpu 8 --io 4 --vm 2 --vm-bytes 128M --timeout 2s

wait $P
