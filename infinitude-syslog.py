# Log Carrier A/C system status to a file
# Uses Infinitude server to get Carrier A/C data
# Infinitude is running on Docker with a random port... 

host = '192.168.1.202'
port = 32769

import sys
import logging
import logging.handlers
import requests

# Set up a file logger
logging.basicConfig(filename='infinitude.log',level=logging.INFO)
# logging.info('user file data') # Add data to user file... no time unless we write it

# Set up a syslog logger, using the standard syslog format
syslogger = logging.getLogger('Infinitude')
handler = logging.handlers.SysLogHandler(address = '/dev/log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('infinitude-syslog[%(process)d]: %(levelname)s: %(message)s')
handler.setFormatter(formatter)
syslogger.addHandler(handler)

# syslogger.info('data') # Add data to syslog file, with automatic time stamp

def writelog(datastr):
    logging.info(datastr) # Add data to user file... no time unless we write it
    syslogger.info(datastr) # Add data to syslog file, with automatic time stamp
    
api_root='http://'+host+':'+str(port)+'/api/' # base api url
status_url=api_root+'status/' 

# Get system status
status = requests.get(status_url)
if status.status_code != 200: # Badness
    syslogger.error('{} GET'.format(status.status_code))
    sys.exit(status.status_code)
else:
    sd = status.json()
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
    writelog('{}: ops {}, cfg {}, mode {}, z {}/{}/{}, zcon {}/{}/{}, zhrc {}<{}<{}/{}<{}<{}/{}<{}<{}, zen {}/{}/{}, zhum {}/{}/{}, zfan {}/{}/{}, zdamp {}/{}/{}'.format\
          (timestr,ops,cfg,mode,zn0,zn1,zn2,zc0,zc1,zc2,zh0,zh1,zh2,zr0,zr1,zr2,zl0,zl1,zl2,ze0,ze1,ze2,zu0,zu1,zu2,zf0,zf1,zf2,zd0,zd1,zd2))



# api_root='http://'+host+':'+str(port)+'/api/' # base api url
# zones_url=api_root+'status/zones' # base api url
# time_url=api_root+'status/localTime' # base api url
# status_url=api_root+'status/' 
# cfgtype_url=api_root+'status/cfgtype/' # base api url

# # Get system status
# # status = requests.get(status_url)
# # if status.status_code != 200: # Badness
# #     print('{} GET'.format(status.status_code))
# # else:
# #     print('Status: ' + status.text + '\n') # Lots of stuff here, need to parse

# now = requests.get(time_url)
# if now.status_code != 200: # Badness
#     syslogger.error('{} GET'.format(now.status_code))
#     sys.exit(now.status_code)
# else:
#     timestr = now.json()['localTime']
        
# # cfgtype = requests.get(cfgtype_url)
# # if cfgtype.status_code != 200: # Badness
# #     print('{} GET'.format(cfgtype.status_code))
# # else:
# #     print('Cfg: '+cfgtype.json()['cfgtype'])
        
# zones = requests.get(zones_url)
# if zones.status_code != 200: # Badness
#     syslogger.error('{} GET'.format(zones.status_code))
#     sys.exit(now.status_code)
# else:
#     zd = zones.json(); zd = zd['zones'] 
#     writelog('{} <{}> temp {} < {} < {}, RH {}%, fan {}, damper {} (0 is closed)'.format
#         (timestr,zd['zone'][0]['name'][0],zd['zone'][0]['htsp'][0],
#         zd['zone'][0]['rt'][0],zd['zone'][0]['clsp'][0],
#         zd['zone'][0]['rh'][0],zd['zone'][0]['fan'][0],
#         zd['zone'][0]['damperposition'][0]))
#     writelog('{} <{}> temp {} < {} < {}, RH {}%, fan {}, damper {} (0 is closed)'.format
#         (timestr,zd['zone'][1]['name'][0],zd['zone'][1]['htsp'][0],
#         zd['zone'][1]['rt'][0],zd['zone'][1]['clsp'][0],
#         zd['zone'][1]['rh'][0],zd['zone'][1]['fan'][0],
#         zd['zone'][1]['damperposition'][0]))
#     writelog('{} <{}> temp {} < {} < {}, RH {}%, fan {}, damper {} (0 is closed)'.format
#         (timestr,zd['zone'][2]['name'][0],zd['zone'][2]['htsp'][0],
#         zd['zone'][2]['rt'][0],zd['zone'][2]['clsp'][0],
#         zd['zone'][2]['rh'][0],zd['zone'][2]['fan'][0],
#         zd['zone'][2]['damperposition'][0]))
    
