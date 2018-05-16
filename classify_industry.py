#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:45:25 2017

@author: Gino
"""
import requests
import pandas as pd
import re
from pyquery import PyQuery as pq
import time

def get_html_data(code):
    URL = '''http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/%s/menu_num/2.phtml'''
    url = URL % code
    HEADER_REQ = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
    response = requests.get(url,headers=HEADER_REQ)
    response.encoding='gbk'
    data = pq(response.text)

    industry_temp = []
    conception_temp = []
    content = data('#con02-0 .comInfo1')
    industry_html = content[0]
    conception_html = content[1]
    industry_start = (len(industry_html) -2) 
    industry_end = (len(industry_html) -1)
    industry_content = pq(industry_html[industry_start:industry_end]).text()
    if len(industry_content) <5:
        industry_temp.append(None)
    else:
        industry_temp.append(industry_content.split(' ')[0])
    conception_content = conception_html[1:]
    for item in (conception_content):
        conception_temp.append( pq(item).text().split(' ')[0])
    
    industry_list.append(industry_temp)
    conception_list.append(conception_temp)
    code_list.append(code)

def main():
    start = time.time()
    PATH = '/Users/Gino/workspace/mysite/stock/stock/'
    df = pd.read_hdf('stocklist.h5','stocklist')
    for i in range(len(df)):
        code = df.loc[i,'stocklist']
        get_html_data(code)
        print code + 'done!'
    df = pd.DataFrame({'code':code_list,'industry':industry_list,'conception':conception_list})
    df.to_hdf('outstand.h5','conception')
    print 'spend'+ str(time.time() - start)
industry_list = []
conception_list = []
code_list = []
if __name__ == '__main__':
    main()


#URL = '''http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/%s/menu_num/2.phtml'''
'''
HEADER_REQ = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }    
industry = []
conception = []
response = requests.get(url,headers=HEADER_REQ)
response.encoding='gbk'
data = pq(response.text)
content = data('#con02-0 .comInfo1')
industry_html = content[0]
conception_html = content[1]
industry_start = (len(industry_html) -2) 
industry_end = (len(industry_html) -1)
industry_content = pq(industry_html[industry_start:industry_end]).text()
if len(industry_content) <5:
    industry.append(None)
else:
    industry.append(industry_content.split(' ')[0])

conception_content = conception_html[1:]
for item in (conception_content):
    conception.append( pq(item).text().split(' ')[0])
for item in industry:
    print 'industry:',item
for item2 in conception:
    print 'conception:',item2
'''