#-*- coding:utf-8 -*-
import pandas as pd 
import tushare as ts 

li = ['399300','000852']
df = ts.get_k_data('399300',start='2009-06-01',end='2017-02-20')
df['change'] = df['close'] / df['close'].shift(1) -1.0
df['change'].fillna(0,inplace=True)
df.to_hdf('all_index.h5','hs300')
