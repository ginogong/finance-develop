import tushare as ts 
import pandas as pd 
import datetime

#df = pd.read_csv('tickdata_511990_01.csv')
#df =  df[['date','time','price','volume']]
df = pd.read_hdf('tick.h5','511990')
print df