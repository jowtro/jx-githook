#!/bin/bash
set -e
homedir=/home/pi/work/jx-githook
echo "read enviroment variables"
export $(cat .env | xargs)
echo "running python´"
${homedir}/venv/bin/python ${homedir}/src/main.py
