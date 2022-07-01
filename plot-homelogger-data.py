#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 13:31:43 2020

@author: pugsley

Plot Carrier A/C data logged with infinitude-syslog.py, home
temperature and humidity from wirelesstags, and outside temperature
and humidity from NWS

WirelessTags as of 8/18/2021 are
# 0 Outdoors
# 1 Master Bedroom
# 2 Morgan's Room
# 3 Cristopher's Room
# 4 Upstairs Bathroom
# 5 Chris Window
# 6 Garage
# 7 Guest Room
# 8 Morgans Door
# 9 Crawlspace
    
"""

import sys, re, datetime, dateutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get the local timezone for use in later corrections
now = datetime.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)

if len(sys.argv) > 1:
    hours = float(sys.argv[1])
    INTERACTIVE = True
else:
    hours = 8
    INTERACTIVE = False
    
infilename = '/home/pugsley/code/AC/homedata.log'  
    
t=[]; zone=[]; hsp=[]; rt=[]; csp=[]; rh=[]; fan=[]; damper=[]; 
ops=[]; cfg=[]; mode=[]; zn0=[]; zn1=[]; zn2=[]; zc0=[]; zc1=[]; zc2=[]; zh0=[];
zh1=[]; zh2=[]; zr0=[]; zr1=[]; zr2=[]; zl0=[]; zl1=[]; zl2=[]; ze0=[]; ze1=[]; ze2=[];
zu0=[]; zu1=[]; zu2=[]; zf0=[]; zf1=[]; zf2=[]; zd0=[]; zd1=[]; zd2=[];         
KGAItime=[]; KGAItemp=[]; KGAIhum=[];
wt0n=[]; wt0t=[]; wt0h=[];
wt1n=[]; wt1t=[]; wt1h=[]; wt2n=[]; wt2t=[]; wt2h=[];
wt3n=[]; wt3t=[]; wt3h=[]; wt4n=[]; wt4t=[]; wt4h=[];
wt5n=[]; wt5t=[]; wt5h=[]; wt6n=[]; wt6t=[]; wt6h=[];
wt7n=[]; wt7t=[]; wt7h=[]; wt8n=[]; wt8t=[]; wt8h=[];
wt9n=[]; wt9t=[]; wt9h=[]; wt10n=[]; wt10t=[]; wt10h=[];
wt11n=[]; wt11t=[]; wt11h=[]; wt12n=[]; wt12t=[]; wt12h=[];

# INFO:root:2021-08-14T13:27:07-05:00: ops idle, cfg heatcool, mode
# off, z 2nd floor/living room/master bedroom, zcon idle/idle/idle,
# zhrc 66.0<75.0<75.0/67.0<73.0<75.0/64.0<71.0<75.0, zen on/on/on,
# zhum 65/65/65, zfan high/off/high, zdamp 15/0/15, outside
# 2021-08-14T12:56:00+00:00:79.0/76.8, TAGS: Outdoors: 80.2 F, 72.3 %
# RH, Master Bedroom: 72.3 F, 52.0 % RH, Morgan's Room: 71.5 F, 57.3 %
# RH, Cristopher's Room: 74.6 F, 53.6 % RH, Upstairs Bathroom: 74.1 F,
# 62.0 % RH, Chris Window: 74.7 F, 49.6 % RH, Garage: 81.7 F, 52.0 %
# RH, Guest Room: 72.6 F, 57.7 % RH, Morgans Door: 70.3 F, 51.7 % RH,
# Crawlspace: 69.0 F, 63.4 % RH,

# Infinitude timestamps have -5:00 hardcoded in homedatalogger.py...

# This format will return a timestr without the ISO 8601 TZ
restr10tag = r'.*INFO:root:(.*)-\d\d:\d\d: ops (.*?), cfg (.*?), mode (.*?), z (.*?)/(.*?)/(.*?), zcon (.*?)/(.*?)/(.*?), zhrc (.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?), zen (.*?)/(.*?)/(.*?), zhum (.*?)/(.*?)/(.*?), zfan (.*?)/(.*?)/(.*?), zdamp (\d+)/(\d+)/(\d+), outside (.*?)[+-]\d\d:\d\d:(.*?)/(.*?), TAGS: (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, '

# This format will match the full ISO 8601 TZ... just need to avoid the final :
# restr10tag = r'.*INFO:root:(.*): ops (.*?), cfg (.*?), mode (.*?), z (.*?)/(.*?)/(.*?), zcon (.*?)/(.*?)/(.*?), zhrc (.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?), zen (.*?)/(.*?)/(.*?), zhum (.*?)/(.*?)/(.*?), zfan (.*?)/(.*?)/(.*?), zdamp (\d+)/(\d+)/(\d+), outside (.*?)[+-]\d\d:\d\d:(.*?)/(.*?), TAGS: (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, '

print("Reading...")
f = open(infilename, 'r'); 
for linenum,line in enumerate(f): # fileinput.input():
    ldat=re.match(restr10tag, line)
    if ldat != None:        
        timestr=ldat.group(1); 
        thistime = dateutil.parser.isoparse(timestr) # Parse string to get datetime
        thistime = thistime.astimezone(local_tz) # Make TZ-aware as local time
        thistime = thistime - datetime.timedelta(hours=5) # Correct for the hardcoded -5, may break when we go to EDT

        # Collect the data for this line into arrays
        t.append(thistime)
        ops.append(str(ldat.group(2))); cfg.append(str(ldat.group(3))); mode.append(str(ldat.group(4)))
        zn0.append(str(ldat.group(5))); zn1.append(str(ldat.group(6))); zn2.append(str(ldat.group(7)))
        zc0.append(str(ldat.group(8))); zc1.append(str(ldat.group(9))); zc2.append(str(ldat.group(10)))
        zh0.append(float(ldat.group(11))); zr0.append(float(ldat.group(12))); zl0.append(float(ldat.group(13)))
        zh1.append(float(ldat.group(14))); zr1.append(float(ldat.group(15))); zl1.append(float(ldat.group(16)))
        zh2.append(float(ldat.group(17))); zr2.append(float(ldat.group(18))); zl2.append(float(ldat.group(19)))
        ze0.append(str(ldat.group(20))); ze1.append(str(ldat.group(21))); ze2.append(str(ldat.group(22)))
        zu0.append(float(ldat.group(23))); zu1.append(float(ldat.group(24))); zu2.append(float(ldat.group(25)))
        zf0.append(str(ldat.group(26))); zf1.append(str(ldat.group(27))); zf2.append(str(ldat.group(28)))
        zd0.append(float(ldat.group(29))); zd1.append(float(ldat.group(30))); zd2.append(float(ldat.group(31)))
        KGAItemp.append(float(ldat.group(33)));  KGAIhum.append(float(ldat.group(34)));
        wt0n.append(str(ldat.group(35))); wt0t.append(float(ldat.group(36))); wt0h.append(float(ldat.group(37)));
        wt1n.append(str(ldat.group(38))); wt1t.append(float(ldat.group(39))); wt1h.append(float(ldat.group(40)));
        wt2n.append(str(ldat.group(41))); wt2t.append(float(ldat.group(42))); wt2h.append(float(ldat.group(43)));
        wt3n.append(str(ldat.group(44))); wt3t.append(float(ldat.group(45))); wt3h.append(float(ldat.group(46)));
        wt4n.append(str(ldat.group(47))); wt4t.append(float(ldat.group(48))); wt4h.append(float(ldat.group(49)));
        wt5n.append(str(ldat.group(50))); wt5t.append(float(ldat.group(51))); wt5h.append(float(ldat.group(52)));
        wt6n.append(str(ldat.group(53))); wt6t.append(float(ldat.group(54))); wt6h.append(float(ldat.group(55)));
        wt7n.append(str(ldat.group(56))); wt7t.append(float(ldat.group(57))); wt7h.append(float(ldat.group(58)));
        wt8n.append(str(ldat.group(59))); wt8t.append(float(ldat.group(60))); wt8h.append(float(ldat.group(61)));
        wt9n.append(str(ldat.group(62))); wt9t.append(float(ldat.group(63))); wt9h.append(float(ldat.group(64)));
 
    else:
        f.close()
        sys.exit('Error parsing line {}: <{}>'.format(linenum,line))

f.close()

# Put the collected arrays into a dataframe
print("Framing...")
df = pd.DataFrame({'Time':t, 'ops':ops, 'cfg':cfg, 'mode':mode,\
                   'zn0':zn0, 'zn1':zn1, 'zn2':zn2,\
                   'zc0':zc0, 'zc1':zc1, 'zc2':zc2,\
                   'zh0':zh0, 'zh1':zh1, 'zh2':zh2,\
                   'zr0':zr0, 'zr1':zr1, 'zr2':zr2,\
                   'zl0':zl0, 'zl1':zl1, 'zl2':zl2,\
                   'ze0':ze0, 'ze1':ze1, 'ze2':ze2,\
                   'zu0':zu0, 'zu1':zu1, 'zu2':zu2,\
                   'zf0':zf0, 'zf1':zf1, 'zf2':zf2,\
                   'zd0':zd0, 'zd1':zd1, 'zd2':zd2,\
                   'KGAItemp':KGAItemp, 'KGAIhum':KGAIhum,\
                   'outtemp':wt0t, 'outhum':wt0h,\
                   'wt1n':wt1n, 'wt1t':wt1t, 'wt1h':wt1h,\
                   'wt2n':wt2n, 'wt2t':wt2t, 'wt2h':wt2h,\
                   'wt3n':wt3n, 'wt3t':wt3t, 'wt3h':wt3h,\
                   'wt4n':wt4n, 'wt4t':wt4t, 'wt4h':wt4h,\
                   'wt5n':wt5n, 'wt5t':wt5t, 'wt5h':wt5h,\
                   'wt6n':wt6n, 'wt6t':wt6t, 'wt6h':wt6h,\
                   'wt7n':wt7n, 'wt7t':wt7t, 'wt7h':wt7h,\
                   'wt8n':wt8n, 'wt8t':wt8t, 'wt8h':wt8h,\
                   'wt9n':wt9n, 'wt9t':wt9t, 'wt9h':wt9h\
})
outtemp = wt0t; outhum = wt0h;

# Set the time column as the index
df.set_index('Time', inplace=True)

# Ensure we are monotonically increasing
print("Sorting...")
df.sort_index(inplace=True)

# Convert to local time
# Not necessary ... df = df.tz_localize(local_tz)

# We read (and converted!) the entire data file... Cut back to the requested number of hours
now = datetime.datetime.now()
now = now.replace(tzinfo=local_tz)
then = now - datetime.timedelta(hours=hours)

# Debuggering printout... timezones are a pain in the ass
earliest = df.head(1).index
latest = df.tail(1).index
print("Dataset ends {0}, requested {1} to {2}".format\
       (latest.format()[0], str(then), str(now)))

nearnow = min(now,latest)
df = df.loc[ df.index > then ]
#df = df[then:nearnow]  

# Iterate through and find on/off points... we need to color the
# area between each on-off pair.  
def findheatsandcools(df,zone,tz):
    cools = []; heats = []; old = pd.Timestamp(0,tz=tz)
    heatstart = old; coolstart = old; heatstop = old; coolstop = old;
    for sample in df.iterrows():
        if 'active_cool' in sample[1][zone]: # A/C is on
            if coolstart == old: # A/C just turned on
                coolstart = sample[0]
        else: # A/C is off
            if coolstart != old: # A/C just turned off
                coolstop = sample[0]
    
        if coolstart != old and coolstop != old: # We have a pair
            cools.append([coolstart,coolstop])
            coolstart = old; coolstop = old;
    
        if 'active_heat' in sample[1][zone]: # Heat is on
            if heatstart == old: # Heat just turned on
                heatstart = sample[0]
        else: # A/C is off
            if heatstart != old: # Heat just turned off
                heatstop = sample[0]
    
        if heatstart != old and heatstop != old: # We have a pair
            heats.append([heatstart,heatstop])
            heatstart = old; heatstop = old;

    if coolstart != old and coolstop == old: # Still running... add final pair
        coolstop = sample[0]
        cools.append([coolstart,coolstop])

    if heatstart != old and heatstop == old: 
        heatstop = sample[0]
        heats.append([heatstart,heatstop])
        
    return (heats,cools)

(heats1,cools1) = findheatsandcools(df,'zc0',local_tz)
(heats2,cools2) = findheatsandcools(df,'zc1',local_tz)
(heats3,cools3) = findheatsandcools(df,'zc2',local_tz)

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
sns.set(rc={'figure.figsize':(20, 12)})

# Top line has overall status for zone - cfg, mode, zc, zf, zd
# Show blocks for set points - blue for A/C, red for heat
#   Plot zh and below as red, zl and above as blue

# TAGS as of 8/18/2021 are
# 0 Outdoors
# 1 Master Bedroom
# 2 Morgan's Room
# 3 Cristopher's Room
# 4 Upstairs Bathroom
# 5 Chris Window
# 6 Garage
# 7 Guest Room
# 8 Morgans Door
# 9 Crawlspace

# Temperature plot window
fig, (ax1, ax2, ax3) = plt.subplots(3,sharex=True)
fig.suptitle('CFG: {} Now: {} Hall:{}/LR:{}/MBR:{} Fan {}/{}/{} Damper {}/{}/{} (0 is closed)'.format\
             (cfg[-1],mode[-1],zc0[-1],zc1[-1],zc2[-1],zf0[-1],zf1[-1],zf2[-1],zd0[-1],zd1[-1],zd2[-1]))

# Make sure our plots are tz-aware    
ax1.xaxis_date(tz=local_tzname)    
ax2.xaxis_date(tz=local_tzname)    
ax3.xaxis_date(tz=local_tzname)    

# Zone: 2nd floor, tags 7 (Guest), 4 (Bathroom), 3 (Chris' Room) ... 5 Chris Window is OOR
temps = ['zr0', 'wt7t', 'wt4t','wt3t'] # 'outtemp', removed
ax1.plot(df[temps],marker='.')
ax1.fill_between(df.index,[x-5 for x in df['zh0']],df['zh0'],alpha=0.2,color='red')
ax1.fill_between(df.index,[x+5 for x in df['zl0']],df['zl0'],alpha=0.2,color='blue')
ax1.set_ylabel('Temperature')
ax1.title.set_text('2nd Floor Hall Thermostat Zone')
# 'Outside {:.0f}'.format(df['outtemp'][-1]),\
ax1.legend(['Hall Thermostat {:.0f}'.format(df['zr0'][-1]),\
            'Guest Room Tag {:.0f}'.format(df['wt7t'][-1]),\
            "Upstairs Bathroom Tag {:.0f}".format(df['wt4t'][-1]),\
            "Chris's Room Tag {:.0f}".format(df['wt3t'][-1])],\
           loc='lower left')
for item in cools1:
    ax1.axvspan(item[0], item[1], alpha=0.1, color='blue')
for item in heats1:
    ax1.axvspan(item[0], item[1], alpha=0.1, color='red')

# Zone: Living room, tag 9 (Crawlspace), 6 (Garage)
temps = ['zr1', 'wt9t', 'wt6t']
ax2.plot(df[temps],marker='.')
ax2.fill_between(df.index,[x-5 for x in df['zh1']],df['zh1'],alpha=0.2,color='red')
ax2.fill_between(df.index,[x+5 for x in df['zl1']],df['zl1'],alpha=0.2,color='blue')
ax2.set_ylabel('Temperature')
ax2.title.set_text('Living Room Thermostat Zone')
ax2.legend(['Living Room Thermostat {:.0f}'.format(df['zr1'][-1]),\
            'Crawlspace {:.0f}'.format(df['wt9t'][-1]),\
            'Garage Tag {:.0f}'.format(df['wt6t'][-1])],\
            loc='lower left')
for item in cools2:
    ax2.axvspan(item[0], item[1], alpha=0.1, color='blue')
for item in heats2:
    ax2.axvspan(item[0], item[1], alpha=0.1, color='red')

# Zone: Master Bedroom, tags 2 (Morgan) and 1 (MBR)
temps = ['zr2', 'wt2t', 'wt1t']
ax3.plot(df[temps],marker='.')
ax3.fill_between(df.index,[x-5 for x in df['zh2']],df['zh2'],alpha=0.2,color='red')
ax3.fill_between(df.index,[x+5 for x in df['zl2']],df['zl2'],alpha=0.2,color='blue')
ax3.set_ylabel('Temperature')
ax3.set_xlabel("Time")
ax3.title.set_text('Master Bedroom Thermostat Zone')
ax3.legend(['Master Bedroom Thermostat {:.0f}'.format(df['zr2'][-1]),\
            "Morgan's Room Tag {:.0f}".format(df['wt2t'][-1]),\
            'Master Bedroom Tag {:.0f}'.format(df['wt1t'][-1])],\
            loc='lower left')
for item in cools3:
    ax3.axvspan(item[0], item[1], alpha=0.1, color='blue')
for item in heats3:
    ax3.axvspan(item[0], item[1], alpha=0.1, color='red')

plt.savefig('temp.jpg', bbox_inches='tight')


# Humidity plot
fig = plt.figure()
ax = plt.axes()
# Make sure our plot is tz-aware    
ax.xaxis_date(tz=local_tzname)    

plt.title('CFG: {} Now: {} Hall:{}/LR:{}/MBR:{} Fan {}/{}/{} Damper {}/{}/{} (0 is closed)'.format\
             (cfg[-1],mode[-1],zc0[-1],zc1[-1],zc2[-1],zf0[-1],zf1[-1],zf2[-1],zd0[-1],zd1[-1],zd2[-1]))
hums = ['zu0', 'zu1', 'zu2', 'wt1h','wt2h','wt3h','wt4h','wt5h','wt6h','wt7h','wt8h','wt9h']
ax.plot(df[hums],marker='.')
#ax3.fill_between(df.index,[x-5 for x in df['zh2']],df['zh2'],alpha=0.2,color='red')
#ax3.fill_between(df.index,[x+5 for x in df['zl2']],df['zl2'],alpha=0.2,color='blue')
ax.set_ylabel('% Humidity')
ax.set_xlabel("Time")
ax.title.set_text('Humidity vs Time for all sensors')
ax.legend(['2nd Floor Hall Thermostat {:.0f}'.format(df['zu0'][-1]),\
            'Living Room Thermostat {:.0f}'.format(df['zu1'][-1]),\
            'Master Bedroom Thermostat {:.0f}'.format(df['zu2'][-1]),\
            "Master Bedroom Tag {:.0f}".format(df['wt1h'][-1]),\
            "Morgan's Room Tag {:.0f}".format(df['wt2h'][-1]),\
            "Christopher's Room Tag {:.0f}".format(df['wt3h'][-1]),\
            "Upstairs Bathroom Tag {:.0f}".format(df['wt4h'][-1]),\
            "Christopher's Window Tag {:.0f}".format(df['wt5h'][-1]),\
            "Garage Tag {:.0f}".format(df['wt6h'][-1]),
            "Guest Room Tag {:.0f}".format(df['wt7h'][-1]),\
            "Morgan's Door Tag {:.0f}".format(df['wt8h'][-1]),\
            "Crawlspace Tag {:.0f}".format(df['wt9h'][-1])],\
          loc='lower left')
plt.savefig('hum.jpg', bbox_inches='tight')

if INTERACTIVE:
    plt.show()

# TAGS as of 8/18/2021 are
# 0 Outdoors
# 1 Master Bedroom
# 2 Morgan's Room
# 3 Cristopher's Room
# 4 Upstairs Bathroom
# 5 Chris Window
# 6 Garage
# 7 Guest Room
# 8 Morgans Door
# 9 Crawlspace
