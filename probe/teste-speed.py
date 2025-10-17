#!/usr/bin/env python3

# Version 2 
# Custon 4

import subprocess
from subprocess import getoutput
import json
import requests
import time
import urllib3
import syslog
import random 
from random import randint
from time import sleep
urllib3.disable_warnings()

zabbix = "172.26.12.29"
host = "PB-A01-LEP001-SP"
'''
# Time to RUN - Aqui o script aguarda o intervalo randomico de 
30 a 450 segundo para inciar, isso é necessário para os testes 
não acontecerem em todos os probes ao mesmo momento
'''
sleepTime = randint(1,15)*30
syslog.syslog("sleep "+str(sleepTime))
sleep(sleepTime)

'''
# Configuring Tests IP - Configuração de váriavel em IPv4 e IPv6 para testes 
esses IPs são as Loopbacks dos roteadores de SP4
'''
ipIPv4 = "201.77.113.20"
ipIPv6 = "2804:868:1:0:201:77:113:245"

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

speedtest = {   
        "sumare": "31991", 
        "lencois": "31991", 
        "cirion": "57284"
}

domainsGov = {   
        "correios": "www.correios.com.br", 
        "tjsp": "tjsp.jus.br",
        "tse": "tse.jus.br",
        "inss": "www.meu.inss.gov.br",
        "gov-br": "www.gov.br",
        "nfe": "www.nfe.fazenda.gov.br",
        "caixa": "caixa.gov.br",
        "ecnh": "www.e-cnhsp.sp.gov.br",
        "bb": "www.bb.com.br"
}

def dns():
    # Testes de DNS - Faz o teste usando o DIG utilizando os DNSs autoconfigurados na problem em /etc/resolv.conf

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


def ipv4():
    # Realiza testes de IPv4 - Se esta atingivel, latencia jitter e Loss

    command="ping -4 -i 1 -n -q -c 5 "+ipIPv4
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
        status = 'DOWN'
    else:
        #Geting Average time (latency)
        resLatency = float(resPing[3].split("/")[1])
                            
        #Geting Jitter
        resJitter = float(resPing[3].split("/")[3])

        #Getting Connection
        status = 'UP'

    keys = {"ipv4_latency": resLatency, "ipv4_jitter": resJitter, "ipv4_loss": resLoss, "ipv4_status": status}

    for key, value in keys.items():
        command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
        #print (command)
        syslog.syslog(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def ipv6():
    # Realiza testes de IPv6 - Se esta atingivel, latencia jitter e Loss
    command="ping -6 -i 1 -n -q -c 5 "+ipIPv6
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
        status = 'DOWN'
    else:
        #Geting Average time (latency)
        resLatency = float(resPing[3].split("/")[1])
                            
        #Geting Jitter
        resJitter = float(resPing[3].split("/")[3])

        #Getting Connection
        status = 'UP'

    keys = {"ipv6_latency": resLatency, "ipv6_jitter": resJitter, "ipv6_loss": resLoss, "ipv6_status": status}

    for key, value in keys.items():
        command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
        #print (command)
        syslog.syslog(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
def fragmentation():
    # Realiza os testes de fragmentação, confirma se um pacote pode ser fragmentado, o testes é feito da probe até o seu gateway o BRAS

    # Getting Gateway (ip confirmado pelo BRAS)
    commandIp="route -n | grep '^0\.0\.0\.0' | awk '{print $2}'"
    IP = getoutput(commandIp)

    command = "ping -4 -i 1 -n -q -c 5 -s 1800 "+IP
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
        status = 'DOWN'
    else:
        #Getting Connection
        status = 'UP'

    keys = {"fragmentation_loss": resLoss, "fragmentation_status": status}

    for key, value in keys.items():
        command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
        #print (command)
        syslog.syslog(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def icmp():
    # realiza o teste de ping icmp para destinos informados na lista [domains]

    count = 0

    for URL in domains.values():
        service = list(domains.keys())[count]
        #print (URL)

        command="ping -4 -i 1 -n -q -c 5 "+URL
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
    '''
    # Reliza o testes de abertura da pagina e devolve o valor em milesegundos do tempo de load da pagina
    # Paginas configuradas na lista [domains]
    '''

    count = 0

    #curl -s -o /dev/null -w "Tempo de conexão: %{time_connect}s\nTempo total: %{time_total}s\n" google.com
    #curl -s -o /dev/null -w "%{time_total}s\n" google.com
    for URL in domains.values():
        service = list(domains.keys())[count]
        #print (URL)

        command = "curl -s -4 -o /dev/null -w '%{time_total}s\n' "+URL
        loading_time = getoutput(command)
        loading_time = loading_time.removesuffix('s') 
        f_loading_time = float(loading_time)
        ms_loading_time = f_loading_time *1000

        resWeb = "{:.2f}".format(ms_loading_time)

        keys = {service+"_web_latency": resWeb}

        for key, value in keys.items():
            command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
            #print (command)
            syslog.syslog(command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        count = count+1


def webpagesGov():
    '''
    # Reliza o testes de abertura da pagina do GOVERNO e devolve o valor em milesegundos do tempo de load da pagina
    # Paginas configuradas na lista [domainsGov]
    '''

    count = 0


    for URL in domainsGov.values():
        service = list(domainsGov.keys())[count]
        #print (URL)

        command = "curl -s -4 -o /dev/null -w '%{time_total}s\n' "+URL
        loading_time = getoutput(command)
        loading_time = loading_time.removesuffix('s') 
        f_loading_time = float(loading_time)
        ms_loading_time = f_loading_time *1000
    
        resWeb = "{:.2f}".format(ms_loading_time)

        keys = {service+"_web_latency": resWeb}

        for key, value in keys.items():
            command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
            #print (command)
            syslog.syslog(command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        count = count+1

def speedTest():
    '''
    Realiza o testes de speed test em um servidor por vez, de maneira randomica 
    tilizando o speedtext_cli e tras as informações de download upload latencia e jitter
    '''
    chaves = list(speedtest.keys())
    chave_aleatoria = random.choice(chaves)
    ST = speedtest[chave_aleatoria]

    #print (ST)
    service = chave_aleatoria
    command= f"speedtest --accept-license --accept-gdpr -s {ST} --format=json"
    resSpeedtest = getoutput(command)
    JresSpeedtest = json.loads(resSpeedtest)
    StDownload = JresSpeedtest['download']['bandwidth']/125000
    StUpload = JresSpeedtest['upload']['bandwidth']/125000
    StJitter = JresSpeedtest ['ping']['jitter']
    StLatency = JresSpeedtest ['ping']['latency']
    keys = {service+"_st_latency": StLatency, service+"_st_download": StDownload, service+"_st_upload": StUpload, service+"_st_jitter": StJitter, "st_server": service,
    "geral_st_latency": StLatency, "geral_st_download": StDownload, "geral_st_upload": StUpload, "geral_st_jitter": StJitter}
    for key, value in keys.items():
        command = f"zabbix_sender -z {zabbix} -s {host} -k {key} -o {value}"
        #print (command)
        syslog.syslog(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#def mtr():
    # mtr -4 -n -r -c3 -w -b -p -j google.com
    # mtr -4 -n -r -c3 -w -b google.com

    # apenas resultados
    # mtr -4 -n -r -c1 -w -b -p google.com

dns()
ipv4()
ipv6()
fragmentation()
speedTest()
icmp()
webpages()
webpagesGov()
