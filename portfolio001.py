# -*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import warnings 
from rollingmaxdd import max_dd
import datetime
warnings.filterwarnings('ignore')

galaxy_start = '2013-04-12'
galaxy_end = '2017-03-28'
filename = 'knn30_0402.csv'

def split_data(df,start='2015-01-01',end='2017-03-10'):
	df = df[df.index >= start]
	df = df[df.index <= end]
	return df 

def signal(hs,zz,step=0.125):
	hs_signal = 0
	zz_signal = 0
	if hs == 1 and zz == 1:
		hs_signal = 0
		zz_signal = 0
	elif hs == -1 and zz ==1:
		hs_signal = 0
		zz_signal = step
	elif hs == 1 and zz == -1:
		hs_signal = step
		zz_signal = 0
	else:
		hs_signal = -1 * step
		zz_signal = -1 * step
	return hs_signal, zz_signal

def adjust_signal(weight,high=0.82,low=0.18):
	if weight > 0.82:
		return 0
	elif weight < 0.18:
		return 0
	else:
		return 1
def defence(df,threshold=-0.1204):
	pass

def period_return(df):
	df.index = pd.to_datetime(df.index)
	year_return  = df['port_change'].resample('A',how=lambda x:(1 + x).prod() - 1.0)
	month_return = df['port_change'].resample('M',how=lambda x:(1 + x).prod() - 1.0)
	week_return  = df['port_change'].resample('W',how=lambda x:(1 + x).prod() - 1.0)
	year_return.fillna(0,inplace=True)
	month_return.fillna(0,inplace=True)
	week_return.fillna(0,inplace=True)
	year_winrate = len(year_return[year_return > 0]) / len(year_return[year_return != 0])
	month_winrate = len(month_return[month_return > 0]) / len(month_return[month_return != 0])
	week_winrate = len(week_return[week_return > 0]) / len(week_return[week_return != 0])
	print 'year_return:',year_return
	print 'year_winrate:',year_winrate
	print 'month_return:',month_return
	print 'month_winrate:', month_winrate
	print 'week_return:',week_return
	print 'week_winrate:',week_winrate

def calculate_change(df):
	df['port_change'] = df['worth'] / df['worth'].shift(1) - 1.0
	df.ix[0,'port_change'] = 0.5 * df.ix[0,'zzchange'] + 0.5 * df.ix[0,'hschange']
	return df 

def maxdd(df):
	df['max2here'] = pd.expanding_max(df['worth'])
	df['dd2here'] = df['worth'] / df['max2here'] -1.0
	max_dd = df.sort_values(by='dd2here').ix[0,'dd2here']
	end_date = df.sort_values(by='dd2here').index[0]
	end_date_str= end_date.strftime('%Y-%m-%d')
	df = df[df.index < df.sort_values(by='dd2here').index[0]]
	start_date = df.sort_values(by='worth',ascending=False).index[0]
	start_date_str = start_date.strftime('%Y-%m-%d')
	lasts_days = len(df.loc[start_date:end_date])
	print max_dd
	print 'maxxdd is %f,from %s to %s last %d days' % (max_dd, start_date_str,end_date_str,lasts_days)
	
def returnline(df):
	max_worth = df.sort_values(by='worth',ascending=False).ix[0,'worth']
	date = df.sort_values(by='worth',ascending=False).index[0]
	date_str = date.strftime('%Y-%m-%d')
	end_date = df.sort_index().index[-1]
	end_date_str = end_date.strftime('%Y-%m-%d')
	lasts_days = len(df.loc[date:end_date])
	print 'max return is %f,from %s to %s lasts %d days below the max return' % (max_worth,date_str,end_date_str,lasts_days)

def calc_change(df):
	df['change'] = df['close'] / df['close'].shift(1) - 1.0
	df.ix[0,'change'] = 0
	return df

df_hs300 = pd.read_hdf('all_index.h5','hs300')
df_zz1000 = pd.read_hdf('all_index.h5','zz1000')
df_hs300 = calc_change(df_hs300)
df_zz1000 = calc_change(df_zz1000)
df_hs300 = split_data(df_hs300,start=galaxy_start,end=galaxy_end)
df_zz1000 = split_data(df_zz1000,start=galaxy_start,end=galaxy_end)

#df_hs300 = df_hs300.set_index('date')
#df_zz1000 = df_zz1000.set_index('date')
df = df_hs300.copy()
df_hs300 = max_dd(df_hs300,window=27)
df_zz1000 = max_dd(df_zz1000,window=20)
df['zzchange'] = df_zz1000['change']
df['zzmaxdd'] = df_zz1000['maxdd']
df['hschange'] = df_hs300['change']
df['hsmaxdd'] = df_hs300['maxdd']
df = df[['zzchange','hschange','hsmaxdd','zzmaxdd']]


label = pd.read_csv(filename)
label = label.set_index('date')
wght_zz = 0.5
wght_hs = 0.5
worth = 1.0
hs_thres = -1
zz_thres = -1
weight_low = 0.18


for i in range(len(df)):
	if i >= 1:
		if df.ix[i-1,'hsmaxdd'] <= hs_thres:
			wght_hs = 0
		elif df.ix[i-1,'wght_hs'] == 0:
			wght_hs = weight_low
		if df.ix[i-1,'zzmaxdd'] <= zz_thres:
			wght_zz = 0
		elif df.ix[i-1,'wght_zz'] == 0:
			wght_zz = weight_low
	zz = df.ix[i,'zzchange']
	hs = df.ix[i,'hschange']
	worth = worth * (1 + zz * wght_zz  + hs * wght_hs)
	df.ix[i,'worth'] = worth
	hs1 = label.ix[i,'hs_pre']
	zz1 = label.ix[i,'zz_pre']
	hs_sig,zz_sig = signal(hs1,zz1)	
	wght_zz_temp = (wght_zz + zz * wght_zz ) / (1 + zz * wght_zz + hs * wght_hs)
	wght_hs_temp = (wght_hs + hs * wght_hs ) / (1 + zz * wght_zz + hs * wght_hs)
	df.ix[i,'wght_zz'] = wght_zz_temp
	df.ix[i,'wght_hs'] = wght_hs_temp
	wght_zz_obj = wght_zz_temp + zz_sig
	wght_hs_obj = wght_hs_temp + hs_sig
	zz_flag = adjust_signal(wght_zz_obj)
	hs_flag = adjust_signal(wght_hs_obj)
	if wght_zz_obj + wght_hs_obj > 1:
		wght_zz = wght_zz_temp
		wght_hs = wght_hs_temp
	else:
		wght_zz = wght_zz_temp + zz_flag * zz_sig
		wght_hs = wght_hs_temp + hs_flag * hs_sig

df = calculate_change(df)
period_return(df)
maxdd(df)
returnline(df)

df.to_csv('worth_0402_'+filename)







