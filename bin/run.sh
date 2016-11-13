#/bin/bash

PIREWORKS=/home/pi/pireworks/src
WATCHDOG=$PIREWORKS/common/watchdog.sh

# Make sure bluetooth service is running
sudo service bluetooth start
sudo sdptool add SP
sudo hciconfig hci0 piscan

# Stop any python stripts
sudo killall watchdog.sh
sudo killall python

# Run backend
cd $PIREWORKS
sudo $WATCHDOG python main.py

echo "Running pireworks!"
