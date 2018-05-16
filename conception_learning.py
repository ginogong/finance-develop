#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:05:28 2017

@author: Gino
"""

import pandas as pd
import pickle
PATH = '/Users/Gino/workspace/mysite/stock/stock/'
def unpack_industry(li):
    return li[0]
    
df = pd.read_hdf('outstand.h5','conception')
industry_dict = {}
conception_dict = {}
'''
code = df.loc[1,'code']
df['industry_unpack'] = df['industry'].apply(unpack_industry)
df['industry_unpack'].fillna('empty',inplace=True)
industry_set = df['industry_unpack'].unique()
industry_set =list(set(industry_set))
df_industry_group = df.groupby('industry_unpack')
for item in industry_set:
    code_list= []
    code_list = df_industry_group.get_group(item)['code'].unique()
    code_list = list(set(code_list))
    industry_dict.setdefault(item,[])
    industry_dict[item]= code_list
    print item + 'done'
    
f = open(PATH+'industry.txt','w')
pickle.dump(industry_dict,f)
f.close()
'''
conception_list = []
for i in range(len(df)):
    conception_list.extend(df.loc[i,'conception'])
conception_list = list(set(conception_list))


for conception in conception_list:
    conception_dict.setdefault(conception,[])
    for i in range(len(df)):
        if conception in df.loc[i,'conception']:
           conception_dict[conception].append(df.loc[i,'code'])
    print conception + '_done!'
f1 = open(PATH+'conception.txt','w')
pickle.dump(conception_dict,f1)
f1.close()
  

