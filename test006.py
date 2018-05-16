#-*- coding:utf-8 -*-
import pandas as pd
import tushare as ts 
import datetime
import requests
import json

zxg_api = 'http://www.e-ox.cn/api/'
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
	query_data = {'AUTHCODE':ath,'STRATEGYCODE':'gino001'}
	res = requests.post(zxg_api + query_url,data=json.dumps(query_data))
	result = json.loads(res.text)
	resultid = result['RESULTID']
	li = result['LISTS']
	return resultid,li

auth = login()
res_id,holding_li = query_port(auth)
big_port = 'ZH000207'
small_port = 'ZH000130'
for i in holding_li:
	if i['GPDM'] == big_port:
		big_weight = i['QZ']
	if i['GPDM'] == small_port:
		small_weight = i['QZ']



