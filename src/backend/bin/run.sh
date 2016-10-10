#/bin/bash

# Notes:
# Might need to edit file via "sudo vim /lib/systemd/system/bluetooth.service"
# Add --compat to line "ExecStart=/usr/lib/bluetooth/bluetoothd
# Then run "sudo systemctl daemon-reload"
# Might alswo need to add "DisablePlugins = pnat"
# to /etc/bluetooth/main.conf
# Then run sudo invoke-rc.d bluetooth restart

sudo service bluetooth start
sudo sdptool add SP
sudo hciconfig hci0 piscan

~/pireworks/src/common/watch_dog.sh sudo python ~/pireworks/src/backend/src/server.py

