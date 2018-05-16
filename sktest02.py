# -*- coding:utf-8 -*-
from sklearn import datasets
from sklearn import svm
import numpy as np 
from sklearn import neighbors
import tushare as ts 
import pandas as pd 
import warnings
warnings.filterwarnings('ignore')
code_list = ['399005','399300','399905']
range_list = [10, 20 ,40]
for cod in code_list:
	df = ts.get_k_data(code=cod,start='2010-06-01',end='2017-02-16')
	#calculate price change
	for i in range_list:
		name_roll = 'roll' + str(i)
		df[name_roll] = pd.rolling_mean(df['close'],window=i)
	df.to_csv(cod + 'test003' +'.csv') 
'''


def cal_org_data(df,rl):
	for i in rl:
		max_name  = 'max'  + str(i)
		min_name  = 'min'  + str(i)
		open_name = 'open' + str(i)
		tr_name   = 'tr'   + str(i)
		perf_name = 'perf' + str(i)
		next_name = 'next' + str(i)
	 	df[max_name]  = df['high'].rolling(i).max()
		df[min_name]  = df['low'].rolling(i).min()
		df[open_name] = df['open'].shift(i-1)
		df['c_h']     = abs(df[max_name] / df[open_name] - 1.0)
		df['h_l']     = abs(df[max_name] / df[min_name] -1.0)
		df['c_l']     = abs(df['close'] / df[open_name] -1.0)
		df[tr_name]   = df[['c_h','h_l','c_l']].max(axis=1)
		df[perf_name] = df['close'] / df[open_name] -1.0
		df[next_name] = df['close'].shift(-i) / df['close'] - 1.0
		df.pop(max_name)
		df.pop(min_name)
		df.pop(open_name)
		df.pop('c_h')
		df.pop('h_l')
		df.pop('c_l')
	return df
#calculate 
def cal_label(df,rl):
	for i in rl:
		label_name = 'label' + str(i)
		#perf_name = 'perf' + str(i)
		next_name = 'next' + str(i)
		three_point = df[next_name].quantile(0.3)
		seven_point = df[next_name].quantile(0.7)
		df.ix[df[next_name] > seven_point,label_name] = 1
		df.ix[df[next_name] < three_point,label_name] = -1
		df[label_name].fillna(0,inplace=True)
	return df

df = cal_org_data(df,range_list)
df = cal_label(df,range_list)
df = df[df['date'] > '2011-01-01']
#df2.to_csv('mltest011.csv',index=False)
df['tr10'] = (df['tr10'] - df['tr10'].min()) / (df['tr10'].max() - df['tr10'].min())
df['tr20'] = (df['tr20'] - df['tr20'].min()) / (df['tr20'].max() - df['tr20'].min())
df['tr40'] = (df['tr40'] - df['tr40'].min()) / (df['tr40'].max() - df['tr40'].min())
df['perf10'] = (df['perf10'] - df['perf10'].min()) / (df['perf10'].max() - df['perf10'].min())
df['perf20'] = (df['perf20'] - df['perf20'].min()) / (df['perf20'].max() - df['perf20'].min())
df['perf40'] = (df['perf40'] - df['perf40'].min()) / (df['perf40'].max() - df['perf40'].min())
df = df[['date','tr10','tr20', 'tr40','perf10','perf20','perf40','label10','label20','label40']]
df1 = df[df['date'] < '2016-01-01']
df2 = df[df['date'] >= '2016-01-01']
k_list = []
ratio_list = []
weight_list = []
rng_list = []
for i in range(5,100):
	for wghts in ['uniform', 'distance']:
		for label in range_list:
			label_name = 'label' + str(label)
			clf = neighbors.KNeighborsClassifier(i,weights=wghts)
			clf.fit(df1[['tr10','tr20', 'tr40','perf10','perf20','perf40']], df1[label_name])
			z = clf.predict(df2[['tr10','tr20', 'tr40','perf10','perf20','perf40']])
			name = wghts + 'pre'
			com_name = wghts + 'com'
			df2[name] = z
			num_right = len(df2[df2[label_name] == df2[name]])
			num_total = len(df2)
			ratio = float(num_right) / num_total
			k_list.append(i)
			weight_list.append(wghts)
			rng_list.append(label)
			ratio_list.append(ratio)

summary = pd.DataFrame({'k':k_list, 'type':weight_list,'range':rng_list,'ratio':ratio_list})
df2.to_csv('mltest015.csv',index=False)
summary.to_csv('summary001.csv')
'''







