#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np 
import tushare as ts
import warnings
#----setting------
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)
#-----------------
index_name = ['all_a','hs300','zz1000']
#get data
def get_data(name,store='all_index.h5'):
	df = pd.read_hdf(store,name)
	return df 
#sort date set date index

def sort_dataframe(df,start='2010-01-01',end='2017-02-20'):
	df = df[df['date'] >= start]
	df = df[df['date'] <= end]
	df = df.set_index('date')
	return df 

#calculate future change
def future_change(df):
	period_list = [1,2,3,5]
	for i in period_list:
		name = 'furc' + str(i)
		class_name = 'cls' + str(i)
		df[name] = df['close'] / df['close'].shift(i) -1
		df[name] = df[name].shift(-i)
		df[class_name] = np.where(df[name]>0,1,-1)
	return df 

#get data
df_all = get_data(index_name[0])
df_hs300 = get_data(index_name[1])
df_hs300 = df_hs300[['date','open','high','low','close','volume','change']]
df_zz1000 = get_data(index_name[2])
df_zz1000 = df_zz1000[['date','open','high','low','close','volume','change']]

df_hs300 = future_change(df_hs300)
df_zz1000 = future_change(df_zz1000)
df_hs300 = sort_dataframe(df_hs300)
df_zz1000 = sort_dataframe(df_zz1000)

#class_label append label
class_label = df_all.copy()
class_label['hs_cls1'] = df_hs300['cls1']
class_label['hs_cls2'] = df_hs300['cls2']
class_label['hs_cls3'] = df_hs300['cls3']
class_label['hs_cls5'] = df_hs300['cls5']
class_label['zz_cls1'] = df_zz1000['cls1']
class_label['zz_cls2'] = df_zz1000['cls2']
class_label['zz_cls3'] = df_zz1000['cls3']
class_label['zz_cls5'] = df_zz1000['cls5']
class_label.to_hdf('ml.h5','label')
