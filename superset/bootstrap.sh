#!/bin/bash

# Functions

DATE() {
  date '+%Y-%m-%d %H:%M:%S'
}

# Let's go
# Update the System
echo "[$(DATE)] [Info] [System] Updating the system..."
apt update &> /dev/null
# Install Java
if [ $(dpkg-query -W -f='${Status}' openjdk-8-jdk 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  echo "[$(DATE)] [Info] [Java] Installing Java..."
  add-apt-repository -y ppa:openjdk-r/ppa &> /dev/null
  apt update &> /dev/null
  apt -y install openjdk-8-jdk &> /dev/null
fi


