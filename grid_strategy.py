from __future__ import division
import tushare as ts 
import pandas as pd 

code = '601390'
start = '2008-01-01'
end = '2017-03-16'
df = ts.get_k_data(code,start=start,end=end)
df = df.set_index('date')
df = df[['open','close','high','low']]

grid_style = pd.read_excel('601390_grid.xlsx',sheet='sheet1')
# grid coloumns   price_buy  price_sell quantity

def signal(vec,df,name):
	if df.ix[0,'low'] > vec['price_buy']:
		df.ix[0,name]=0
	df.ix[df['low'] < vec['price_buy'],name] = 0 
	df.ix[df['high'] >vec['price_sell'],name] = 1
	return df 

def real_price(vec,df,name):
	df[name + 'real_sell'] = vec['price_sell']
	df[name + 'real_buy']  = vec['price_buy']
	#df.ix[(df[name] < df[name].shift(1)) & (vec['price_buy'] > df['open']) ,name + 'real_buy'] = df['open']
	#df.ix[(df[name] > df[name].shift(1) )& (vec['price_sell'] < df['open']),name + 'real_sell'] = df['open']
	#df[name + 'real_buy'] = df[name + 'real_buy'].fillna(method='ffill')
	#df[name + 'real_sell'] =df[name + 'real_sell'].fillna(method='ffill')
	return df

def calc_trade(vec,df,name):
	df.ix[df[name] < df[name].shift(1),name + 'change'] = df[name + 'real_sell'] - df[name + 'real_buy']
	df[name + 'change'].fillna(0,inplace=True)
	df.ix[df[name] == 0,name + 'holding'] = vec['quantity']
	df.ix[df[name] == 1,name + 'holding'] = 0
	df[name+'holding'].fillna(0,inplace=True)
	return df
def calc_profit(vec,df,name):
	df[name + 'profit'] = df[name + 'change'] * df [name + 'holding']
	df[name + 'profit'] = df[name + 'profit'].cumsum()
	return df
for i in range(len(grid_style)):
	name = 'grid_' + str(i)
	df = signal(grid_style.ix[i,:],df,name)
	df = real_price(grid_style.ix[i,:],df,name)
	df= calc_trade(grid_style.ix[i,:],df,name)
	df = calc_profit(grid_style.ix[i,:],df,name)
	grid_style.ix[i,'profit'] = df.ix[-1,name+'profit']
	grid_style.ix[i,'trade_times'] = len(df) - df[name+'change'].value_counts()[0]

grid_style['cost'] = grid_style['price_buy'] * grid_style['quantity']
print grid_style
