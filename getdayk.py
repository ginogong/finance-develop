# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import create_engine,Table,MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import tushare as ts 
import pandas as pd 
import numpy as np 

def get_ts_data(code,st='2010-01-01',ed='2017-02-20'):
	columns = ['date','open_price','close_price','high_price','low_price','volume','code']
	df = ts.get_k_data(code,start=st,end=ed)
	df.columns = columns
	return df
def get_stock_list():
	engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8')
	stl = pd.read_sql('list',engine)
	return stl

def main():	
	engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8')
	stocklist = get_stock_list()
	for i in range(len(stocklist)):
		dataframe = get_ts_data(stocklist['stocklist'].ix[i])
		dataframe.to_sql('newdayk',engine,if_exists='append')
		print 'just finished %s' % stocklist['stocklist'].ix[i]

main()