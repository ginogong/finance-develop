# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import create_engine,Table,MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa 
import tushare as ts 
import pandas as pd 
import numpy as np 

engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8')
sql = "select date,open_price,close_price,code from dayk where code=600000 or code=300001"
dataframe = pd.read_sql(sa.text(sql),engine,parse_dates='date')
def get_change(x,y):
	return (x - y) / y
dataframe['rise'] = get_change(dataframe['close_price'],dataframe['open_price'])
dataframe['change_day'] = get_change(dataframe['close_price'],dataframe['close_price'].shift(1))
up_days = dataframe[dataframe['change_day'] >0]

def cal_rsi(rise, fall):
	return 100.0 - 100.0 / (1 + rise /abs(fall))

def cal_rsi14(df):
	number = 14
	for i in range(0,len(df) - number+1):
		df_sub = df['change_day'][i:i+number]
		rise_sum = df_sub[df_sub>0].sum()
		fall_sum = abs(df_sub[df_sub <= 0].sum())
		if fall_sum != 0:
			df.ix[i+number-1,'rsi'] = 100 - 100 / (1 + rise_sum / fall_sum)
		else:
			df.ix[i+number-1,'rsi'] = 99.99
	return df 

df_group = dataframe.groupby('code').apply(cal_rsi14)
code_list = dataframe['code'].unique()




