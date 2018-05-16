#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:45:33 2017

@author: Gino
"""
from __future__ import division
import pickle
import pandas as pd 

PATH = '/Users/Gino/workspace/mysite/stock/stock/'
df = pd.read_hdf('dayk.h5','dayk')
f = open(PATH + 'conception.txt','r')
conception_dict = pickle.load(f)
j = 0
df_temp = df[df['date'] > '2017-01-01']


df_code_list = pd.DataFrame({'code':conception_dict['OLED']})
df_conception = pd.merge(df_temp,df_code_list,how='left',on=['code'])
df_conception['change'] = df_conception.groupby('code').close.pct_change()

df_oled = df_conception.groupby('date').mean()
df_oled = df_oled.reset_index()
df_oled = df_oled[['date','change']]
df_oled.loc[0,'oled_index'] = 1000
for i in range(len(df_oled)):
    if i > 0 :
        df_oled.loc[i,'oled_index'] = df_oled.loc[i-1,'oled_index'] * (1.0 + df_oled.loc[i,'change'])
df1 = df_conception[df_conception['code'] == '002845'][['date','code','change']]
df2 = pd.merge(df1,df_oled,how='left',on=['date'])
df2 = df2[df2['date']>= '2017-07-01']
df2.fillna(0,inplace=True)
df2['change_x_sum'] = df2['change_x'].cumsum()
df2['change_y_sum'] = df2['change_y'].cumsum()
df2['change_bias'] = df2['change_x_sum'] - df2['change_y_sum']
df2['change_bias'].plot()