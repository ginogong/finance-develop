#-*- coding:utf-8 -*-
from __future__ import division
import requests
from pyquery import PyQuery as pq
import pandas as pd
import datetime

'''
url = 'http://hq.sinajs.cn/list='
code = 'sh603027'
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
response = requests.get(url + code, headers=header_req)
l1 = response.text.split(',')
#print 'open:',float(l1[1]),'close:',float(l1[3]),'high:',float(l1[4]),'low:',float(l1[5]),'volume:',int(l1[8])/100
now = datetime.datetime.now().strftime('%Y-%m-%d')
code1 = code[2:]
values = [now,float(l1[1]),float(l1[3]),float(l1[4]),float(l1[5]),int(l1[8])/100,code1]
df_temp = pd.DataFrame(values,columns=columns)
#df = pd.read_hdf('dayk.h5','dayk')
'''

def add_prefix(code):
	code = str(code)
	if code.startswith('6'):
		code = 'sh'+ code
	else:
		code = 'sz' + code
	return code

def get_data(code,head):
	url = 'http://hq.sinajs.cn/list='
	response = requests.get(url + code, headers=head)
	l1 = response.text.split(',')
	if len(l1) >= 5:
		if float(l1[1]) != 0.0 and float(l1[8] > 0):
		    now = datetime.datetime.now().strftime('%Y-%m-%d')
		    date_list.append(l1[30])
		    open_price_list.append(float(l1[1]))
		    close_price_list.append(float(l1[3]))
		    high_price_list.append(float(l1[4]))
		    low_price_list.append(float(l1[5]))
		    volume_list.append(int(l1[8])/100)
		    code_list.append(code[2:])

		    print '%s has finished!' % code


header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
date_list = []
open_price_list = []
close_price_list = []
high_price_list = []
low_price_list = []
volume_list = []
code_list = []
columns = [u'date',u'open_price',u'close_price',u'high_price',u'low_price',u'volume',u'code']
stock_list = pd.read_hdf('stocklist.h5','stocklist')

for i in range(len(stock_list)):	
	code = stock_list.ix[i,'stocklist']
	code_temp = add_prefix(code)
	get_data(code_temp,header_req)

df = pd.DataFrame({u'date':date_list,u'open_price':open_price_list,u'close_price':close_price_list,\
					u'high_price':high_price_list,u'low_price':low_price_list,u'volume':volume_list,\
					u'code':code_list})
df = df[columns]
print len(df) 
df.to_csv('20170310_04.csv')


