#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 21:38:52 2017

@author: Gino
"""

import jieba
import pandas as pd
import re
PATH = '/Users/Gino/workspace/mysite/stock/stock/'

    
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
    df.index = range(len(df))   
    df.to_hdf(PATH+'information.h5','name')

#get_code_name_list()
df = pd.read_hdf(PATH + 'information.h5','name')
pattern = re.compile(u'[\u4e00-\u9fa5]+')
for i in range(len(df)):
    name = pattern.findall(df.loc[3449,'name'])[0]
    jieba.add_word(name,freq=10000)
jieba.add_word('TCL集团',freq=1000)
jieba.add_word('GQY视讯',freq=1000)
jieba.add_word('中报',freq=1000)

df2 = pd.read_hdf(PATH + 'information.h5','info')
for k in range(10):
    print '_'.join(jieba.cut(df2.loc[k,'content']))


















