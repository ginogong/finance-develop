#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:18:28 2017

@author: Gino
"""
from __future__ import division
import pandas as pd 
import tushare as ts 
import matplotlib.pyplot as plt 
import numpy as np
import warnings 
warnings.filterwarnings('ignore')

def moving_average(df,day=60):
    df['volume_avg'] = pd.rolling_mean(df['volume'],window=day)
    return df

def macd(df,window):
    name = 'macd_' + str(window)
    df[name] = pd.rolling_mean(df['close'],window=window)
    return df 
#trend 1:raise   0:down  1-0 sin
def trend(df,num=30):
    df1 = df[-30:]
    rate = len(df1[df1['macd_5'] > df1['macd_25']]) / 30
    return rate

def strategy(df):
    df.ix[(df['volume_signal'] == 1.0) & (df['ratio'] < 0.5),'buy'] = 1
    df.ix[df['close'] < df['macd_5'],'buy'] = 0
    df['buy'].fillna(method='pad',inplace=True)
    return df
    

def trend_1(df):
    ratio  = len(df[df['macd_5'] > df['macd_25']]) / len(df)
    return ratio
    
df = ts.get_k_data(code='002466',start='2016-01-01',end='2017-04-14')
df = df.set_index('date')
df = df[['close','volume']]
df = moving_average(df)
df['delta_ratio'] = (df['volume'] - df['volume_avg']) / df['volume_avg']
df['change'] = df['close'] / df['close'].shift(1) - 1.0
df['change'] = df['change'] * 100
df['delta_ratio'] = df['delta_ratio'] * 10
df['close_avg'] = pd.rolling_mean(df['close'],window=5)
df = macd(df,5)
df = macd(df,25)
df.ix[df['macd_5'] > df['macd_25'],'signal'] = 1
df['signal'].fillna(0,inplace=True)
df['ratio'] = pd.rolling_sum(arg=df['signal'],window=30) / 30
df.ix[(df['volume'] / df ['volume_avg'] -1) * 10 >10,'volume_signal'] = 1
df['volume_signal'].fillna(0,inplace=True)
df=df[df.index>'2016-03-01']
df =  strategy(df)
df.to_csv('test041703.csv')
#df[['close_avg','delta_ratio']].plot()

