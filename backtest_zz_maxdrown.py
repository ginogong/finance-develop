# -*- coding:utf-8 -*-
import pandas as pd 
import numpy as np 
import tushare as ts 
import warnings
from rollingmaxdd import max_dd
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)

#sma strategy 
def sma_strategy(stock_data, short_ma=5,long_ma=30):
	stock_data['short_ma'] = pd.rolling_mean(stock_data['close'],short_ma,min_periods=1)
	stock_data['long_ma']  = pd.rolling_mean(stock_data['close'],long_ma, min_periods=1)
	stock_data.ix[(stock_data['short_ma'].shift(1) > stock_data['long_ma'].shift(1)) &
				  (stock_data['short_ma'].shift(2) <= stock_data['long_ma'].shift(2)) &
				  (stock_data['open'] < stock_data['close'] * 1.094), 'postion'] = 1

	stock_data.ix[(stock_data['short_ma'].shift(1) < stock_data['long_ma'].shift(1)) &
				  (stock_data['short_ma'].shift(2) >= stock_data['long_ma'].shift(2)) &
				  (stock_data['open'] > stock_data['close'].shift(1) * 0.906), 'postion'] = 0
	stock_data['postion'].fillna(method='pad',inplace=True)
	stock_data['postion'].fillna(0,inplace=True)
	#stock_data.to_csv('test005.csv')
	return stock_data[['date','code','open','close', 'change','postion']]

#calculate return 
def account(dataframe):
	dataframe.ix[0,'cap_ret'] = 0
	dataframe.ix[dataframe['postion'] > dataframe['postion'].shift(1), 'cap_ret' ] = dataframe['close'] / dataframe['open'] - 1.0
	dataframe.ix[dataframe['postion'] < dataframe['postion'].shift(1), 'cap_ret' ] = dataframe['open'] / dataframe['close'].shift(1) -1.0
	dataframe.ix[dataframe['postion'] == dataframe['postion'].shift(1), 'cap_ret' ] = dataframe['change'] * dataframe['postion']
	#dataframe.to_csv('test007.csv',index=False)
	return dataframe

#choose date field
def select_data_range():
	pass

def period_return(stock_data, days=250):


	#calc every year, month ,week capital return
	year_ret  = stock_data[['change','cap_ret']].resample('A', how=lambda x :(x + 1.0).prod() - 1.0)
	month_ret = stock_data[['change','cap_ret']].resample('M', how=lambda x :(x + 1.0).prod() - 1.0)
	week_ret  = stock_data[['change','cap_ret']].resample('W', how=lambda x :(x + 1.0).prod() - 1.0)
	year_ret.fillna(0,inplace=True)
	month_ret.fillna(0,inplace=True)
	week_ret.fillna(0,inplace=True)

	#calc  strategy win ratio 
	yearly_win_rate  = float(len(year_ret[year_ret['cap_ret'] > 0])) / len(year_ret[year_ret['cap_ret'] != 0])
	monthly_win_rate = float(len(month_ret[month_ret['cap_ret'] > 0])) / len(month_ret[month_ret['cap_ret'] != 0])
	weekly_win_rate  = float(len(week_ret[week_ret['cap_ret'] > 0])) / len(week_ret[week_ret['cap_ret'] != 0])

	#calc stock win ratio
	stock_yearly_win_rate  = float(len(year_ret[year_ret['change'] > 0])) / len(year_ret[year_ret['change'] != 0])
	stock_monthly_win_rate = float(len(month_ret[month_ret['change'] > 0])) / len(month_ret[month_ret['change'] != 0])
	stock_weekly_win_rate  = float(len(week_ret[week_ret['change'] > 0])) / len(week_ret[week_ret['change'] != 0])

	#output debug
	'''
	year_ret.to_csv('year_ret_test003.csv')
	month_ret.to_csv('month_ret_test003.csv')
	week_ret.to_csv('week_ret_test003.csv')
	recent_ret_line.to_csv('recent_ret_linetest003.csv')
	'''



	if len(year_ret) :
		print '\nrecent strategy and stock performance:'
		#print recent_ret_line
		#print '\npast every years return:'
		#print year_ret
		print '\nstrategy yearly win rate: %f' % yearly_win_rate
		print '\nstock yearly win rate: %f'    % stock_yearly_win_rate
		#print '\npast every month return:'
		#print month_ret
		print '\nstrategy monthly win rate: %f' % monthly_win_rate
		print '\nstock mongthly win rate: %f'   % stock_monthly_win_rate
		#print '\npast every week return:'
		#print week_ret
		print '\nstrategy weekly win rate: %f' % weekly_win_rate
		print '\nstock weekly win rate: %f'  %   stock_weekly_win_rate
	return year_ret, month_ret, week_ret

