import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery as pq
import re
import requests

url = 'https://xueqiu.com/strategy/24?from=singlemessage&isappinstalled=1'
header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
response = requests.get(url, headers=header_req)
data = pq(response.content)
#pattern_name = re.compile(u'^\w{8}')
#pattern_stock = re.compile(u'^\d{6}')
pattern_chn = re.compile(u'^[\u4E00-\u9FA5]+$')
for item in data('tbody ').items():
	stockData = item.find('item-row').find('td')
	print 'name:',item.find('td').find('.stock-name').text()
	print 'code:',item.find('td').find('.stock-symbol').text()
	print 'price:_recent:', item.find('td').eq(1).text()
	print 'price_choose:',  item.find('td').eq(2).text()
	print 'acc_raise:', item.find('td').eq(3).text()

	print 'date:', item.find('p').text()