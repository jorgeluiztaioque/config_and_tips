#!/bin/bash

# Download Probe

echo "$1" | sudo -S rm -rf /opt/teste-speed.py
cd /opt
echo "$1" | sudo -S wget https://raw.githubusercontent.com/jorgeluiztaioque/config_and_tips/refs/heads/master/probe/teste-speed.py
echo "$1" | sudo -S chmod +x teste-speed.py
echo "$1" | sudo -S wget https://raw.githubusercontent.com/jorgeluiztaioque/config_and_tips/refs/heads/master/probe/pppoe-connect.sh
echo "$1" | sudo -S chmod +x pppoe-connect.sh
crontab -r
sudo crontab -l | { cat; echo "*/15 * * * * /opt/teste-speed.py"; } | crontab -
sudo crontab -l | { cat; echo "*/5 * * * * /opt/pppoe-connect.sh"; } | crontab -
