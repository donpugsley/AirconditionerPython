#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 13:31:43 2020

@author: pugsley
"""

# Plot Carrier A/C data logged with infinitude-syslog.py
# Eventually add Infinitude data to plots

# Data is in syslog... lets try getting it from there

# Follow code:
# import time
# def follow(syslog_file):
#     syslog_file.seek(0,2) # Go to the end of the file
#     while True:
#         line = syslog_file.readline()
#         if not line:
#             time.sleep(0.1) # Sleep briefly
#             continue
#         yield line

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import fileinput
import seaborn as sns

# First get our input file name
if len(sys.argv) > 1:
    infilename = sys.argv[1]
else:
    infilename = '/var/log/syslog'  
    
t=[]; zone=[]; hsp=[]; rt=[]; csp=[]; rh=[]; fan=[]; damper=[]; 
ops=[]; cfg=[]; mode=[]; zn0=[]; zn1=[]; zn2=[]; zc0=[]; zc1=[]; zc2=[]; zh0=[];
zh1=[]; zh2=[]; zr0=[]; zr1=[]; zr2=[]; zl0=[]; zl1=[]; zl2=[]; ze0=[]; ze1=[]; ze2=[];
zu0=[]; zu1=[]; zu2=[]; zf0=[]; zf1=[]; zf2=[]; zd0=[]; zd1=[]; zd2=[];         

# Sep 20 13:29:21 Ubuntu-EP45-UD3P infinitude-syslog[32275]: INFO: 
#  2020-09-20T14:02:12-05:00 <living room> temp 66.0 < 67.0 < 78.0, RH 48%,
#  fan off, damper 1 (0 is closed)'
# Old Format...
# m=re.match(r'.*INFO: (.*)-05:00 <(.*?)> temp (.*?) < (.*?) < (.*?), RH (.*?)%, fan (.*), damper (\d+) ', line)
# if m!=None: # Old format line 
#     time = m.group(1)
#     t.append(pd.to_datetime(time))
#     zone.append(str(m.group(2)))
#     hsp.append(float(m.group(3)))
#     rt.append(float(m.group(4)))
#     csp.append(float(m.group(5)))
#     rh.append(float(m.group(6)))
#     fan.append(str(m.group(7)))
#     dampervalue = float(m.group(8))
#     damper.append(dampervalue)
#     df = pd.DataFrame({'Time':t, 'Zone':zone, 'HSP':hsp, 'Temp':rt,\
#                        'CSP':csp, 'RH':rh, 'Fan':fan, 'Damper':damper})
#
# 2020-09-21T13:48:13-05:00: ops idle, cfg heatcool, mode gasheat, 
# z 2nd floor/living room/master bedroom, zcon idle/idle/idle, 
# zhrc 62.0<66.0<67.0/71.0<67.0<68.0/77.0<78.0<71.0, zen on/on/on, 
# zhum 50/50/50, zfan off/off/low, zdamp 0/0/15

f = open(infilename, 'r'); 
for line in f: # fileinput.input():
    n=re.match(r'.*INFO: (.*)-05:00: ops (.*?), cfg (.*?), mode (.*?), z (.*?)/(.*?)/(.*?), zcon (.*?)/(.*?)/(.*?), zhrc (.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?), zen (.*?)/(.*?)/(.*?), zhum (.*?)/(.*?)/(.*?), zfan (.*?)/(.*?)/(.*?), zdamp (\d+)/(\d+)/(\d+)', line)
    if n!=None: # new format
        timestr=n.group(1)
        t.append(pd.to_datetime(timestr))
        ops.append(str(n.group(2)))
        cfg.append(str(n.group(3)))
        mode.append(str(n.group(4)))
        zn0.append(str(n.group(5))); zn1.append(str(n.group(6))); zn2.append(str(n.group(7)))
        zc0.append(str(n.group(8))); zc1.append(str(n.group(9))); zc2.append(str(n.group(10)))
        zh0.append(float(n.group(11))); zr0.append(float(n.group(12))); zl0.append(float(n.group(13)))
        zh1.append(float(n.group(14))); zr1.append(float(n.group(15))); zl1.append(float(n.group(16)))
        zh2.append(float(n.group(17))); zr2.append(float(n.group(18))); zl2.append(float(n.group(19)))
        ze0.append(str(n.group(20))); ze1.append(str(n.group(21))); ze2.append(str(n.group(22)))
        zu0.append(float(n.group(23))); zu1.append(float(n.group(24))); zu2.append(float(n.group(25)))
        zf0.append(str(n.group(26))); zf1.append(str(n.group(27))); zf2.append(str(n.group(28)))
        zd0.append(float(n.group(29))); zd1.append(float(n.group(30))); zd2.append(float(n.group(31)))

# Now we have all the data...
f.close()

df = pd.DataFrame({'Time':t,\
                   'ops':ops,\
                   'cfg':cfg,\
                   'mode':mode,\
                   'zn0':zn0,\
                   'zn1':zn1,\
                   'zn2':zn2,\
                   'zc0':zc0,\
                   'zc1':zc1,\
                   'zc2':zc2,\
                   'zh0':zh0,\
                   'zh1':zh1,\
                   'zh2':zh2,\
                   'zr0':zr0,\
                   'zr1':zr1,\
                   'zr2':zr2,\
                   'zl0':zl0,\
                   'zl1':zl1,\
                   'zl2':zl2,\
                   'ze0':ze0,\
                   'ze1':ze1,\
                   'ze2':ze2,\
                   'zu0':zu0,\
                   'zu1':zu1,\
                   'zu2':zu2,\
                   'zf0':zf0,\
                   'zf1':zf1,\
                   'zf2':zf2,\
                   'zd0':zd0,\
                   'zd1':zd1,\
                   'zd2':zd2\
})

# Set the time column as the index
df.set_index('Time', inplace=True)
    
# Important stuff
# cfg is heat, cool, or heatcool
# mode is off, gasheat, or ??
# zc is zoneconditioning= idle, active_heat, active_cool
# zu is humidity
# zh is htsp
# zr is realtime temp
# zl is clsp
# zf is fan off/low/??
# zd is damper 0..15, 0 is closed
# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})
temps = ['zr0', 'zr1', 'zr2']
axes = df[temps].plot(marker='.', alpha=0.5, linestyle='None')
for ax in axes:
    ax.set_ylabel('Temperature')
    ax.set_xlabel("Time"); 

plt.show()
