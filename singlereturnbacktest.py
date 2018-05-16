from __future__ import division
import pandas as pd 
import tushare as ts
import rollingmaxdd
import numpy as np 

def max_dd(df,window=27):
	for i in range(len(df) - window):
		df1 = df[i:window+i]
		dd_temp = 0
		max_temp = 0
		min_temp = 100000000
		for j in range(len(df1)):			
			if df1.ix[j,'mini'] > max_temp:
				max_temp = df1.ix[j,'mini']
				min_temp = df1.ix[j,'mini']
			else:
				max_temp = max_temp
			if df1.ix[j,'mini'] < min_temp:
				min_temp = df1.ix[j,'mini']
			else:
				min_temp = min_temp
			if dd_temp > (min_temp / max_temp - 1.0) :
				dd_temp = min_temp / max_temp - 1.0
			else:
				dd_temp = dd_temp
		df.ix[window+i,'maxdd'] = dd_temp
	return df

def account(df):
	df.ix[0,'cap_return'] = 0
	df.ix[df['position'] == df['position'].shift(1),'cap_return'] = df['change'] * df['position']
	df.ix[df['position'] != df['position'].shift(1),'cap_return'] = df['change']
	return df
#calculate max drawdown
def max_drawdown(df):
	date_line = df.index
	capital_line = df['capital']
	df = pd.DataFrame({'date':date_line, 'capital':capital_line})
	df['max2here'] = pd.expanding_max(df['capital']) # calc expanding max
	df['dd2here']  = df['capital'] / df['max2here'] - 1.0 # calculate day drawdown

	#calculate max draw down ,date
	temp     = df.sort_values(by='dd2here').iloc[0][['date','dd2here']]
	max_dd   = temp['dd2here']
	end_date = temp['date']
	#end_date_name = end_date.strftime('%Y-%m-%d')

	#calculate days
	df = df[df['date'] < end_date]
	start_date = df.sort_values(by='capital',ascending=False).iloc[0]['date']
	#start_date_name = start_date.strftime('%Y-%m-%d')
	#last_days = str(start_date - end_date)
	print 'max draw down: %f, start date: %s, end date: %s' % (max_dd,start_date,end_date)
	return max_dd,start_date,end_date
max_dd_list = []
start_date_list = []
end_date_list = []
total_return = []
date_list = []
thre_list = []
number_list = [32]
threshold_list = [-0.123]
df = pd.read_excel('mini_zz.xls',sheet='mini')
df = df.set_index('date')
df['change'] = df[u'mini'] / df[u'mini'].shift(1) - 1.0
df.ix[0,'change'] = 0
df.ix['2016-01-04','change'] = 0
df.ix['2016-01-07','change'] = 0

for number in number_list:
	df = max_dd(df,window=number)
	for threshold in threshold_list:
		df.ix[df['maxdd'] > threshold,'position'] = 1
		df.ix[df['maxdd'] <= threshold,'position'] = 0
		df['position'].fillna(0,inplace=True)
		df = account(df)
		df['capital'] = (df['cap_return'] + 1).cumprod()
		df.to_csv('mini_zz_ownshield_worth003.csv')
		l1,l2,l3 = max_drawdown(df)
		date_list.append(number)
		thre_list.append(threshold)
		max_dd_list.append(l1)
		start_date_list.append(l2)
		end_date_list.append(l3)
		total_return.append(df.ix[-1,'capital'])
df_result = pd.DataFrame({'start':start_date_list,'end':end_date_list,\
						  'max_dd':max_dd_list,'return':total_return,'date_num':date_list,'threshold':thre_list})
df_result = df_result[['date_num','threshold','start','end','max_dd','return']]
#df_result.to_csv('mini_zz_ownshield004.csv')





