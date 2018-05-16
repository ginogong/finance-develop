from __future__ import division
import tushare as ts 
import pandas as pd 
import numpy as np 
pd.set_option('precision',6)


#print data['price'].quantile([0.1,0.9])
#print data

grid_low  = 99.90
grid_high = 100.05
grid_step = 0.001

lows = int((grid_low+grid_step) * 1000)
highs = int((grid_high+grid_step) * 1000)
vec = pd.DataFrame({'buy':[],'sell':[]})


for low in range(lows,highs):
	vec_sell = range(low,highs)
	vec_temp = pd.DataFrame({'sell':vec_sell})
	vec_temp['sell'] = vec_temp['sell'] / 1000.0
	vec_temp['buy'] = low /1000 -0.001
	vec = pd.concat([vec,vec_temp])
vec = vec.drop_duplicates()
vec.index = range(len(vec))


#print vec
# grid coloumns   price_buy  price_sell quantity

def signal(vec,df):
	df.ix[df['price'] < vec['buy'],'temp'] = 0 
	df.ix[df['price'] > vec['sell'],'temp'] = 1
	df['temp'].fillna(method='pad',inplace=True)
	df.ix[df['temp'] < df['temp'].shift(1),'change'] = 1
	df['change'].fillna(0,inplace=True)
	df['change'] = df['change'].cumsum()
	df.index = range(len(df))
	return int(df.ix[len(df)-1,'change'])


for i in range(len(vec)):
	data = pd.read_hdf('tick.h5','511990')
	vec.ix[i,'number']= signal(vec.ix[i,:],data)
	vec['number'].fillna(0,inplace=True)
	print 'finished %s in %s' % (i, len(vec))

vec.to_csv('mass_grid_data.csv')


