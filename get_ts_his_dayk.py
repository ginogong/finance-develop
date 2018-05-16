#-*- coding:utf-8 -*-
import tushare as ts 
import pandas as pd 

start = '2017-01-01'
end = '2017-08-21'
start1 = '2009-06-01' 
end1 = '2013-12-31'
start2 = '2014-01-01' 
end2 =  '2016-12-31'
stock_list = pd.read_hdf('stocklist.h5','stocklist')
#df = ts.get_k_data(code=stock_list.ix[0,'stocklist'], start=start,end=end)
#df_dayk = pd.read_hdf('dayk.h5','dayk')
#mask = df_dayk[df_dayk['date']==end]
#df_dayk = df_dayk.drop(mask)

columns = ['date','open','close','high','low','volume','code']
df_temp = pd.DataFrame(columns=columns)
df_dayk = pd.DataFrame(columns=columns)
for i in range(len(stock_list)):
	df = ts.get_k_data(code=stock_list.ix[i,'stocklist'], start=start,end=end)
	df_temp = df_temp.append(df)
	print stock_list.ix[i,'stocklist'] + 'done!'
df_dayk = df_dayk.append(df_temp)
df_dayk = df_dayk.drop_duplicates()
df_dayk = df_dayk.sort_values('date')

df_dayk.to_hdf('dayk_17.h5','dayk_17')

'''
df_day = pd.read_hdf('all_index.h5','hs300')
df_temp = ts.get_h_data('399300',index=True,start='2017-05-18',end='2017-05-18')[df_day.columns]
df_day = pd.concat([df_day,df_temp])
df_day = df_day.sort_index()
#df_day.to_hdf('all_index.h5','hs300')

df_temp = ts.get_h_data('000852',index=True,start='2017-05-18',end='2017-05-18')[df_day.columns]
df_day = pd.concat([df_day,df_temp])
df_day = df_day.sort_index()
#df_day.to_hdf('all_index.h5','zz1000')
'''