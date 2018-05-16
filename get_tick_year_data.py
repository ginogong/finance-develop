import tushare as ts 
import pandas as pd 
import datetime

now = datetime.datetime.now().strftime('%Y-%m-%d')


date_2013 = ['2013-01-01','2013-12-31']
date_2014 = ['2014-01-01','2014-12-31']
date_2015 = ['2015-01-01','2015-12-31']
date_2016 = ['2016-01-01','2016-12-31']
date_2017 = ['2017-01-01','2017-03-24']
dates = [date_2013,date_2014,date_2015,date_2016,date_2017]

df_temp = pd.DataFrame(columns=['date','time','price','volume','amount'])
for date in dates:
	df_temp = pd.DataFrame(columns=['date','time','price','volume','amount'])
	df1 = pd.read_hdf('all_index.h5','hs300')
	date_list = df1[df1.index>= date[0] ]
	date_list = date_list[date_list.index <= date[1]].index
	date_list =  list(date_list)
	name = date[0]
	for i in date_list:

		date = i.strftime('%Y-%m-%d')
		print date
		df = ts.get_tick_data('204001',date=date)
		if len(df) > 5:
			df['date'] = date
			df = df[['date','time','price','volume','amount']]
			df_temp = pd.concat([df_temp,df])
			#print df_temp
	df_temp = df_temp.drop_duplicates()
	df_temp.to_csv('tickdata__204001_' + name + '.csv')
	print name + ' finished'
