#!/bin/bash

function ctrl_c() {
  echo "*** Stopping all started jobs ***"
  kill $db_pid
  exit 
}

trap ctrl_c 2 # 2 for SIGINT

if [ -z "$1" ]; then
  echo "Searching for open serial port..."
  PORT=`../tools/find_port.sh`
  FIND_PORT_RETURNCO=$?
  if [ $FIND_PORT_RETURNCO -eq 1 ]; then
    echo "Port couldn't be found"
    read -p "Create artificial serial port? [Y/n]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then 
      echo "Creating a pseudo terminal..." 
      ART=1
      PORT="PTY"
    else
      ART=0
    fi 
  else
    ART=0
  fi
  echo "Selected port -> $PORT"
else
  PORT=$1
  echo "HERE"
  exit
fi

export RERE_PORT=$PORT # check if this works later

# required on linux
echo ART $ART
if [ $ART == 0 ]; then
  if [ `uname` == "Linux" ]; then
    if  [ "`stat -c '%a' $PORT`" == "660" ] ; then
      echo "Changing permissions of $PORT to 660"
      sudo chmod a+rw $PORT
    fi
  fi
fi

echo "Starting db.py in WRITE mode"
WRITE=1 ./db.py & 
db_pid=$!
echo "Starting flask server"
./serve.py 
