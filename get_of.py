# -*- coding: utf-8 -*-
import tushare as ts 
import pandas as pd

df = ts.shibor_data()
df = df.set_index('date')
df_recent = df[df.index > '2017-09-01']
df_recent['ON'].plot()
