#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:19:09 2016

@author: Gino
"""
from pyquery import PyQuery as pq
import pandas as pd 
import re
import requests
import sys
from sqlalchemy import create_engine
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://quote.eastmoney.com/stocklist.html'
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
response = requests.get(url, headers=header_req)
response.encoding = 'gbk'
engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8')
data = pq(response.text)
pattern = re.compile(u"\d{6}")
num = 0
temp_list = []
with open('stocklist.txt', 'w') as sl:
	for item in data('#quotesearch ul a'):
		if pattern.findall(pq(item).text())[0][0:3] in ['600', '603', '601', '300', '002', '000']:
			sl.write(pattern.findall(pq(item).text())[0] + '\n')
			temp_list.append(pattern.findall(pq(item).text())[0])
			#print pattern.findall(pq(item).text())[0]
			#num += 1
df = pd.DataFrame(temp_list,columns=['stocklist'])
df.to_sql('list',engine)



 