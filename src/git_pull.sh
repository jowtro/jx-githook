#!/bin/bash
path="$1"
echo "move to repo DIR"
echo "git pull"
( cd $path && git pull)
echo "DONE"
