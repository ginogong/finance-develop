#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 16:44:31 2017

@author: Gino
"""
import jieba
import jieba.posseg as pseg
import jieba.analyse as anl
import requests
from pyquery import PyQuery as pq
import re
import pandas as pd
import tushare as ts 
from bs4 import BeautifulSoup
from urllib2 import urlopen
import datetime
import time

url_7_24 = 'http://kuaixun.eastmoney.com/'
url_stock_list = 'http://quote.eastmoney.com/stocklist.html'
HEADER_REQ = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
PATH = '/Users/Gino/workspace/mysite/stock/stock/'
'''
response = requests.get(url_7_24,headers=HEADER_REQ)
response.encoding = 'utf-8'
now = datetime.datetime.now().strftime('%Y-%m-%d')
data = pq(response.text)

df = pd.DataFrame({})
pattern = re.compile(u'【.+】')
for item in data('#livenews-list h2 a'):
    print pattern.findall(pq(item).text())[0].encode('utf-8')
'''   

def get_eastmoney_info():
    df1 = pd.read_hdf(PATH + 'information.h5','info')
    url = 'http://kuaixun.eastmoney.com/'
    response = requests.get(url,headers=HEADER_REQ)
    response.encoding = 'utf-8'
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    data = pq(response.text)
    pattern_title = re.compile(u'【.+】')
    pattern_content = re.compile(u'】.+')
    title_list= []
    content_list = []
    for item in data('#livenews-list h2 a'):
        title = pattern_title.findall(pq(item).text())[0][1:-1].encode('utf-8')
        title_list.append(title)
        content = pattern_content.findall(pq(item).text())[0][1:]
        content_list.append(content)
    df_temp = pd.DataFrame({'content':content_list,'title':title_list})
    df_temp['date'] = now
    df1 = pd.concat([df1,df_temp])
    df1 = df1.drop_duplicates()
    df1.index = range(len(df1))
    df1.to_hdf(PATH+'information.h5','info')

    
def get_code_name_list():
    df = pd.read_hdf(PATH+'information.h5','name')   
    url_stock_list = 'http://quote.eastmoney.com/stocklist.html'
    code_pattern = re.compile(r'\d{6}')
    replace_pattern = re.compile('\(\d{6}\)')
    response = requests.get(url=url_stock_list,headers=HEADER_REQ)
    response.encoding ='gb2312'
    data = pq(response.text)
    name_list = []
    code_list = []
    stock_a = ['600', '603', '601', '300', '002', '000','001']
    for item in data('#quotesearch ul li'):
        code_temp = code_pattern.findall(pq(item).text())   
        code_find = str(code_pattern.findall(str(code_temp)))
        if code_find[2:5] in stock_a:    
            name = re.sub(replace_pattern,'',pq(item).text())
            code_list.append(code_find[2:8])
            name_list.append(name)
    df_temp = pd.DataFrame({'code':code_list,'name':name_list})
    df = pd.concat([df,df_temp])
    df = df.drop_duplicates()
    
    df.to_hdf(PATH+'information.h5','name')

def main():
    time.sleep(300)
    et_eastmoney_info()
    
if __name__ == '__main__':
    main()




