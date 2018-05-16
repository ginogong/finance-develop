# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery as pq
import re
import requests


url = "http://hotel.qunar.com/city/chongqing_city/q-%E8%A7%A3%E6%94%BE%E7%A2%91#fromDate=2016-12-11&cityurl=chongqing_city&from=hotellist%7Cdiv&toDate=2016-12-12&QHFP=ZSL_A588B596&bs=&bc=重庆"
url1 = "http://hotel.qunar.com/city/chongqing_city/"
url2 = "http://hotel.qunar.com/city/chongqing_city/dt-21128/?tag=chongqing_city#fromDate=2016-12-11&toDate=2016-12-12&q=&from=list_page&fromFocusList=0&filterid=069b9016-f770-4fa9-a971-07b35a313a8a_A&showMap=0&qptype=&QHFP=ZSS_A61FD912"
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
response = requests.get(url2, headers=header_req)
#response.encoding = 'gbk'
with open('juanjuan.txt', 'w') as jj:
	jj.write(response.text)
data = pq(filename='juanjuan.txt')
print data('h3 title')