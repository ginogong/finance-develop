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

classify_start = '2013-04-12'
classify_end = '2017-03-29'
classify_data = split_data(data1,start=classify_start,end=classify_end)
classify_label = split_data(label,start=classify_start,end=classify_end)


label1 = []
label2 = []
num = 30

times = int(round(len(classify_data) / num )) + 1
hs_list = ['all_hs_change','all_zz_change','hs_zz_amp20','hs_zz_chg10','hs_zz_sma40','hs_zz_vol40']
zz_list = ['all_hs_change','all_zz_change','hs_zz_amp40','hs_zz_chg20','hs_zz_sma10','hs_zz_vol10']
training1 = training_data[hs_list]
training2 = training_data[zz_list]
for i in range(times):
	srt_num =  i * num
	end_num = (i + 1 )* num
	classify_temp = classify_data[srt_num:end_num]
	classify_label_temp = classify_label[srt_num:end_num]
	if len(classify_label_temp) > 0:
		clf1 = neighbors.KNeighborsClassifier(7,weights='uniform')
		clf1.fit(training1,training_label['hs_cls1'])
		clf2 = neighbors.KNeighborsClassifier(27,weights='uniform')
		clf2.fit(training2,training_label['zz_cls1'])
		z1 = clf1.predict(classify_temp[hs_list])
		label1.extend(z1)
		z2 = clf2.predict(classify_temp[zz_list])
		label2.extend(z2)
		training1 = pd.concat([training1 ,classify_temp[hs_list]])
		training2 = pd.concat([training2 ,classify_temp[zz_list]])
		training_label = pd.concat([training_label,classify_label_temp])
classify_label['hs_pre'] = label1
classify_label['zz_pre'] = label2

classify_label.to_csv('knn'+ str(num) +'_0402.csv')


