# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd 
import tushare as ts 
import numpy as np

def get_report_data(year,quarter):
    df = ts.get_report_data(year,quarter)
    return df
def add_year(s,year):
    s = s.apply(lambda x: str(year) +'-'+ x)
    return s 
year_list = range(2009,2017)
quarter_list = range(1,5)
path = '/Users/Gino/workspace/mysite/stock/stock/'
df_report = pd.DataFrame()
columns = ['code','eps','eps_yoy','bvps','roe','epcf',\
           'net_profits','profits_yoy','report_date','report']

for year in year_list:
    for quarter in quarter_list:
        df_temp = get_report_data(year,quarter)
        date = str(year) +'-' +  str(quarter)
        df_temp['report'] = date
        if quarter == 4:
            df_temp['report_date'] = add_year(df_temp['report_date'],year+1)
        else:
            df_temp['report_date'] = add_year(df_temp['report_date'],year)
        df_report = pd.concat([df_report,df_temp[columns]])
        print '%d year %d  qrt done!' % (year,quarter)
        #print df_report
df_temp = get_report_data(2017,1)
df_temp['report'] = '2017-1'
df_temp['report_date'] = add_year(df_temp['report_date'],2017)
df_report = pd.concat([df_report,df_temp[columns]])      
df_report.to_csv(path +'stock_report_05.csv')
df_report.to_hdf(path + 'report.h5','report')
