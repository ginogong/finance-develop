import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tushare as ts 
import numpy as np 
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8',echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
df = pd.read_sql('report_table', engine)
new_index = [ x for x in range(1,len(df)+1)]
print df.index
df.index = new_index
df.to_sql('report_table', engine,if_exists='replace')
print df.index