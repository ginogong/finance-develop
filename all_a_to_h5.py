#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd
import datetime

now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d')
df = pd.read_hdf('dayk_17.h5','dayk_17')
df_all = pd.read_hdf('all_index.h5' , 'all_a')
df.index = range(len(df))
df_index = df.copy()
df_index['change'] = df_index.groupby('code').close.pct_change()

change_now =  df_index[df_index['date'] ==now].change.mean()
df_all = df_all.sort_index()
length = len(df_all)
all_a_now = df_all.ix[length-1, 'all_a']
if str(df_all.index[-1]) < now:
	print 'run'
	df_all.loc[now,'change'] = change_now
	df_all.loc[now,'all_a'] = all_a_now * ( 1 + change_now )
print df_all
'''
code_list = list(df['code'].unique())
date_list = list(df['date'].unique()) 
all_list = ['date','code','change']
df_all = pd.DataFrame(columns=all_list)
for code in code_list:
	df_temp = df[df['code'] == code]
	df_temp['change'] = df_temp['close'] / df_temp['close'].shift(1) - 1.0
	df_all = pd.concat([df_all,df_temp[all_list]])
	print code + ' _Done!'

df_index = pd.DataFrame(columns=['all_a','change','date'])
change_list = [] 
for date in date_list:
	change_list.append(df_all[df_all['date'] ==date]['change'].mean())

df_index = pd.DataFrame({'date':date_list,'change':change_list})
df_index.ix[0,'change'] = 0
df_index.ix[0,'all_a']  = 1000
df_index = df_index.sort_values(by='date')
df_index = df_index.set_index('date')
for i in range(len(df_index)):
	if i > 0:
		df_index.ix[i,'all_a'] = (df_index.ix[i,'change'] + 1) * df_index.ix[i-1,'all_a']


'''
df_all.to_hdf('all_index.h5','all_a')


