from __future__ import division
import tushare as ts 
import pandas as pd


# date        open close high low volume      code
#2009-01-01   7.89 7.89  7.89 7.89 587096.25  600000

index_list = ['399300','000852']
start = '2017-04-14'
end   = '2017-04-14'
'''
df = pd.read_hdf('dayk.h5','dayk')
stocklist = pd.read_hdf('stocklist.h5','stocklist')


columns = ['date','open','close','high','low','volume','code']
df_new = pd.DataFrame(columns=columns)
for i in range(len(stocklist)):
	df_temp = ts.get_k_data(code=stocklist.ix[i,'stocklist'],start=start,end=end)
	df_new = pd.concat([df_new,df_temp])
	print '%s done' % i

df = pd.concat([df,df_new])
df = df.drop_duplicates()
df.to_hdf('dayk.h5','dayk')

index_name = ['all_a','hs300','zz1000']
df =  pd.read_hdf('all_index.h5','hs300')
df_temp = ts.get_k_data(code=index_list[0],start=start,end=end,index=True)
df_temp['date'] = df_temp['date'].astype('datetime64')
df_temp = df_temp.set_index('date')

df = pd.concat([df,df_temp[['open','close','high','low','volume']]])
df = df.drop_duplicates()
df = df.sort_index()
print df 
df.to_hdf('all_index.h5','hs300')
'''

df2 = pd.read_hdf('all_index.h5','zz1000')
df_temp2 = ts.get_k_data(code=index_list[1],start=start,end=end,index=True)
df_temp2['date'] = df_temp2['date'].astype('datetime64')
df_temp2 = df_temp2.set_index('date')

df2 = pd.concat([df2,df_temp2[['open','close','high','low','volume']]])
df2 = df2.drop_duplicates()
df2 = df2.sort_index()

df2.to_hdf('all_index.h5','zz1000')
print len(df2)

'''
df = pd.read_csv('000852 (1).csv',parse_dates=[0])
df = df[['date','open','close','high','low','volume']]
#df['date'] = df['date'].astype('datetime64')
df = df.set_index('date')
df = df.sort_index()
df = df[df.index>='2009-06-02']
df.to_hdf('all_index.h5','zz1000')
'''