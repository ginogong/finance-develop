#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 20:56:49 2017

@author: Gino
"""
from __future__ import division
import pandas as pd 
import concat_dataframe

PATH = '/Users/Gino/workspace/mysite/stock/stock/'
def rolling_mean(df):
    return df.rolling(window=60,min_periods=1).mean()

df = concat_dataframe.concat_dataframe()
days = 60
df['macd60'] = df.groupby('code')['close'].transform(rolling_mean)
df_temp = df[df['date']=='2017-11-24']
print df_temp[df_temp['macd60']<df_temp['close']]