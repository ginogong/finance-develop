#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np 
import tushare as ts
import warnings
import datetime
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

def sort_dataframe(df,start='2010-01-01',end='2017-03-13'):
	df = df[df.index >= start]
	df = df[df.index <= end]
	return df 

#calculate future change
def future_change(df):
	period_list = [1]
	for i in period_list:
		name = 'furc' + str(i)
		class_name = 'cls' + str(i)
		df[name] = df['close'] / df['close'].shift(i) -1
		df[name] = df[name].shift(-i)
		df[class_name] = np.where(df[name]>0,1,-1)
	return df 

now = datetime.datetime.now().strftime('%Y-%m-%d')
#now = '2017-04-21'
#get data
df_all = get_data(index_name[0])
df_hs300 = get_data(index_name[1])
df_zz1000 = get_data(index_name[2])

df_hs300 = future_change(df_hs300)
df_zz1000 = future_change(df_zz1000)

df_hs300 = sort_dataframe(df_hs300,end=now)
df_zz1000 = sort_dataframe(df_zz1000,end=now)
df_all = sort_dataframe(df_all,end=now)


#class_label append label
class_label = df_all.copy()

class_label['hs_cls1'] = df_hs300['cls1']

class_label['zz_cls1'] = df_zz1000['cls1']

class_label.to_hdf('ml.h5','label002')

