#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on Sun Sep 20 13:46:21 2020

@author: pugsley

Collect and save Carrier A/C system status to a file, using an Infinitude
server to get Carrier A/C data; the wifi thermostat use Infinitude as a 
proxy server on the way to the Carrier host.  

"""
import sys
import logging
import logging.handlers
import requests
from time import gmtime, strftime
import xmltodict
import numpy as np
from subprocess import call

# Location of Infinitude server - running on Synology inside Docker container
INFINITUDE_HOST = "192.168.1.202"
INFINITUDE_PORT = "3000"

# Set up a file logger
logging.basicConfig(filename='homedata.log',level=logging.INFO)

# # Set up a syslog logger, using the standard syslog format
# syslogger = logging.getLogger('Weather')
# handler = logging.handlers.SysLogHandler(address = '/dev/log')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('getcurrentweather[%(process)d]: %(levelname)s: %(message)s')
# handler.setFormatter(formatter)
# syslogger.addHandler(handler)

def writelog(datastr):
    logging.info(datastr) # Add data to user file... no time unless we write it
    #    syslogger.info(datastr) # Add data to syslog file, with automatic time stamp


def geturljson(url):
    """Return JSON dict from the given URL"""
    here = requests.get(url)
    if here.status_code != 200: # Badness
        print('{} GET {}'.format(here.status_code,url))
        return None
    else:
        return (here.json()) 

def getlocalweather(): # National Weather Service station KGAI is Montgomery County Airpark
    """Return latest temperature (F), humidity (%), and time for KGAI station"""
    # Set missing-data values to return on GET failure
    KGAItemperature = np.nan
    KGAIhumidity = np.nan
    KGAItime = strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime())
    hd = geturljson('https://api.weather.gov/stations/KGAI/observations/latest')
    if hd is not None:
        tstr = hd['properties']['temperature']['value']
        if tstr is not None: KGAItemperature = float(tstr)*(9/5)+32
        hstr = hd['properties']['relativeHumidity']['value']
        if hstr is not None: KGAIhumidity = float(hstr)
        KGAItime = hd['properties']['timestamp']
    return (KGAItemperature,KGAIhumidity,KGAItime)

def getwirelesstagdata(): # Get current temp and humidity from home wirelesstags using site API
    """Return latest temp and humidity for all three zones"""
    URL = 'https://my.wirelesstag.net/ethAccount.asmx/SignInEx'
    PARAMS = {"email":'WirelessTag-tt@snkmail.com', "password":''}
    req = requests.get(url=URL, params=PARAMS)
    if req.status_code != 200: # Badness
        print('{} GET'.format(req.status_code))
        # sys.exit(req.status_code)
    jar = req.cookies # Save auth cookie for use in following requests
        
    URL = 'https://my.wirelesstag.net/ethClient.asmx?op=SaveTrendsOption'
    data = requests.get(url=URL,cookies=jar,params={"showRH":"true","showLux":"true"})
    if data.status_code != 200: # Badness
        print('{} GET'.format(data.status_code))
        sys.exit(data.status_code)

    URL = 'https://my.wirelesstag.net/ethClient.asmx/GetTrends'
    data = requests.get(url=URL,cookies=jar,params={"allTagManagers":"true"})
    if data.status_code != 200: # Badness
        print('{} GET'.format(data.status_code))
        sys.exit(data.status_code)
    
    dd = xmltodict.parse(data.text)

    # URL = 'https://my.wirelesstag.net/ethAccount.asmx/SelectTagManager'
    # stm = requests.get(url=URL,cookies=jar,params={"mac":mytagmac1})
    # if stm.status_code != 200: # Badness
    #     print('{} GET'.format(stm.status_code))
    #     sys.exit(stm.status_code)
    # 
    # URL = 'https://my.wirelesstag.net/ethClient.asmx/GetTrends'
    # data = requests.get(url=URL,cookies=jar,params={"allTagManagers":"false"})
    # if data.status_code != 200: # Badness
    #     print('{} GET'.format(data.status_code))
    #     sys.exit(data.status_code)
    # 
    # dd = xmltodict.parse(data.text)

    URL = 'https://my.wirelesstag.net/ethClient.asmx/SignOut'
    so = requests.get(url=URL,cookies=jar)
    if so.status_code != 200: # Badness
        print('{} GET'.format(so.status_code))
        sys.exit(so.status_code)

    # # Format output for logging
    # outstr=''
    # for tag in dd['TrendReply']['trends']['RecentTrend']:
    #     degf = float(tag['temperature']['double'][-1])*(9/5)+32
    #     rhum = float(tag['rh']['float'][-1])
    #     name = tag['name']
    #     outstr = outstr+'{}: {:.1f} F, {:.1f} % RH, '.format(name,degf,rhum)

    return dd['TrendReply']['trends']['RecentTrend']
        
def getACdata(): # Infinitude local network server - its a proxy server
                 # for the WIFI thermostat, so it gets all the A/C data
                 # from the thermostat
    """Return latest data for all home A/C zones"""
    host = INFINITUDE_HOST; port = INFINITUDE_PORT 
    api_root='http://'+host+':'+str(port)+'/api/' # base api url
    url=api_root+'status/' 
    sd = geturljson(url)
    timestr = sd['localTime'][0]
    ops=sd['oprstsmsg'][0]
    cfg=sd['cfgtype'][0]
    mode=sd['mode'][0]
    zc0=sd['zones'][0]['zone'][0]['zoneconditioning'][0]
    zc1=sd['zones'][0]['zone'][1]['zoneconditioning'][0]
    zc2=sd['zones'][0]['zone'][2]['zoneconditioning'][0]
    zf0=sd['zones'][0]['zone'][0]['fan'][0]
    zf1=sd['zones'][0]['zone'][1]['fan'][0]
    zf2=sd['zones'][0]['zone'][2]['fan'][0]
    ze0=sd['zones'][0]['zone'][0]['enabled'][0]
    ze1=sd['zones'][0]['zone'][1]['enabled'][0]
    ze2=sd['zones'][0]['zone'][2]['enabled'][0]
    zh0=sd['zones'][0]['zone'][0]['htsp'][0]
    zh1=sd['zones'][0]['zone'][1]['htsp'][0]
    zh2=sd['zones'][0]['zone'][2]['htsp'][0]
    zr0=sd['zones'][0]['zone'][0]['rt'][0]
    zr1=sd['zones'][0]['zone'][1]['rt'][0]
    zr2=sd['zones'][0]['zone'][2]['rt'][0]
    zu0=sd['zones'][0]['zone'][0]['rh'][0]
    zu1=sd['zones'][0]['zone'][1]['rh'][0]
    zu2=sd['zones'][0]['zone'][2]['rh'][0]
    zl0=sd['zones'][0]['zone'][0]['clsp'][0]
    zl1=sd['zones'][0]['zone'][1]['clsp'][0]
    zl2=sd['zones'][0]['zone'][2]['clsp'][0]
    zd0=sd['zones'][0]['zone'][0]['damperposition'][0]
    zd1=sd['zones'][0]['zone'][1]['damperposition'][0]
    zd2=sd['zones'][0]['zone'][2]['damperposition'][0]
    zn0=sd['zones'][0]['zone'][0]['name'][0]
    zn1=sd['zones'][0]['zone'][1]['name'][0]
    zn2=sd['zones'][0]['zone'][2]['name'][0]
    return (timestr,ops,cfg,mode,zn0,zn1,zn2,zc0,zc1,zc2,\
            zh0,zh1,zh2,zr0,zr1,zr2,zl0,zl1,zl2,ze0,ze1,ze2,\
            zu0,zu1,zu2,zf0,zf1,zf2,zd0,zd1,zd2)

(outsidetemperature,outsidehumidity,outsidetime) = getlocalweather()

(ACtimestr,ops,cfg,mode,zn0,zn1,zn2,zc0,zc1,zc2,\
 zh0,zh1,zh2,zr0,zr1,zr2,zl0,zl1,zl2,ze0,ze1,ze2,\
 zu0,zu1,zu2,zf0,zf1,zf2,zd0,zd1,zd2) = getACdata()

wtd = getwirelesstagdata()
tagstr=''
for tag in wtd:
    degf = float(tag['temperature']['double'][-1])*(9/5)+32
    if tag.get('rh')==None: # Non-ALS tags!
        rhum = 0.0;
    else:
        rhum = float(tag['rh']['float'][-1])
    name = tag['name']
    tagstr = tagstr+'{}: {:.1f} F, {:.1f} % RH, '.format(name,degf,rhum)

nowstr = strftime("%Y-%m-%dT%H:%M:%S-05:00", gmtime())

if outsidetemperature is None: outsidetemperature = 'None'
    
writelog('{}: ops {}, cfg {}, mode {}, z {}/{}/{}, zcon {}/{}/{}, zhrc {}<{}<{}/{}<{}<{}/{}<{}<{}, zen {}/{}/{}, zhum {}/{}/{}, zfan {}/{}/{}, zdamp {}/{}/{}, outside {}:{:.1f}/{:.1f}, TAGS: {}'.format\
        (nowstr,ops,cfg,mode,zn0,zn1,zn2,zc0,zc1,zc2,zh0,zr0,zl0,zh1,zr1,zl1,zh2,zr2,zl2,ze0,ze1,ze2,zu0,zu1,zu2,zf0,zf1,zf2,zd0,zd1,zd2,outsidetime,outsidetemperature,outsidehumidity,tagstr))

call("/home/pugsley/anaconda3/bin/python" + " /home/pugsley/plot-homelogger-data.py", shell=True)
