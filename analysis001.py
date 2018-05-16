# -*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import warnings 
import numpy as np
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)

df_all = pd.read_hdf('all_index.h5','all_a')
df_hs = pd.read_hdf('all_index.h5','hs300')
df_zz = pd.read_hdf('all_index.h5','zz1000')
def split_data(df,start='2013-01-01',end='2017-03-07'):
	df = df[df.index >= start]
	df = df[df.index <= end]
	return df 

df_all = split_data(df_all)
df_hs  = split_data(df_hs)
df_zz  = split_data(df_zz)

df_all['hs'] = df_hs['close']
df_all['zz'] = df_zz['close']
df_all['hs_change'] = df_all['hs'] / df_all['hs'].shift(1) - 1.0
df_all['zz_change'] = df_all['zz'] / df_all['zz'].shift(1) - 1.0
df_all.ix[0,['hs_change','zz_change']] = 0 
df_all.to_csv('all_analysis003.csv')
