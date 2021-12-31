#!/bin/bash
# pull the script and then call script to build front-end

#path is argument
cd $1

dt_now="INFO"[$(date '+%Y-%m-%d %T')]

echo "$dt_now cd $1" > debug_git_pull.log

result=$(git pull)
echo $result >> debug_git_pull.log

echo "Running build with version" >> debug_git_pull.log
result=$(bash -x "$1/build_with_version.sh")
echo $result >> debug_git_pull.log
