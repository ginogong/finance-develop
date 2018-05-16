#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np 
import tushare as ts
import warnings
import datetime
#----setting------
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',7)
pd.set_option('expand_frame_repr',False)
#-----------------

index_name = ['all_a','hs300','zz1000']

#get data
def get_data(name,store='all_index.h5'):
	df = pd.read_hdf(store,name)
	return df 
#sort date set date index

def sort_dataframe(df,start='2010-01-01',end='2017-03-13'):
	df = df[df.index >= start]
	df = df[df.index <= end]
	return df 

#rolling 
def calc_rolling(df):
	rolling_number = [5,10,20,30,40,60]
	for i in rolling_number:
		name = 'sma' + str(i)
		change_name = 'change_sma' + str(i)
		df[name] = pd.rolling_mean(df['close'],window=i,min_periods=1)
		df[change_name] = (df['close'] - df[name]) / df['close'].shift(1)
		df.fillna(0,inplace=True)
	return df

#calculate period change
def period_change(df):
	period_list = [5,10,20]
	for i in period_list:
		name = 'change' + str(i)
		df[name] = df['close'] / df['close'].shift(i) - 1.0
	return df
#cal amplitude
def amplitude_range(df):
	period_list = [5,10,20,40]
	for i in period_list:
		name = 'ampr' + str(i)
		df[name] = (pd.rolling_max(df['high'],i) - pd.rolling_min(df['low'],i)) / df['close'].shift(i+1)
	return df 
		
#cal volume rate of increase
def volume_rate(df):
	period_list = [10,20,30,40]
	for i in period_list:
		name = 'volr' + str(i)
		df[name] =  df['volume'] / pd.rolling_mean(df['volume'],i) - 1.0
	return df

#calculate future change
def future_change(df):
	period_list = [1,2,3,5]
	name = 'furc' + str(1)
	df[name] = df['close'] / df['close'].shift(1) -1
	df[name] = df[name].shift(-1)
	return df 

def calc_change(df):
	df['change'] = df['close'] / df['close'].shift(1) - 1.0
	df.ix[0,'change'] = 0
	return df 

now = datetime.datetime.now().strftime('%Y-%m-%d')
#now = '2017-05-19'
#get data
df_all = get_data(index_name[0])

df_hs300 = get_data(index_name[1])
df_hs300 = calc_change(df_hs300)

df_zz1000 = get_data(index_name[2])
df_zz1000 = calc_change(df_zz1000)

#--------------------
#hs - sma change and zz - sma change
df_hs300 = calc_rolling(df_hs300)

df_zz1000 = calc_rolling(df_zz1000)

df_hs300 = period_change(df_hs300)

df_zz1000 = period_change(df_zz1000)
df_hs300 = amplitude_range(df_hs300)
df_zz1000 = amplitude_range(df_zz1000)
df_hs300 = volume_rate(df_hs300)
df_zz1000 = volume_rate(df_zz1000)

df_hs300 = sort_dataframe(df_hs300,end=now)
df_zz1000 = sort_dataframe(df_zz1000,end=now)
df_all = sort_dataframe(df_all,end=now)



#--------------------
#append  all - hs  and all - zz
feature = df_all.copy()
feature['all_hs_change'] =  df_all['change'] - df_hs300['change']

feature['all_zz_change'] =  df_all['change'] - df_zz1000['change']

feature['hs_zz_sma5'] = df_hs300['change_sma5'] - df_zz1000['change_sma5']

feature['hs_zz_sma10'] = df_hs300['change_sma10'] - df_zz1000['change_sma10']
feature['hs_zz_sma20'] = df_hs300['change_sma20'] - df_zz1000['change_sma20']
feature['hs_zz_sma30'] = df_hs300['change_sma30'] - df_zz1000['change_sma30']
feature['hs_zz_sma40'] = df_hs300['change_sma40'] - df_zz1000['change_sma40']
feature['hs_zz_sma60'] = df_hs300['change_sma60'] - df_zz1000['change_sma60']
feature['hs_zz_chg5']  = df_hs300['change5'] - df_zz1000['change5']
feature['hs_zz_chg10'] = df_hs300['change10'] - df_zz1000['change10']
feature['hs_zz_chg20'] = df_hs300['change20'] - df_zz1000['change20']
feature['hs_zz_amp5']  = df_hs300['ampr5'] - df_zz1000['ampr5']
feature['hs_zz_amp10'] = df_hs300['ampr10'] - df_zz1000['ampr10']
feature['hs_zz_amp20'] = df_hs300['ampr20'] - df_zz1000['ampr20']

feature['hs_zz_amp40'] = df_hs300['ampr40'] - df_zz1000['ampr40']

feature['hs_zz_vol10'] = df_hs300['volr10'] - df_zz1000['volr10']

feature['hs_zz_vol20'] = df_hs300['volr20'] - df_zz1000['volr20']

feature['hs_zz_vol30'] = df_hs300['volr30'] - df_zz1000['volr30']

feature['hs_zz_vol40'] = df_hs300['volr40'] - df_zz1000['volr40']

feature.to_hdf('ml.h5','feature002')



 





