#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:17:26 2017

@author: Gino
"""

from __future__ import division
import pandas as pd
import tushare as ts 
import numpy as np
import datetime as dt

def conti_rise(df,shift_num=2):
    df.index = range(len(df))
    index_list = ['date','open','close','high','low','change']
    df.loc[df['change'] > 0,'rise_label'] = 1
    df.loc[df['change'] <= 0,'rise_label'] = 0
    df_down = df[df['rise_label']==0].index
    df.loc[df.index[0],'conti_rise'] = 1
    for index in range(len(df)):
        if index>= 1:
            df.loc[index,'conti_rise'] = df.loc[index,'rise_label'] * (df.loc[index-1,'conti_rise'] + df.loc[index,'rise_label'])


    return df
    
def conti_change(df):
    df.index = range(len(df))
    df['close_low_rate'] = df['close'] / df['low']
    df['t2_count'] = df['rise_label'].shift(1) + df['rise_label'].shift(2)
    df['t2_count'].fillna(0,inplace=True)
    return df
path = '/Users/Gino/workspace/mysite/stock/stock/'
df = pd.read_hdf(path+'dayk_down.h5','dayk_down')
df.index = range(len(df))
df_index = df.copy()
df_index['change'] = df_index.groupby('code').close.pct_change()
nan_index = pd.isnull(df_index['change'] )
df_index.loc[nan_index,'change'] = df_index.loc[nan_index,'close']/df_index.loc[nan_index,'open'] - 1.0
df_group = df_index.groupby('code')

columns = ['date','open','close','high','low','change','rise_label','conti_rise']

#df_new = df_group.apply(conti_rise)
df_new = df_group.apply(conti_change)
df_new.index = range(len(df_new))  
print df_new
df_new.to_hdf(path+'dayk_down.h5','dayk_down')