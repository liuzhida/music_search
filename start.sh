#!/bin/bash
python $1 1>>$1.log 2>&1 &
