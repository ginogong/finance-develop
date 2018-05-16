import redis
import pandas as pd 
import tushare as ts 
import tables
import numpy as np 
import datetime
'''
loop = True
chunkSize = 100000
chunks = []
while loop:
  try:
    chunk = reader.get_chunk(chunkSize)
    chunks.append(chunk)
  except StopIteration:
    loop = False
    print "Iteration is stopped."
df = pd.concat(chunks, ignore_index=True)

df = ts.get_k_data('600000',start='2016-10-30',end='2016-11-05')
r = redis.Redis(host='localhost', port=6379, db=1)

rng= pd.bdate_range('2016-10-01',periods=5)
start = pd.datetime(2015,1,1)
end = pd.datetime(2015,2,1)
ts = pd.DataFrame(np.random.randn(len(rng)),index=rng,columns=['data'])
print (pd.to_datetime('2016-10-1') + pd.tseries.offsets.BDay()).strftime('%Y-%m-%d')
'''
'''
from sqlalchemy import create_engine
engine = create_engine('mysql://root:tomeko123@localhost/stock')
df = ts.get_k_data('399300',index=True,start='2013-01-01',end='2016-12-30')
df.to_sql('hs300',engine)
df.to_hdf('hs300.h5','hs300')
'''
from pandas.tseries.offsets import *
df = pd.read_hdf('hs300.h5')
start = '2016-10-01'
end = '2016-11-02'
#--- date list
date_li = pd.DataFrame([start],columns=['date'])
flag = True
while flag == True:
	if  len(df[df['date']==start]) == 0:
		start= (pd.to_datetime(start) + BDay()).strftime('%Y-%m-%d')
		print start
	else:
		flag = False
		start_index = df[df['date']==start].index
print start_index
flag1 = True
while flag1 ==True:
	if len(df[df['date']==end]) == 0:
		end = (pd.to_datetime(end) - BDay()).strftime('%Y-%m-%d')
	else:
		flag1 = False
		end_index = df[df['date']==end].index
print end_index
print df[start_index:end_index]
'''
for i in range()
if len(df[df['date']==start]) == 0:
	start =+
print date_li
'''