def trade_describe(df):

	#calc capital return 
	df['capital'] = (df['cap_ret'] + 1.0).cumprod()

	#record date ,capital when buy]
	df.ix[df['postion'] > df['postion'].shift(1), 'start_date'] = df['date']
	df.ix[df['postion'] > df['postion'].shift(1), 'start_capital'] = df['capital'].shift(1)
	df.ix[df['postion'] > df['postion'].shift(1), 'start_stock'] = df['open']

	#record  date,capital when sell
	df.ix[df['postion'] < df['postion'].shift(1), 'end_date'] = df['date']
	df.ix[df['postion'] < df['postion'].shift(1), 'end_capital'] = df['capital']
	df.ix[df['postion'] < df['postion'].shift(1), 'end_stock'] = df['open']

	#debug output
	#df.to_csv('describetest003.csv',index=False)

	#trade info combine
	df_temp = df[df['start_date'].notnull() | df['end_date'].notnull()]

	df_temp['end_date']    = df_temp['end_date'].shift(-1)
	df_temp['end_capital'] = df_temp['end_capital'].shift(-1)
	df_temp['end_stock']   = df_temp['end_stock'].shift(-1)
	#df_temp.to_csv('temptest002.csv',index=False)

	#account trade information
	trade = df_temp.ix[df_temp['end_date'].notnull(),['start_date', 'start_capital', 'start_stock',
													  'end_date', 'end_capital', 'end_stock']]
	trade['hold_time']    = (trade['end_date'] - trade['start_date']).dt.days
	trade['trade_return'] = trade['end_capital'] / trade['start_capital'] - 1.0
	trade['stock_return'] = trade['end_stock'] / trade['start_stock'] - 1.0  #meaningless 
	#trade.to_csv('tradetest002.csv',index=False)

	trade_num      = len(trade) #calc trade times
	max_holdtime   = trade['hold_time'].max() #calc the longest holding days
	average_change = trade['trade_return'].mean() # calc average change
	max_gain       = trade['trade_return'].max() # calc max gain
	max_loss       = trade['trade_return'].min() #calc max loss
	total_years    = (trade['end_date'].iloc[-1] - trade['start_date'].iloc[0]).days / 365
	trade_per_year = trade_num / total_years # trade number per year

	#contineous loss
	trade.ix[trade['trade_return'] > 0 , 'gain'] = 1
	trade.ix[trade['trade_return'] < 0 , 'gain'] = 0
	#trade.to_csv('tradetest003.csv', index=False)
	#trade.fillna(method='ffill', inplace=True)

	ret_list = list(trade['gain'])
	suc_gain_list = []
	num = 1
	for i in range(len(ret_list)):
		if i == 0:
			suc_gain_list.append(num)
		else:
			if (ret_list[i] == ret_list[i-1] == 1) or (ret_list[i] == ret_list[i-1] == 0) :
				num += 1
			else:
				num = 1
			suc_gain_list.append(num)

	trade['suc_gain'] = suc_gain_list

	max_suc_gain = trade[trade['gain'] == 1].sort_values(by='suc_gain',ascending=False)['suc_gain'].iloc[0]
	max_suc_loss = trade[trade['gain'] == 0].sort_values(by='suc_gain',ascending=False)['suc_gain'].iloc[0]


	#print '\n==========trade performance=========='
	#print trade[['start_date','end_date','trade_return','stock_return']]
	print '\n==========account summary=========='
	print 'trade numbers: %d, the largest holding days: %d' % (trade_num, max_holdtime)
	print 'average change: % f' % average_change
	print 'max gain: %f, max_loss: %f' % (max_gain, max_loss)
	print 'trade times per year : %d' % trade_per_year
	print 'tradings of max contineous gain : %d, tradings of max contineous loss: %d' % (max_suc_gain, max_suc_loss)
	return trade

