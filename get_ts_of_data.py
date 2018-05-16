#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 18:24:00 2017

@author: Gino
"""

import tushare as ts 
import pandas as pd


conn = ts.get_apis()
PATH = '/Users/Gino/workspace/mysite/stock/stock/'
def get_of_data(code_name,start,end):
    df = ts.get_k_data(code=code_name,start=start,end=end,ktype='5')
    return df
    
def get_of_bar(code,conn,freq,start,end):
    df = ts.bar(code=code,conn=conn,freq=freq,start_date=start,end_date=end)
    return df
start_date = '2015-01-01'
end_date = '2017-10-25'
freq = '5min'
of_list = ['511660','511810','511990','511900']
columns = ['open','close','high','low','vol','code','amount']
df = pd.DataFrame([],columns=columns)

for code in of_list:
    df_temp = get_of_bar(code,conn,freq,start_date,end_date)
    df = pd.concat([df,df_temp])

df.to_hdf(PATH+'of.h5','of_M5')
print df