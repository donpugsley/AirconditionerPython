#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 22:31:48 2020

@author: pugsley
"""
# Get current temp and humidity from wirelesstags

import sys
import requests
import xmltodict

URL = 'https://my.wirelesstag.net/ethAccount.asmx/SignInEx'
PARAMS = {"email":'XXXXXX', "password":'XXXXXX'}
req = requests.get(url=URL, params=PARAMS)
if req.status_code != 200: # Badness
    print('{} GET'.format(req.status_code))
    sys.exit(req.status_code)
jar = req.cookies # Save auth cookie for use in following requests
        
URL = 'https://my.wirelesstag.net/ethAccount.asmx/GetTagManagers'
tm = requests.get(url=URL,cookies=jar)
if tm.status_code != 200: # Badness
    print('{} GET'.format(tm.status_code))
    sys.exit(tm.status_code)
tmdata = xmltodict.parse(tm.text)
mytagmac = tmdata['ArrayOfTagManagerEntry']['TagManagerEntry']['mac']

URL = 'https://my.wirelesstag.net/ethAccount.asmx/SelectTagManager'
stm = requests.get(url=URL,cookies=jar,params={"mac":mytagmac})
if stm.status_code != 200: # Badness
    print('{} GET'.format(stm.status_code))
    sys.exit(stm.status_code)
    
URL = 'https://my.wirelesstag.net/ethClient.asmx/GetTrends'
data = requests.get(url=URL,cookies=jar,params={"allTagManagers":"true"})
if data.status_code != 200: # Badness
    print('{} GET'.format(data.status_code))
    sys.exit(data.status_code)
    
dd = xmltodict.parse(data.text)

URL = 'https://my.wirelesstag.net/ethClient.asmx/SignOut'
so = requests.get(url=URL,cookies=jar)
if so.status_code != 200: # Badness
    print('{} GET'.format(so.status_code))
    sys.exit(so.status_code)

# Format output for logging
outstr=''
for tag in dd['TrendReply']['trends']['RecentTrend']:
    degf = float(tag['temperature']['double'][-1])*(9/5)+32
    rhum = float(tag['rh']['float'][-1])
    name = tag['name']
    outstr = outstr+'{}: {:.1f} F, {:.1f} % RH, '.format(name,degf,rhum)

print(outstr)
