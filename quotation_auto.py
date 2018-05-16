# -*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import warnings 
import tushare as ts
from pyquery import PyQuery as pq
import re
import requests
import datetime
from rollingmaxdd import max_dd
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)

now_time = datetime.datetime.now()
now = now_time.strftime('%Y-%m-%d')

def find_lastday(dataframe):
	last_day = dataframe['date'].sort_values(ascending=False).unique()[0]
	return last_day

def get_dayk(code,start,end):
	df = ts.get_k_data(code,start=start,end=end)
	return df

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

#get new stock list
url = 'http://quote.eastmoney.com/stocklist.html'
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
'''
response = requests.get(url, headers=header_req)
response.encoding = 'gbk'
data = pq(response.text)
pattern = re.compile(u"\d{6}")
temp_list = []
with open('stocklist.txt', 'w') as sl:
	for item in data('#quotesearch ul a'):
		if pattern.findall(pq(item).text())[0][0:3] in ['600', '603', '601', '300', '002', '000','001']:
			sl.write(pattern.findall(pq(item).text())[0] + '\n')
			temp_list.append(pattern.findall(pq(item).text())[0])
			#print pattern.findall(pq(item).text())[0]
			#num += 1
df_stlist = pd.DataFrame(temp_list,columns=['stocklist'])
df_stlist.to_hdf('stocklist.h5','stocklist')
print 'stock list updating finished '
#read history data decision
'''
date_list = []
open_price_list = []
close_price_list = []
high_price_list = []
low_price_list = []
volume_list = []
code_list = []
columns = ['date','open','close','high','low','volume','code']
stock_list = pd.read_hdf('stocklist.h5','stocklist')

for i in range(len(stock_list)):	
	code = stock_list.ix[i,'stocklist']
	code_temp = add_prefix(code)
	get_data(code_temp,header_req)

df = pd.DataFrame({'date':date_list,'open':open_price_list,'close':close_price_list,\
					'high':high_price_list,'low':low_price_list,'volume':volume_list,\
					'code':code_list})
df = df[columns]

df_hist = pd.read_hdf('dayk.h5','dayk')
df_hist = pd.concat([df_hist,df])
df_hist = df_hist.drop_duplicates()
df_hist.to_hdf('dayk.h5','dayk')
print 'stock day k data updating finished'
#df_hist = df_hist[['date','open_price','close_price','high_price','low_price','volume','code']]
#df_hist.to_hdf('dayk.h5','dayk')
#hist_last_day = df_hist['date'].sort_values(ascending=False).unique()[0]


'''
#get different quotation from history  until now
for index in range(len(df_stlist)):
	df_temp = get_dayk(df_stlist.ix[index,'stocklist'],hist_last_day,now)
	if len(df_temp) > 0:
		df_temp.columns = df_hist.columns
		df_hist = pd.concat([df_hist,df_temp])
df_hist = df_hist.drop_duplicates()
df_hist.to_hdf('dayk.h5','dayk')
print 'stock day k data updating finished'
'''

columns = ['open','close','high','low','volume']
df_hs = pd.read_hdf('all_index.h5','hs300')
hs_last_day = df_hs.sort_index().index[-1].strftime('%Y-%m-%d')
hs_temp = ts.get_k_data('399300',index=True,start=hs_last_day,end=now)
hs_temp = hs_temp.set_index('date')
hs_temp.index = pd.to_datetime(hs_temp.index)
hs_temp = hs_temp[columns]

if len(hs_temp[1:]) >= 1:
	df_hs = pd.concat([df_hs,hs_temp[1:]])
	df_hs = df_hs.drop_duplicates()
	df_hs = df_hs.sort_index()
	df_hs.to_hdf('all_index.h5','hs300')
print 'hs300 updating finished'


df_zz = pd.read_hdf('all_index.h5','zz1000')
zz_last_day = df_zz.sort_index().index[-1].strftime('%Y-%m-%d')
zz_temp = ts.get_k_data('000852',index=True,start=zz_last_day,end=now)
zz_temp = zz_temp.set_index('date')
zz_temp.index = pd.to_datetime(zz_temp.index)
zz_temp = zz_temp[columns]
if len(zz_temp[1:]) >= 1:
	df_zz = pd.concat([df_zz,zz_temp[1:]])
	df_zz = df_zz.drop_duplicates()
	df_zz = df_zz.sort_index()
	df_zz.to_hdf('all_index.h5','zz1000')
print 'zz1000 updating finished'






