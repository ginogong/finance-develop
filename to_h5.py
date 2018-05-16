#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd

df = pd.read_hdf('dayk.h5','dayk')
#print df.columns
#print len(df.groupby(u'code').apply(lambda x : x[u'close_price'] / x[u'close_price'].shift(1) - 1.0))
#print len(df)
df = df.sort_values(by=['code','date'])
df2 = df.groupby(u'code').apply(lambda x : x[u'close_price'] / x[u'close_price'].shift(1) - 1.0)
df['change'] = (list(df2))
df['change'].fillna(0,inplace=True)
df3 = df.groupby('date')['change'].mean()
df4 = pd.DataFrame(df3)
df4.ix[0,'all_a'] = 1000
for i in range(len(df4)):
	if i >0:
		df4.ix[i,'all_a'] = (df4.ix[i,'change'] + 1) * df4.ix[i-1,'all_a']
df4.to_hdf('all_index.h5','all_a')


