#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 22:33:40 2017

@author: Gino
"""

from __future__ import division
import datetime
import pandas as pd
from pyquery import PyQuery as pq
import re
import time
import requests
import random

CODE = '601988'
URL = 'http://quote.eastmoney.com/%s.html'
HEADER_REQ = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
PATH = '/Users/Gino/workspace/mysite/stock/stock/'
now = datetime.datetime.now().strftime('%Y-%m-%d')
df_stocklist = pd.read_hdf(PATH +'stocklist.h5','stocklist')

def auto_pre(code):
    if code.startswith('6'):
        code = 'sh'+ code
    else:
        code = 'sz'+ code
    return code
    
def get_outstand(url_base,code):
    new_code = auto_pre(code)
    url = url_base % new_code
    response = requests.get(url,headers=HEADER_REQ)
    response.encoding = 'gbk'
    data = pq(response.text)
    pattern = re.compile(r'[0-9]+.[0-9]+')
    num = 0
    for item in data('#rtp2 tr td'):   
        
        name = ur'流通股'
        lev1 = ur'万'
        lev2 = ur'亿'
        if pq(item).text()[0:3] == name:
            if len(pattern.findall(pq(item).text())) > 0:
                num =float( pattern.findall(pq(item).text())[0])
                if pq(item).text()[-1:] == lev2:
                    num = 10000 * num

    outstand_list.append(num)
    code_list.append(code)
    print code + 'Done!'


outstand_list =[]
code_list = []
for i in range(len(df_stocklist)):
    time_sleep = random.uniform(0,0.1)
    code = df_stocklist.loc[i,'stocklist']
    get_outstand(URL,code)
    time.sleep(time_sleep)
df = pd.DataFrame({'code':code_list,'outstand':outstand_list})
df['date'] = now

df_outstand = pd.read_hdf(PATH+'outstand.h5','outstand')
df_outstand = pd.concat([df_outstand,df])
df_outstand.to_hdf(PATH +'outstand.h5','outstand')

'''
#new_code = auto_pre(CODE)
#url = URL + new_code
response = requests.get(URL,headers=HEADER_REQ)
response.encoding = 'gbk'
data = pq(response.text)
pattern = re.compile(r'[0-9]+.[0-9]+')
for item in data('#rtp2 tr td'):
    name = ur'流通股'
    lev1 = ur'亿'
    lev2 = '万'
    if pq(item).text()[0:3] == name:
        num = float(pattern.findall(pq(item).text())[0])
        if pq(item).text()[-1:] == lev1:
            num = num * 10000
print str(num) + lev2   
'''
        
        
        
        
        