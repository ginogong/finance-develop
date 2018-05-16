#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 16:35:45 2017

@author: Gino
"""
from __future__ import division
import pandas as pd
 
pd.set_option('precision',4)

PATH = '/Users/Gino/workspace/mysite/stock/stock/'
def rise_delta_hs300(df):
    change='hs300_change'
    df_temp = df[df[change] >0]
    mean = (df_temp['mini_change'] - df_temp[change]).mean()
    return mean
def down_delta_hs300(df1):
    change='hs300_change'
    df_temp = df1[df1['hs300_change']<0]
    mean = (df_temp['mini_change'] - df_temp[change]).mean()
    return mean
def rolling_cal(dataframe,window=250):
    lens = len(dataframe)
    for i in range(lens):
        if window+i < lens:
            df_temp = dataframe[0+i:window+i]
            df_hs300_up = df_temp[df_temp['hs300_change'] >0]
            df_hs300_down = df_temp[df_temp['hs300_change'] <0]
            df_all_up = df_temp[df_temp['change']>0]
            df_all_down = df_temp[df_temp['change']<0]
            dataframe.loc[window+i,'hs_down'] = (df_hs300_down['mini_change'] - df_hs300_down['hs300_change']).mean()
            dataframe.loc[window+i,'hs_up'] = (df_hs300_up['mini_change'] - df_hs300_up['hs300_change']).mean()
            dataframe.loc[window+i,'all_up'] = (df_all_up['mini_change'] - df_all_up['change']).mean()
            dataframe.loc[window+i,'all_down'] = (df_all_down['mini_change'] - df_all_down['change']).mean()
            
    return dataframe  
df = pd.read_excel(PATH+'mini1120.xls')
df = df.rename(columns={'Category':'date'})
df = df.set_index('date')
df['mini_change'] = df['mini'].pct_change()
df['mini_change'].fillna(0,inplace=True)
df['hs300_change'] = df['hs300'].pct_change()
df['hs300_change'].fillna(0,inplace=True)

df_all = pd.read_hdf(PATH+'all_index.h5','all_a')

df_concat = pd.concat([df,df_all],axis=1,join_axes=[df.index])

df_concat = df_concat.reset_index()
df_res = rolling_cal(df_concat).set_index('date')
df_res = df_res.dropna()
print df

#df_concat.rolling(window=250,min_periods=90).apply(mean)

#df_all[df_all['change'] <0]

