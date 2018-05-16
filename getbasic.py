# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlalchemy as sa 
import tushare as ts 
import pandas as pd 
import numpy as np 
from sqlalchemy import create_engine
from pandas.tseries.offsets import *
# gen adjust dataframe ---------
#---------gen hold list ------
#-----check holding----
#-----check adjust----
#-----adjust-----
#-----cal net worth
#-----gen hold list
hold_li = pd.DataFrame({'date':'2016-10-11','code':'999999','price':1,'weight':1.0},index=[0])
adjust_li = pd.DataFrame({'date':['2016-10-11','2016-10-11'],
						'code':['600000','300124'],
						'target_weight':[0.4,0.4]})
print adjust_li
print hold_li
#---- import dayk
dayk = pd.read_hdf('dayk.h5')
#---adjust
start_date = hold_li.ix[0,'date']
worth_li = pd.DataFrame([],columns=['date','net_worth'])
#--- check adjust
df = pd.merge(adjust_li,hold_li,how='outer')
df = df.fillna(0)
wsum = df['target_weight'].sum()
df = df.set_index('code')
df.loc['999999','target_weight'] = 1 - df['target_weight'].sum()
df['close_price'] = 0
#--- cal price
for i in df.index:
	if i =='999999':
		df.loc[i,'price'] = 1
		df.loc[i,'close_price'] = 1
	else:
		data_k = dayk[dayk.code == i]
		data_k = data_k[data_k.date ==start_date]
		data_k = data_k.set_index('code')	
		df.loc[i,'price'] = data_k.loc[i,'open_price']
		df.loc[i,'close_price'] = data_k.loc[i,'close_price']
df['change'] = (df['close_price'] - df['price']) / df['price']
df['worth'] =  df['target_weight'] * (1+df['change'])
net_worth = df['worth'].sum()
df['weight'] = df['worth'] / net_worth
day_worth = pd.Series({'date':start_date,'net_worth':net_worth})
print day_worth
worth_li = worth_li.append(day_worth,ignore_index=True)
print df
print net_worth
print worth_li

data_plus = (pd.to_datetime(start_date) + BDay()).strftime('%Y-%m-%d')

#---cal net worth--
#---cal hold change
'''
for i in range(len(hold_li['code'])):
	code_hold = hold_li.ix[i,'code']
	date_hold = hold_li.ix[i,'date']
	if code_hold == '999999':
		hold_li.ix[i,'change'] = 0
	else:
		data_k = dayk[dayk.code ==code_hold]
		data_k = data_k.set_index('date')
		price_close = data_k.loc[date_hold,'close_price']
		price_hold = hold_li.ix[i,'price']
		hold_li.ix[i,'change'] =  (price_close - price_hold) / price_hold
#----calculate net worth---
hold_li['netsum'] = hold_li['weight'] *(1+ hold_li['change']).sum()
hold_li['weight_change'] = hold_li['weight'] / hold_li['netsum'] 
# ---
'''








	








