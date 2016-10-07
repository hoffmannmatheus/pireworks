#/bin/bash

sudo apt-get update; sudo apt-get install python-dev python-bluez -y
sudo apt-get install bluetooth libbluetooth-dev -y
sudo pip install bluez
sudo bash -c "echo 'PRETTY_HOSTNAME=Pireworks' > /etc/machine-info"
