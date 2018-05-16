# -*- coding: utf-8 -*-
from __future__ import division
import pybacktest
import pandas as pd
import tushare as ts 

df = pd.read_csv('000852.csv',parse_dates=['date'])
df = df[['date','code','open','high','low','close','change','volume']]
df['code'] = '000852'
df = df.sort_values(by='date')
df = df[df['date'] > '2009-06-01' ]
df = df[:-1]
df['change'] = df['close'] / df['close'].shift(1) - 1.0
df['change'].fillna(0,inplace=True)
df.to_hdf('all_index.h5','zz1000')


