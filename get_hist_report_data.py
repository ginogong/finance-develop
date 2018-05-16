import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tushare as ts 
import numpy as np 
import pandas as pd 

year_list = [2012,2013,2014,2015,2016,2017]
quarter_list = [1,2,3,4]
for year in year_list:
	print year
	print type(year)
	for quarter in quarter_list:
		print quarter
		print type(quarter)
		df = ts.get_report_data(year,quarter)
		df = df[['code','eps','eps_yoy','report_date']]
		df['date'] = '%s-%s' % (str(year),str(quarter))
		df.to_sql('report_table',engine,if_exists='append')
