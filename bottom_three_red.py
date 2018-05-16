#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 22:09:20 2017

@author: Gino
"""

from __future__ import division
import pandas as pd 
import numpy as np
import warnings 
import datetime
import requests
import json

warnings.filterwarnings('ignore')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr', False)

zxg_api = 'http://114.215.241.28/api/'
login_url = 'login/login.php'
new_url = 'strategy/strategynew.php'
adjust_url = 'strategy/strategychange.php'
query_url = 'strategy/strategyquery.php'
def login():
	login_data = {'USERID':'YH00000004','PASSWORD':'12346789'}
	res = requests.post(zxg_api + login_url,data=json.dumps(login_data))
	auth = json.loads(res.text)['RESULTMSG'].encode('utf-8')
	return auth
def query_port(ath):
	query_data = {'AUTHCODE':ath,'STRATEGYCODE':'gino002'}
	res = requests.post(zxg_api + query_url,data=json.dumps(query_data))
	result = json.loads(res.text)
	resultid = result['RESULTID']
	li = result['LISTS']
	return resultid,li
def adjust_port(ath,li):
	adjust_data = {'AUTHCODE':ath,'STRATEGYCODE':'gino002','STRATEGYNAME':'bottom_red','STRATEGYDESCRIPTION':'red_three',\
					'LISTS':li}
	response = requests.post(zxg_api + adjust_url, data=json.dumps(adjust_data))
	res = json.loads(response.text)
	resultid = res['RESULTID']
	return resultid

def new_strategy(ath,li):
    new_strategy_data = {
                         'AUTHCODE':ath,
                         'STRATEGYCODE':'gino002',
                         'STRATEGYNAME':'bottom_red',
                         'STRATEGYDESCRIPTION':'red_three',
                         'STRATEGYLEVEL':'0',
                         'LISTS':li
                        
                         }
    response = requests.post(zxg_api + new_url, data=json.dumps(new_strategy_data))
    res = json.loads(response.text)
    resultid = res['RESULTID']
    return resultid
def unpack_holding_list(li):
    stock_list = []
    weight_list = []
    stock_num = len(li)
    for item in li:
        stock_list.append(item['GPDM'])
        weight_list.append(float(item['QZ']))
    return stock_list,weight_list
    
def holding_to_json(df):
    li = []
    for i in range(len(df)):
        di = {}
        di['STOCKCODE'] =df.loc[i,'code']
        di['WEIGHT'] = str(df.loc[i,'weights'])
        li.append(di)
        
    return li

def remove_stock(li,dataframe):
    for i in li:
       dataframe.loc[ dataframe['code']== i,'weights'] =0
    stock_weight_sum = dataframe[dataframe['code']!='XXXXXX'].weights.sum(axis=0)
    if len(dataframe[dataframe['code']=='XXXXXX']) < 1:
        dataframe.loc[len(dataframe)] = {'code':'XXXXXX','weights':1.0 -stock_weight_sum}
    else:
        dataframe.loc[dataframe['code']=='XXXXXX','weights'] = 1.0 -stock_weight_sum
    #dataframe.loc[dataframe['code']=='XXXXXX','weights'] = 1.0 -stock_weight_sum
    return dataframe

def add_stock(li,dataframe):
    t = 0
    weight = 0.25
    if len(dataframe[dataframe['code']=='XXXXXX']) < 1:
        print 'Can not add stock !'
        return dataframe
    else:
        cash = dataframe.loc[dataframe[dataframe['code']=='XXXXXX'].index[0],'weights']
        if cash / len(li) < weight:
            weight = cash / len(li)
        for j in range(len(dataframe),len(li)+len(dataframe)):           
            dataframe.loc[j,'code'] = li[t]
            t+= 1
        for i in li:
            dataframe.loc[dataframe['code']== i,'weights'] = weight
        stock_weight_sum = dataframe[dataframe['code']!='XXXXXX'].weights.sum(axis=0)
        if len(dataframe[dataframe['code']=='XXXXXX']) < 1:
            dataframe.loc[len(dataframe)] = {'code':'XXXXXX','weights':1.0 -stock_weight_sum}
        else:
            dataframe.loc[dataframe['code']=='XXXXXX','weights'] = 1.0 -stock_weight_sum
        return dataframe

new_li = [{'STOCKCODE':'sz000611',
           'WEIGHT':'0.25'
           },
           {'STOCKCODE':'sz002686',
            'WEIGHT':'0.25'
            }
           ]
auth = login()
res_id,holding_list = query_port(auth)

remove_li = []
add_li =['sz000630']
sto_li = []
wgt_li = []
if int(res_id) == 1:
     sto_li,wgt_li = unpack_holding_list(holding_list)
df = pd.DataFrame({'code':sto_li,'weights':wgt_li})
df = remove_stock(remove_li,df)

df = add_stock(add_li,df)
print df
'''  
cash_index =df[df['code']==u'sz002686'].index

if df.loc[cash_index[0],'weights']>0.25:
    df.loc[cash_index[0],'weights'] =0
    df_new = pd.DataFrame([[new_code,0.25]],columns=df.columns)
    df =df.append(df_new,ignore_index=True)

elif df.loc[cash_index[0],'weights']<0.25:
    new_weight = df.loc[cash_index[0],'weights']
    df_new = pd.DataFrame([[new_code,new_weight]],columns=df.columns)
    df =df.append(df_new,ignore_index=True)
    df = df.drop(cash_index[0])
    df.index = range(len(df))
    
''' 
adjust_json =  holding_to_json(df)
res = adjust_port(auth,adjust_json)
print res
if res == '1':
    print 'adjust finished'





 
 
 
 
 
 
 