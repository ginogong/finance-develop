#-*- coding:utf-8 -*-
import pandas as pd 
from sqlalchemy import create_engine

engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8')
df = pd.read_sql_table('newdayk',engine)
df.to_hdf('newdayk.h5', 'dayk',index=False)

