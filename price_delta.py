#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 10:47:45 2017

@author: Gino
"""
from __future__ import division
import pandas as pd 
import tushare as ts
import matplotlib
matplotlib.style.use('ggplot')

PATH = '/Users/Gino/workspace/mysite/stock/stock/' 
CODE = '002845'
#计算周期内的加权平均价格
def rolling_weight_price(dataframe,num=30):
    dataframe.index = range(len(dataframe))
    dataframe['price_avg'] = dataframe[['open','close','high','low']].mean(axis=1)
    dataframe['price_avg_change'] = dataframe['price_avg'] - dataframe['price_avg'].shift(1)
    dataframe['price_avg_change'].fillna(0,inplace=True)
    dataframe['volume_change'] = dataframe['volume'] - dataframe['volume'].shift(1)
    dataframe['volume_change'].fillna(0,inplace=True)
    dataframe.loc[0,'weight_price'] = dataframe.loc[0,'open']
    dataframe['rate'] = dataframe['outstand']/dataframe['outstand'].shift(1)
    dataframe['rate'].fillna(1,inplace=True)
    for i in range(len(dataframe)):
        if i >0:
            rate = dataframe.loc[i,'rate']
            dataframe.loc[i,'weight_price'] = (dataframe.loc[i,'price_avg'] \
                * dataframe.loc[i,'volume'] + (dataframe.loc[i,'outstand']*100*rate - \
                dataframe.loc[i,'volume']) *dataframe.loc[i-1,'weight_price'])\
                / (dataframe.loc[i,'outstand']*100*rate)
            
    #dataframe.loc
    return dataframe
#填充流通股本
def forward_fill(s):
    s = s.fillna(method='ffill')
    s = s.fillna(method='bfill')
    return s
df = pd.read_hdf(PATH + 'dayk.h5','dayk')
df.index = range(len(df))
df_outstand = pd.read_hdf(PATH+'outstand.h5','outstand')
df = pd.merge(df,df_outstand,how='left',on=['code','date'])
df_group = df.groupby('code')
df['outstand'] = df.groupby('code').outstand.apply(forward_fill)
df_temp = df[df['code']==CODE]
#print df_temp
df_temp = rolling_weight_price(df_temp)[-200:]
print df_temp[-1:]
df_temp[['close','weight_price']].plot()
#df['price_avg'] = df[['open','close','high','low']].mean(axis=1)
#df['avg_change'] = df['price_avg'] - df['price_avg'].shift(1)
#df['avg_change'].fillna(0,inplace=True)
#df['volume_change'] = df['volume'] - df['volume'].shift(1)
#df['volume_change'].fillna(0,inplace=True)


