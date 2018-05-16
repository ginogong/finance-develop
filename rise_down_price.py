#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 09:14:51 2017

@author: Gino
"""
from __future__ import division
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')
PATH = '/Users/Gino/workspace/mysite/stock/stock/'
CODE = '002845'
def rise_stop(s):
    #df.index = range(len(df))
    #df['rs_price'] = np.round(df['close'].shift(1) * (1 + 0.1),2)
    #df['rs_price'].fillna(np.round(df.loc[0,'close'],2),inplace=True)
    return np.round(s.shift(1) * (1 + 0.1),2)
    
df = pd.read_hdf(PATH + 'dayk.h5','dayk')
df_temp  = df.groupby('code')
'''
df_temp['rs_price'] = df_temp['close'].shift(1) * (1 + 0.1)
df_temp['rs_price'] = np.round(df_temp['rs_price'],2)
df_temp['rs_price'].fillna(0,inplace=True)
print df_temp[df_temp['close']==df_temp['rs_price']]
'''
df['rs_price'] = df_temp.close.apply(rise_stop)

#df['rs_price'] = df_temp.close.transform(rise_stop)
print df.sort(['code','date'])[['code','date','close','rs_price']]