#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 13:46:21 2020

@author: pugsley
"""
import sys
import logging
import logging.handlers
import requests

# Set up a file logger
logging.basicConfig(filename='kgai.log',level=logging.INFO)

# Set up a syslog logger, using the standard syslog format
syslogger = logging.getLogger('Weather')
handler = logging.handlers.SysLogHandler(address = '/dev/log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('getcurrentweather[%(process)d]: %(levelname)s: %(message)s')
handler.setFormatter(formatter)
syslogger.addHandler(handler)


def writelog(datastr):
    logging.info(datastr) # Add data to user file... no time unless we write it
    syslogger.info(datastr) # Add data to syslog file, with automatic time stamp

# Get current weather conditions for our house 39.110992, -76.983083 lat lon
# First try, use National Weather Service
nwsurl = 'https://api.weather.gov/stations/KGAI/observations/latest'
here = requests.get(nwsurl)
if here.status_code != 200: # Badness
    # syslogger.error
    print('{} GET'.format(here.status_code))
    sys.exit(here.status_code)
else:
    hd = here.json(); 
    temperature = hd['properties']['temperature']['value']*(9/5)+32
    humidity = hd['properties']['relativeHumidity']['value']
    timestr = hd['properties']['timestamp']
    print('(KGAI) {}, {}F, {}%'.format(timestr,temperature,humidity))
        



