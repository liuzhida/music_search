#!/bin/bash
for i in {8001..8008};
do
    python music.py --port=$i 1>>music.log 2>&1 &
done