#calculate annual return
def annual_return(date_line,capital_line):
	#combine to dataframe
	df = pd.DataFrame({'date':date_line, 'capital':capital_line})
	annual = (float(df['capital'].iloc[-1]) / df['capital'].iloc[0]) ** (250.0/len(df)) - 1.0
	return annual

#calculate max drawdown
def max_drawdown(date_line,capital_line):

	df = pd.DataFrame({'date':date_line, 'capital':capital_line})
	df['max2here'] = pd.expanding_max(df['capital']) # calc expanding max
	df['dd2here']  = df['capital'] / df['max2here'] - 1.0 # calculate day drawdown

	#calculate max draw down ,date
	temp     = df.sort_values(by='dd2here').iloc[0][['date','dd2here']]
	max_dd   = temp['dd2here']
	end_date = temp['date']
	end_date_name = end_date.strftime('%Y-%m-%d')

	#calculate days
	df = df[df['date'] < end_date]
	start_date = df.sort_values(by='capital',ascending=False).iloc[0]['date']
	start_date_name = start_date.strftime('%Y-%m-%d')
	last_days = str(start_date - end_date)
	#print 'max draw down: %f, start date: %s, end date: %s' % (max_dd,start_date,end_date)
	return max_dd,start_date_name,end_date_name,last_days

def split_df(df,start='2013-01-01',end='2017-03-07'):
	df = df[df.index>=start]
	df = df[df.index<=end]
	return df

max_dd_list = []
start_date_list = []
end_date_list = []
last_days_list =[]
total_return = []
date_list = []
threshold_list = []
df_zz = pd.read_hdf('all_index.h5','zz1000')
df_zz.index = df_zz.index.to_datetime()
df_zz = split_df(df_zz,start='2012-10-01')
df_zz = df_zz[['open','close','high','low','change']]

date_num1 = np.arange(14,31)
date_num = [20,25]

threshold_num1 = np.arange(90,140) * -0.001
threshold_num = [-0.109,-0.136]
name = 1
for number in date_num:
	df_zz = max_dd(df_zz,window=number)
	df_zz = split_df(df_zz,start='2013-01-01')
	for threshold in threshold_num:
		df_zz.ix[df_zz['maxdd'] > threshold , 'postion'] = 1
		df_zz.ix[df_zz['maxdd'] <= threshold, 'postion'] = 0
		df_zz = account(df_zz)
		df_zz['capital'] = (df_zz['cap_ret'] + 1.0).cumprod()
		df_zz.to_csv('sheildtest000'+str(name)+'.csv')
		name += 1

		l1,l2,l3,l4 = max_drawdown(df_zz.index,df_zz['capital'])
		max_dd_list.append(l1)
		start_date_list.append(l2)
		end_date_list.append(l3)
		last_days_list.append(l4)
		total_return.append(df_zz.ix[-1,'capital'])
		date_list.append(number)
		threshold_list.append(threshold)
		print 'number:',number,'threshold:',threshold
df_result = pd.DataFrame({'start':start_date_list,'end':end_date_list,'last_days':last_days_list,\
						  'max_dd':max_dd_list,'return':total_return,'date_num':date_list,'threshold':threshold_list})
df_result = df_result[['date_num','threshold','start','end','last_days','max_dd','return']]
df_result.to_csv('zzshield005.csv')







#stock_trading_days(stock_data, threshold=500)
'''
stock_data   = sma_strategy(stock_data)
stock_data   = account(stock_data)
period_return(stock_data, days=250, if_print=True)
trade_describe(stock_data)

date_line    = list(stock_data['date'])
capital_line = list(stock_data['capital'])
stock_line   = list(stock_data['close'])

print '\nStrategy Annual Return'
print annual_return(date_line, capital_line)
print '\nStock Annual Return'
print annual_return(date_line , stock_line)
print '\nStrategy Maxium Draw Down'
max_drawdown(date_line,capital_line)
print '\nStock Maxium Draw Down'
max_drawdown(date_line, stock_line)
'''

