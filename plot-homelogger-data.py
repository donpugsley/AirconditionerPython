#!/usr/bin/env python3

import sys, re, datetime, dateutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import array
import itertools

def flatten(list2d):
    flatlist = list(itertools.chain.from_iterable(list2d))
    return (flatlist)

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

# These are the tags that will be used and plotted
tags = ['Master Bedroom', 'Garage', 'Guest Room', "Cristopher's Room", "Morgan's Room", 'Upstairs Bathroom', 'Crawlspace']
zone = []

print("Reading...")

# Whole line regexp for reference
linepattern = r'.*INFO:root:(.*)-\d\d:\d\d: ops (.*?), cfg (.*?), mode (.*?), z (.*?)/(.*?)/(.*?), zcon (.*?)/(.*?)/(.*?), zhrc (.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?), zen (.*?)/(.*?)/(.*?), zhum (.*?)/(.*?)/(.*?), zfan (.*?)/(.*?)/(.*?), zdamp (\d+)/(\d+)/(\d+), outside (.*?)[+-]\d\d:\d\d:(.*?)/(.*?), TAGS: (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, (.*?): (.*?) F, (.*?) % RH, '

f = open(infilename, encoding='utf-8')
wholefile = f.read()
f.close()

# Extract AC (Infinitude) data 
acpattern = r'.*INFO:root:(.*)-\d\d:\d\d: ops (.*?), cfg (.*?), mode (.*?), z (.*?)/(.*?)/(.*?), zcon (.*?)/(.*?)/(.*?), zhrc (.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?)/(.*?)<(.*?)<(.*?), zen (.*?)/(.*?)/(.*?), zhum (.*?)/(.*?)/(.*?), zfan (.*?)/(.*?)/(.*?), zdamp (\d+)/(\d+)/(\d+), outside (.*?)[+-]\d\d:\d\d:(.*?)/(.*?), '
ac = re.findall(acpattern, wholefile)

# Convert time string to local 
t = [dateutil.parser.isoparse(ac[i][0]).astimezone(local_tz)-datetime.timedelta(hours=5)for i in range(len(ac))]

ops = flatten(array(ac)[0:, 1:2].tolist()); cfg = flatten(array(ac)[0:, 2:3].tolist()); mode = flatten(array(ac)[0:, 3:4].tolist())
zn0 = flatten(array(ac)[0:, 4:5].tolist()); zn1 = flatten(array(ac)[0:, 5:6].tolist()); zn2 = flatten(array(ac)[0:, 6:7].tolist())
zc0 = flatten(array(ac)[0:, 7:8].tolist()); zc1 = flatten(array(ac)[0:, 8:9].tolist()); zc2 = flatten(array(ac)[0:, 9:10].tolist())
zh0 = flatten(array(ac)[0:, 10:11].tolist()); zr0 = flatten(array(ac)[0:, 11:12].tolist()); zl0 = flatten(array(ac)[0:, 12:13].tolist())
zh1 = flatten(array(ac)[0:, 13:14].tolist()); zr1 = flatten(array(ac)[0:, 14:15].tolist()); zl1 = flatten(array(ac)[0:, 15:16].tolist())
zh2 = flatten(array(ac)[0:, 16:17].tolist()); zr2 = flatten(array(ac)[0:, 17:18].tolist()); zl2 = flatten(array(ac)[0:, 18:19].tolist())
ze0 = flatten(array(ac)[0:, 19:20].tolist()); ze1 = flatten(array(ac)[0:, 20:21].tolist()); ze2 = flatten(array(ac)[0:, 21:22].tolist())
zu0 = flatten(array(ac)[0:, 22:23].tolist()); zu1 = flatten(array(ac)[0:, 23:24].tolist()); zu2 = flatten(array(ac)[0:, 24:25].tolist())
zf0 = flatten(array(ac)[0:, 25:26].tolist()); zf1 = flatten(array(ac)[0:, 26:27].tolist()); zf2 = flatten(array(ac)[0:, 27:28].tolist())
zd0 = flatten(array(ac)[0:, 28:29].tolist()); zd1 = flatten(array(ac)[0:, 29:30].tolist()); zd2 = flatten(array(ac)[0:, 30:31].tolist())
KGAItemp = flatten(array(ac)[0:, 31:32].tolist()); KGAIhum = flatten(array(ac)[0:, 32:33].tolist())


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
                   'KGAItemp':KGAItemp, 'KGAIhum':KGAIhum})
    
# Set the time column as the index
df.set_index('Time', inplace=True)

#N = len(df.columns) # Make all tag data this length for concat

timeandtag = r'.*INFO:root:(.*)-\d\d:\d\d: ops .* TAGS:'
for index,tag in enumerate(tags):
    pattern = timeandtag + '.*' + tag + ': (.*?) F, (.*?) % RH,'
    wt = array(re.findall(pattern,wholefile))
    # Convert values as needed
    tt = [dateutil.parser.isoparse(wt[i][0]).astimezone(local_tz)-datetime.timedelta(hours=5)for i in range(len(wt))]
    
    tdf = pd.DataFrame({'Time':tt,tag+'temp':flatten(array(wt)[0:, 1:2].tolist()),tag+'hum':flatten(array(wt)[0:, 2:3].tolist())})
    tdf.set_index('Time', inplace=True)
    
    df = df.merge(tdf, on='Time', how='inner')

# Convert strings to numbers 
df = df.apply(pd.to_numeric,errors='ignore')

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

