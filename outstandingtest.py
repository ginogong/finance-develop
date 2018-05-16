#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 21:39:57 2017

@author: Gino
"""
import requests
import pandas as pd 
from pyquery import PyQuery as pq
import re
import time
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
PATH = '/Users/Gino/workspace/mysite/stock/stock/'
url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/%s/stocktype/LiuTongA.phtml' 
df_stocklist = pd.read_hdf(PATH +'stocklist.h5','stocklist')
date_list = []
outstanding_list = []
code_list = []

    
def get_data(url,code):
     
    response = requests.get(url1,headers=header_req)
    response.encoding = 'gbk'
    data = pq(response.text)
    pattern = re.compile('[0-9]+.[0-9]+')

    for item in data('#historyTable07 tr'):
        if pattern.findall(pq(item[1]).text()):
            date_list.append(str(pq(item[0]).text()))
            outstanding_list.append(float(pattern.findall(pq(item[1]).text())[0]))
            code_list.append(code)
    for item in data('#historyTable06 tr'):
        if pattern.findall(pq(item[1]).text()):
            date_list.append(str(pq(item[0]).text()))
            outstanding_list.append(float(pattern.findall(pq(item[1]).text())[0]))
            code_list.append(code)
            #print pq(item[0]).text()
            #print pattern.findall(pq(item[1]).text()[0])
    for item in data('#historyTable05 tr'):
        if pattern.findall(pq(item[1]).text()):
            date_list.append(str(pq(item[0]).text()))
            outstanding_list.append(float(pattern.findall(pq(item[1]).text())[0]))
            code_list.append(code)
           # print type(pq(item[0]).text())
            #print type(pattern.findall(pq(item[1]).text())[0])
for i in range(len(df_stocklist)):
    code = str(df_stocklist.loc[i,'stocklist'])
    url1 = url % code
    get_data(url1,code)
    print code + 'Done!'
    time.sleep(0.01)
            
df = pd.DataFrame({'date':date_list,'outstand':outstanding_list,'code':code_list})
df.to_hdf(PATH+'outstand.h5','outstand')
