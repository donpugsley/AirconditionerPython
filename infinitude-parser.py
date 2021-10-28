# Log Carrier A/C system status to a file
# Uses Infinitude server to get Carrier A/C data
# Infinitude is running on Docker with a random port... 

host = '192.168.1.202'
port = 32769

import requests

api_root='http://'+host+':'+str(port)+'/api/' # base api url
status_url=api_root+'status/' 

# Get system status
status = requests.get(status_url)
if status.status_code != 200: # Badness
    print('{} GET'.format(status.status_code))
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
    print('{}: ops {}, cfg {}, mode {}, z {}/{}/{}, zcon {}/{}/{}, zhrc {}<{}<{}/{}<{}<{}/{}<{}<{}, zen {}/{}/{}, zhum {}/{}/{}, zfan {}/{}/{}, zdamp {}/{}/{}'.format\
          (timestr,ops,cfg,mode,zn0,zn1,zn2,zc0,zc1,zc2,zh0,zh1,zh2,zr0,zr1,zr2,zl0,zl1,zl2,ze0,ze1,ze2,zu0,zu1,zu2,zf0,zf1,zf2,zd0,zd1,zd2))
    
