# -*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 

def max_dd(df,window=27):

	#df = df.set_index('date')
	for i in range(len(df) - window):
		df1 = df[i:window+i]
		dd_temp = 0
		max_temp = 0
		min_temp = 100000000
		for j in range(len(df1)):			
			if df1.ix[j,'high'] > max_temp:
				max_temp = df1.ix[j,'high']
				min_temp = df1.ix[j,'low']
			else:
				max_temp = max_temp
			if df1.ix[j,'low'] < min_temp:
				min_temp = df1.ix[j,'low']
			else:
				min_temp = min_temp
			if dd_temp > (min_temp / max_temp - 1.0) :
				dd_temp = min_temp / max_temp - 1.0
			else:
				dd_temp = dd_temp
		df.ix[window+i,'maxdd'] = dd_temp
	return df 



