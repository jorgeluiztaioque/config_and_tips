#!/bin/bash

# Download or update Probe

echo "$1" | sudo -S rm -rf /opt/teste-speed.py
#echo "$1" | sudo -S rm -rf /opt/pppoe-connect.sh
cd /opt
echo "$1" | sudo -S wget https://raw.githubusercontent.com/jorgeluiztaioque/config_and_tips/refs/heads/master/probe/teste-speed.py
echo "$1" | sudo -S chmod +x teste-speed.py
#echo "$1" | sudo -S wget https://raw.githubusercontent.com/jorgeluiztaioque/config_and_tips/refs/heads/master/probe/pppoe-connect.sh
#echo "$1" | sudo -S chmod +x pppoe-connect.sh
crontab -r
sudo crontab -r
echo "3n6%r3de" | sudo -S echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" | sudo crontab -
echo "3n6%r3de" | sudo -S crontab -l | { cat; echo "*/15 * * * * /opt/teste-speed.py"; } | sudo crontab -
echo "3n6%r3de" | sudo -S crontab -l | { cat; echo "*/5 * * * * /opt/pppoe-connect.sh"; } | sudo crontab -
varHostname=$(hostname)
sudo sed -i "s/PB-A01-LEP001-SP/$varHostname/" /opt/teste-speed.py
