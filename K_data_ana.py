#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 10:02:01 2017

@author: Gino
"""

from __future__ import division
import pandas as pd 
import concat_dataframe
import datetime
import tushare as ts 

PATH = '/Users/Gino/workspace/mysite/stock/stock/'
def ma5(s):
    return pd.rolling_mean(s,5,min_periods=1)
def ma20(s):
    return pd.rolling_mean(s,20,min_periods=1)
'''
df = concat_dataframe.concat_dataframe()
code_list = list(df.code.unique())
now = datetime.datetime.now().strftime('%Y-%m-%d')
df_temp = df[df['code']=='002845']
df_temp.index = range(len(df_temp))
df_grouped = df.groupby('code')
   
df['ma5'] = df_grouped.close.transform(ma5)
df['ma20'] = df_grouped.close.transform(ma20)
df['ma5_close']  = df['close'] - df['ma5']
df['ma20_close'] = df['close'] - df['ma20']
df_temp =  df[df['date'] == now]
'''
df = ts.get_stock_basics()
columns = ['name','industry','pe','outstanding','reservedPerShare','esp','gpr']
df_temp =  df[(df['timeToMarket']>20170901)&(df['timeToMarket']<20171020)][columns]
df_temp = df_temp[df_temp['outstanding']<1]
df_highres =  df[df['reservedPerShare']>6]
df_highres = df_highres[df_highres['outstanding']<1]
df_highres = df_highres[df_highres['pe']<100]
df_highres = df_highres.sort_values(by='reservedPerShare')
print df_temp
#df_temp.to_csv(PATH+'recent1110.csv')
#df.to_csv(PATH+ 'all1110.csv')






