import tushare as ts 
import pandas as pd 
import numpy as np 
df_zz = pd.read_hdf('all_index.h5','zz1000')
df_hs = pd.read_hdf('all_index.h5','hs300')
df_hs.index = pd.to_datetime(df_hs.index)
df_hs = df_hs.sort_index()
columns = ['open','close','high','low','volume']
df_hs = df_hs[columns]
df_zz = df_zz[columns]
df_hs = df_hs.drop_duplicates()
df_hs = df_hs[1:]
df_hs.to_hdf('all_index.h5','hs300')
df_zz.to_hdf('all_index.h5','zz1000')
