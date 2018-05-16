# -*- coding: utf-8 -*-
import pybacktest
import pandas as pd
import tushare as ts 
'''
ohlc = pybacktest.load_from_yahoo('SPY')
short_ma = 50  
long_ma = 200  
ms = pandas.rolling_mean(ohlc.C, short_ma)  
ml = pandas.rolling_mean(ohlc.C, long_ma)  
buy = cover = (ms > ml) & (ms.shift() < ml.shift())  # ma cross up  
sell = short = (ms < ml) & (ms.shift() > ml.shift())  # ma cross down  
  
bt = pybacktest.Backtest(locals(), 'ma_cross')
bt.summary()
'''
df = pd.read_csv('000852.csv',parse_dates=['date'])
df = df[['date','code','open','high','low','close','change','volume']]
df['code'] = '000852'
#df['date'] =  df['date'].apply(lambda x:x.replace('/','-'))
df = df.sort_values(by='date')
df = df[df['date'] > '2009-06-01' ]
df = df[:-1]
df.to_hdf('all_index.h5','zz1000')


