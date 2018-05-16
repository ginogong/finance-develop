# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import re
import requests
import sys
from sqlalchemy import create_engine
import pandas as pd 
reload(sys)
sys.setdefaultencoding('utf-8')

header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
engine = create_engine('mysql://root:tomeko123@localhost/stock?charset=utf8', echo=False)
stock_list = pd.read_sql('stock_list',engine)
url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/%s/stocktype/LiuTongA.phtml'
for i in range(len(stock_list)):
	code = stock_list['code'].ix[i]
	url1 = url % code
	response = requests.get(url1, headers=header_req)
	data = pq(response.text)
	pattern_date = re.compile(u"hoverText='(\d{4}-\d{2}-\d{2})'")
	pattern_num = re.compile(u"value='(\d*.\d*)'")
	for item in data('#FusionCharts embed'):
		date =  pattern_date.findall(str(pq(item)))
		num = pattern_num.findall(str(pq(item)))
		l = zip(date,num)
		df = pd.DataFrame(l,columns=['date','outstanding10k'])
		df['code'] = code
		df.to_sql('outstanding',engine,if_exists='append')


	