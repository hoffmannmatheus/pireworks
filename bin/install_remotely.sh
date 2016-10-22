#!/bin/sh

#
# This script installs all Pireworks dependencies on your raspberry pi.
#
# BEWARE, this script assumes that:
# - The raspberry pi user and hostname are Raspbian default (pi@raspberry)
# - The raspberry pi is connected to the same local network as this computer.
# - MDNS works on this network (check how $PI is set: no ip needed in  this case)
#

SOURCE=..
PI=pi@raspberrypi.local  # You can replace this by pi@12.34.56.78

# Install dependencies
ssh $PI "sudo apt-get update;
sudo apt-get install python-dev python-bluez python-pyaudio bluetooth libbluetooth-dev -y;
sudo pip install bluez numpy"

