from __future__ import division
import pandas as pd 
import tushare as ts 
import matplotlib.pyplot as plt 
import numpy as np 
import warnings 
warnings.filterwarnings('ignore')
'''
#groub apply
def volume_ma(df,window=40):
	df['volume_ma_40'] = pd.rolling_mean(df['volume'],window=window)
	df['close_ma_5'] = pd.rolling_mean(df['close'],window=5)
	df['close_ma_30'] = pd.rolling_mean(df['close'],window=30)
	return df

def close_ma(df,window=5):
	name = 'close_ma_' + str(window)
	df[name] = pd.rolling_mean(df['close'],window=window)
	df[name].fillna(0,inplace=True)
	return df 

df = pd.read_hdf('ana_data.h5', 'dayk')
df = df[df['date'] > '2016-01-01']
df = df.groupby('code').apply(volume_ma)
df['volume_ma_40'].fillna(0,inplace=True)
df['close_ma_5'].fillna(0,inplace=True)
df['close_ma_30'].fillna(0,inplace=True)
df.to_hdf('ana_data.h5','data_ma')

df = pd.read_hdf('dayk.h5','dayk')
df = df[df['date'] > '2017-01-01']
code_list = list(df['code'].unique())
all_list = ['date','code','change']
df_all = pd.DataFrame(columns=all_list)
for code in code_list:
	df_temp = df[df['code'] == code]
	df_temp['change'] = df_temp['close'] / df_temp['close'].shift(1) - 1.0
	df_all = pd.concat([df_all,df_temp[all_list]])
	print code + ' _Done!'

df_all.to_csv('dayk_change_0510.csv')

df = pd.read_csv('dayk_change_0510.csv')
date_list = list(df['date'].unique())
df = df.dropna()

print df[df['date'] == date_list[-1]]['change'].mean()
'''
df = pd.DataFrame(columns=['all_a','change','date'])
print df 
