#!/bin/bash

echo "move to repo DIR"
cd $1
echo "git pull"
git pull
echo "DONE"