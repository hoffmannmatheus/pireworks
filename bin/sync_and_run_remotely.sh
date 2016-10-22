#!/bin/sh

#
# This script copies Pireworks source code from your computer and runs Pireworks
# it on the Raspberry Pi.
#
# BEWARE, this script assumes that:
# - The raspberry pi user and hostname are Raspbian default (pi@raspberry)
# - The raspberry pi is connected to the same local network as this computer.
# - MDNS works on this network (check how $PI is set: no ip needed in  this case)
#

SOURCE=..
PI=pi@raspberrypi.local  # You can replace by the real IP, eg: "pi@12.34.56.78"
PIREWORKS=/home/pi/pireworks

# Copy repository to RPi
rsync -avhPS --delete --exclude $SOURCE/.git $SOURCE $PI:$PIREWORKS

# Run
ssh $PI "${PIREWORKS}/bin/run.sh"
