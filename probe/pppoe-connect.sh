#!/bin/bash

if ping -c 3 8.8.8.8 &> /dev/null
then
        logger "PPPOE connected"
else
        logger "PPPOE error"
        nmcli connection down PPPOE
        nmcli connection reload
        sleep 5
        nmcli connection up PPPOE
        logger "PPPOE reconected"
        sleep 5
fi
