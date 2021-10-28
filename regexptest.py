#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:17:54 2020

@author: pugsley
"""
import re

good = 'outside 2020-10-03T17:56:00+00:00:64.0/41.1,'
bad = 'outside nan:nan/nan,'

tagstr = r'outside ((.*?)\+\d\d:\d\d|nan):(.*?|nan)/(.*?|nan),'

grpgood = re.match(tagstr,good)
print('Good: {}, {}, and {}\n'.format(grpgood[1],grpgood[2],grpgood[3]))
grpbad = re.match(tagstr,bad)
if grpbad is None:
    print('Bad got None\n')
else:
    print('Bad: {}, {}, and {}\n'.format(grpbad[1],grpbad[2],grpbad[3]))