# Temperature plot window
fig, (ax1, ax2, ax3) = plt.subplots(3,sharex=True)
fig.suptitle('CFG: {} Now: {} Hall:{}/LR:{}/MBR:{} Fan {}/{}/{} Damper {}/{}/{} (0 is closed)'.format\
             (cfg[-1],mode[-1],zc0[-1],zc1[-1],zc2[-1],zf0[-1],zf1[-1],zf2[-1],zd0[-1],zd1[-1],zd2[-1]))

# Make sure our plots are tz-aware    
ax1.xaxis_date(tz=local_tzname)    
ax2.xaxis_date(tz=local_tzname)    
ax3.xaxis_date(tz=local_tzname)    

# Zone: 2nd floor, Tags: Guest Room, Upstairs Bathroom, Cristopher's Room
temps = ['zr0', 'Guest Roomtemp', 'Upstairs Bathroomtemp',"Cristopher's Roomtemp"] 
ax1.plot(df[temps],marker='.')
ax1.fill_between(df.index,[x-5 for x in df['zh0']],df['zh0'],alpha=0.2,color='red')
ax1.fill_between(df.index,[x+5 for x in df['zl0']],df['zl0'],alpha=0.2,color='blue')
ax1.set_ylabel('Temperature')
ax1.title.set_text('2nd Floor Hall Thermostat Zone')
ax1.legend(['Hall Thermostat {:.0f}'.format(df['zr0'][-1]),\
            'Guest Room Tag {:.0f}'.format(df['Guest Roomtemp'][-1]),\
            "Upstairs Bathroom Tag {:.0f}".format(df['Upstairs Bathroomtemp'][-1]),\
            "Chris's Room Tag {:.0f}".format(df["Cristopher's Roomtemp"][-1])],\
           loc='lower left')
for item in cools1:
    ax1.axvspan(item[0], item[1], alpha=0.1, color='blue')
for item in heats1:
    ax1.axvspan(item[0], item[1], alpha=0.1, color='red')

# Zone: Living room, Tags: Crawlspace, Garage
temps = ['zr1', 'Crawlspacetemp', 'Garagetemp']
ax2.plot(df[temps],marker='.')
ax2.fill_between(df.index,[x-5 for x in df['zh1']],df['zh1'],alpha=0.2,color='red')
ax2.fill_between(df.index,[x+5 for x in df['zl1']],df['zl1'],alpha=0.2,color='blue')
ax2.set_ylabel('Temperature')
ax2.title.set_text('Living Room Thermostat Zone')
ax2.legend(['Living Room Thermostat {:.0f}'.format(df['zr1'][-1]),\
            'Crawlspace {:.0f}'.format(df['Crawlspacetemp'][-1]),\
            'Garage Tag {:.0f}'.format(df['Garagetemp'][-1])],\
            loc='lower left')
for item in cools2:
    ax2.axvspan(item[0], item[1], alpha=0.1, color='blue')
for item in heats2:
    ax2.axvspan(item[0], item[1], alpha=0.1, color='red')

# Zone: Master Bedroom, Tags: Morgan's Room, Master Bedroom
temps = ['zr2', "Morgan's Roomtemp", 'Master Bedroomtemp']
ax3.plot(df[temps],marker='.')
ax3.fill_between(df.index,[x-5 for x in df['zh2']],df['zh2'],alpha=0.2,color='red')
ax3.fill_between(df.index,[x+5 for x in df['zl2']],df['zl2'],alpha=0.2,color='blue')
ax3.set_ylabel('Temperature')
ax3.set_xlabel("Time")
ax3.title.set_text('Master Bedroom Thermostat Zone')
ax3.legend(['Master Bedroom Thermostat {:.0f}'.format(df['zr2'][-1]),\
            "Morgan's Room Tag {:.0f}".format(df["Morgan's Roomtemp"][-1]),\
            'Master Bedroom Tag {:.0f}'.format(df['Master Bedroomtemp'][-1])],\
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
hums = ['zu0', 'zu1', 'zu2','Master Bedroomhum', "Morgan's Roomhum", "Cristopher's Roomhum", 'Upstairs Bathroomhum', 'Garagehum', 'Guest Roomhum', 'Crawlspacehum']
ax.plot(df[hums],marker='.')
ax.set_ylabel('% Humidity')
ax.set_xlabel("Time")
ax.title.set_text('Humidity vs Time for all sensors')
ax.legend(['2nd Floor Hall Thermostat {:.0f}'.format(df['zu0'][-1]),\
            'Living Room Thermostat {:.0f}'.format(df['zu1'][-1]),\
            'Master Bedroom Thermostat {:.0f}'.format(df['zu2'][-1]),\
            "Master Bedroom Tag {:.0f}".format(df['Master Bedroomhum'][-1]),\
            "Morgan's Room Tag {:.0f}".format(df["Morgan's Roomhum"][-1]),\
            "Christopher's Room Tag {:.0f}".format(df["Cristopher's Roomhum"][-1]),\
            "Upstairs Bathroom Tag {:.0f}".format(df['Upstairs Bathroomhum'][-1]),\
            "Garage Tag {:.0f}".format(df['Garagehum'][-1]),
            "Guest Room Tag {:.0f}".format(df['Guest Roomhum'][-1]),\
            "Crawlspace Tag {:.0f}".format(df['Crawlspacehum'][-1])],\
          loc='lower left')
plt.savefig('hum.jpg', bbox_inches='tight')

if INTERACTIVE:
    plt.show()
