from __future__ import division
import pandas as pd
import tushare as ts 


def calc_profit(df, threshold=0.08):
	df['open_change'] = df['open'] / df['close'].shift(1) - 1.0
	df['open_change'].fillna(0,inplace=True)
	df['max_change'] = df['high'] / df['close'].shift(1) - 1.0
	df['max_change'].fillna(0,inplace=True)
	df.ix[ (df['open_change'] > 0.03) & (df['open'] < df['close'].shift(1) * (1 + 0.08)),'buy_sig'] = 1.0
	df['buy_price'] = df['open']
	df['sell_price'] = df['open'].shift(-1)
	df['profit'] = df['sell_price'] / df['buy_price'] - 1.0
	return df[df['buy_sig'] == 1.0][['date','buy_price','sell_price','profit','code']]

columns = ['date','buy_price','sell_price','profit','code']
df_res = pd.DataFrame(columns=columns)
df_dayk = pd.read_hdf('dayk.h5','dayk')
df1 = pd.read_csv('stock_basics_0510.csv')
df1 = df1[df1['pe'] < 20]
ru_li = list(df1.index)
code_list_all= list(df_dayk['code'].unique())
code_list = [i for i in code_list_all if i not in ru_li]

for code in code_list:
	df_temp = df_dayk[df_dayk['code'] == code]
	df_temp = calc_profit(df_temp)
	df_res = pd.concat([df_res,df_temp])
	print code + 'finished!' 
print df_res['profit'].sum()
df_res.to_csv('papapa_0508_08.csv')

