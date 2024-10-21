#!/usr/bin/env python3

# Version 3.2

import subprocess
from subprocess import getoutput
import json
import requests
import time
import urllib3
import syslog
from random import randint
from time import sleep
urllib3.disable_warnings()

zabbix = "172.26.12.29"
host = "PB-A01-LEP001-SP"

sleepTime = randint(1,15)*30
syslog.syslog("sleep "+sleepTime)
sleep(sleepTime)


domains = {   
        "google": "google.com", 
        "facebook": "facebook.com",  
        "youtube": "youtube.com",
        "whatsapp": "whatsapp.com",
        "tiktok": "tiktok.com",
        "mercadolivre": "mercadolivre.com.br",
        "nubank": "nubank.com.br",
        "globo": "globo.com",
        "uol": "uol.com.br",
        "instagran": "instagran.com"
}

def dns():
    command="dig google.com.br | grep Query"
    resDns = getoutput(command)
    timeDns = resDns.split(' ')[3]
    #print (timeDns)

    keys = {"dns_latency": timeDns}

    for key, value in keys.items():
        command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
        #print (command)
        syslog.syslog(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    

def speedTest():
    command="speedtest -s 31991 --format=json"
    resSpeedtest = getoutput(command)
    JresSpeedtest = json.loads(resSpeedtest)


    StDownload = JresSpeedtest['download']['bandwidth']/125000
    StUpload = JresSpeedtest['upload']['bandwidth']/125000
    StJitter = JresSpeedtest ['ping']['jitter']
    StLatency = JresSpeedtest ['ping']['latency']

    keys = {"st_latency": StLatency,"st_download": StDownload,"st_upload": StUpload, "st_jitter": StJitter}

    for key, value in keys.items():
        command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
        #print (command)
        syslog.syslog(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def icmp():
    count = 0

    for URL in domains.values():
        service = list(domains.keys())[count]
        #print (URL)

        command="ping -n -q -c 5 "+URL
        out = getoutput(command)
        allOut = out.split('\n')

        #split result to get all lines of ping 
        resPing = str(allOut[-1]).split(' ')
        resPingPackets = str(allOut[-2]).split(' ')

        #Geting loss packagets
        resLoss = int(resPingPackets[5].replace("%", ""))

        if resLoss == 100:
            resLatency = 0
            resJitter = 0
        else:
            #Geting Average time (latency)
            resLatency = float(resPing[3].split("/")[1])
                            
            #Geting Jitter
            resJitter = float(resPing[3].split("/")[3])

        keys = {service+"_latency": resLatency,service+"_jitter": resJitter,service+"_loss": resLoss}

        for key, value in keys.items():
            command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
            #print (command)
            syslog.syslog(command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        count = count+1


def webpages():
    count = 0


    for URL in domains.values():
        service = list(domains.keys())[count]
        #print (URL)

        start_time = time.time()
        response = requests.get("https://"+URL, verify=False)
        end_time = time.time()
        loading_time = end_time - start_time
    
        resWeb = "{:.2f}".format(loading_time)

        keys = {service+"_web_latency": resWeb}

        for key, value in keys.items():
            command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
            #print (command)
            syslog.syslog(command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        count = count+1

#def mtr():
    # mtr -4 -n -r -c3 -w -b -p -j google.com
    # mtr -4 -n -r -c3 -w -b google.com

dns()
icmp()
speedTest()
webpages()
