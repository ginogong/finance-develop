#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np 
import tushare as ts
import warnings
from sklearn import neighbors
#----setting------
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)
#-----------------
galaxy_start = '2013-04-12'
galaxy_end = '2017-03-28'
#get data
data = pd.read_hdf('ml.h5','feature002')
data.pop('change')
data.pop('all_a')
col_data = list(data.columns)
label = pd.read_hdf('ml.h5','label002')
label.pop('change')
label.pop('all_a')

#---- split data set
def split_data(df,start='2010-01-04',end='2014-12-30'):
	df = df[df.index >= start]
	df = df[df.index <= end]
	return df
def auto_norm(df):
	df1 = df.copy()
	for i in  list(df.columns):
		df1[i] = (df[i] - df[i].min()) / (df[i].max() - df[i].min())
	return df1
data1 = auto_norm(data)
training_data = split_data(data1,end='2013-04-11')
training_label = split_data(label,end='2013-04-11')

classify_data = split_data(data1,start=galaxy_start,end=galaxy_end)
classify_label = split_data(label,start=galaxy_start,end=galaxy_end)

hs_list = ['all_hs_change','all_zz_change','hs_zz_amp20','hs_zz_chg10','hs_zz_sma40','hs_zz_vol40']
zz_list = ['all_hs_change','all_zz_change','hs_zz_amp40','hs_zz_chg20','hs_zz_sma10','hs_zz_vol10']

clf = neighbors.KNeighborsClassifier(7,weights='distance')
clf.fit(training_data[hs_list],training_label['hs_cls1'])
z = clf.predict(classify_data[hs_list])
classify_label['hs_pre'] = z 
clf1 = neighbors.KNeighborsClassifier(27,weights='distance')
clf1.fit(training_data[zz_list],training_label['zz_cls1'])
z1 = clf1.predict(classify_data[zz_list])
classify_label['zz_pre'] = z1
print classify_label.tail(10)
#classify_label.to_csv('knn_0329_01.csv')


