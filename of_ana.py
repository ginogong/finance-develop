#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 21:18:03 2017

@author: Gino
"""

import tushare as ts 
import pandas as pd
token = 'f5bcd95440f205e0ecdb8bd6f7fdbb45eb4c868b8729d60a792acb0ef5c4367c'
ts.set_token(token)
#shibor
'''
df = ts.shibor_data()
df = df.set_index('date')
df_recent = df[df.index > '2017-09-01']
df_recent['ON'].plot()
'''

#bank price
'''
df = ts.get_deposit_rate()
'''

#fund info
fd = ts.getFundDivm(ticker='511660')
#of = fd.Fund(ticker='511660')
print fd