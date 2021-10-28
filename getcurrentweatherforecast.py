#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 13:46:21 2020

@author: pugsley
"""
import sys
import time
import logging
import logging.handlers
import requests


# Get current weather conditions for our house 39.110992, -76.983083 lat lon
# First try, use National Weather Service
nwsurl = 'https://api.weather.gov/points/39.1110,-76.9831'
here = requests.get(nwsurl)
if here.status_code != 200: # Badness
    # syslogger.error
    print('{} GET'.format(here.status_code))
    sys.exit(here.status_code)
else:
    hd = here.json(); furl = hd['properties']['forecast'] # URL to get the forecast
    time.sleep(1) # If we ask too quickly we get a 500 error
    now = requests.get(furl)
    if now.status_code != 200: # Badness
        # syslogger.error
        print('{} GET'.format(now.status_code))
        sys.exit(now.status_code)
    else:    
        wd = now.json()
        temperature = wd['properties']['periods'][0]['temperature']
        print('Local temp forecast {}'.format(temperature))
        



