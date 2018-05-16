#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np
import warnings 
from sklearn import neighbors
import datetime
from sklearn import preprocessing

warnings.filterwarnings('ignore')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr', False)

def auto_norm(df):
	df1 = df.copy()
	for i in  list(df.columns):
		df1[i] = (df[i] - df[i].min()) / (df[i].max() - df[i].min())
	return df1

def split_df(df,start='2010-01-01',end='2014-12-30'):
	df = df[df.index >= start]
	df = df[df.index <= end]
	return df

def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model
    
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model

def svm_classifier(train_x,train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf',probability=True)
    model.fit(train_x, train_y)
    return model
    
def logitic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model
 
 
 
 
data = pd.read_hdf('ml.h5','feature002')
data.pop('change')
data.pop('all_a')
data = auto_norm(data)
label = pd.read_hdf('ml.h5','label_ten')
label.pop('change')
label.pop('all_a')
now = datetime.datetime.now().strftime('%Y-%m-%d')
start = '2015-01-01'
train_x = split_df(data)
train_y = split_df(label)
test_x = split_df(data,start=start,end=now)
test_y = split_df(label,start=start,end=now)
hs_list = ['all_hs_change','all_zz_change','hs_zz_amp20','hs_zz_chg10','hs_zz_sma40','hs_zz_vol40']
zz_list = ['all_hs_change','all_zz_change','hs_zz_amp40','hs_zz_chg20','hs_zz_sma10','hs_zz_vol10']
test_classifier = ['NB','KNN','SVM','LR']
classifiers = {
               'NB':naive_bayes_classifier,
               'KNN':knn_classifier,
               'SVM':svm_classifier,
               'LR':logitic_regression_classifier
               }
for classifier in test_classifier:
    print '*****************{NAME}***********'.format(NAME=classifier)
    hs_model = classifiers[classifier](train_x[hs_list],train_y['hs_rise'])
    zz_model = classifiers[classifier](train_x[zz_list],train_y['zz_rise'])
    hs_predict = hs_model.predict(test_x[hs_list])
    zz_predict = zz_model.predict(test_x[zz_list])
    hs_accuracy = metrics.accuracy_score(test_y['hs_rise'],zz_predict)
    zz_accuracy = metrics.accuracy_score(test_y['zz_rise'],zz_predict)
    print 'hs_accuracy is {num}'.format(num=hs_accuracy)
    print 'zz_accuracy is {num}'.format(num=zz_accuracy)

'''
predict = model.predict(test_x)
accuracy = metrics.accuracy_score(test_y,predict)



#get data
data = pd.read_hdf('ml.h5','feature002')

data.pop('change')
data.pop('all_a')
col_data = list(data.columns)
label = pd.read_hdf('ml.h5','label_ten')

label.pop('change')
label.pop('all_a')
data = auto_norm(data)
now = datetime.datetime.now().strftime('%Y-%m-%d')
start = '2015-01-01'
num = 30
data1 = split_df(data,start=start,end=now)
label1 = split_df(label,start=start,end=now)
times =  int(len(data1) / num)
shift = num * times
data_temp = data1[:shift-1]
label_temp = label1[:shift-1]
data_hist = split_df(data)
label_hist = split_df(label)
data_nn = pd.concat([data_hist,data_temp])
label_nn = pd.concat([label_hist,label_temp])
data_nn = auto_norm(data_nn)

hs_list = ['all_hs_change','all_zz_change','hs_zz_amp20','hs_zz_chg10','hs_zz_sma40','hs_zz_vol40']
zz_list = ['all_hs_change','all_zz_change','hs_zz_amp40','hs_zz_chg20','hs_zz_sma10','hs_zz_vol10']
clf_hs = neighbors.KNeighborsClassifier(7,weights='uniform')
clf_zz = neighbors.KNeighborsClassifier(27,weights='uniform')


clf_hs.fit(data_nn[hs_list],label_nn['hs_cls1'])
clf_zz.fit(data_nn[zz_list],label_nn['zz_cls1'])

hs_pre = clf_hs.predict(data[data.index== now][hs_list])
zz_pre = clf_zz.predict(data[data.index== now][zz_list])

print 'hs_pre:', hs_pre
print 'zz_pre:', zz_pre


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
	query_data = {'AUTHCODE':ath,'STRATEGYCODE':'gino001'}
	res = requests.post(zxg_api + query_url,data=json.dumps(query_data))
	result = json.loads(res.text)
	resultid = result['RESULTID']
	li = result['LISTS']
	return resultid,li
def adjust_port(ath,li):
	adjust_data = {'AUTHCODE':ath,'STRATEGYCODE':'gino001','STRATEGYNAME':'bigbaba','STRATEGYDESCRIPTION':' ',\
					'LISTS':li}
	response = requests.post(zxg_api + adjust_url, data=json.dumps(adjust_data))
	res = json.loads(response.text)
	resultid = res['RESULTID']
	return resultid

auth = login()
res_id,holding_li = query_port(auth)
big_port = 'ZH000207'
small_port = 'ZH000130'
step = 0.125
for i in holding_li:
	if i['GPDM'] == big_port:
		big_weight = float(i['QZ'])
	if i['GPDM'] == small_port:
		small_weight = float(i['QZ'])

big_signal,small_signal = signal(hs_pre,zz_pre)
big_weight_obj = big_weight + big_signal
small_weight_obj = small_weight + small_signal
big_weight_adjust = adjust_signal(big_weight_obj)
small_weight_adjust = adjust_signal(small_weight_obj)
big_weight_temp = big_weight + big_weight_adjust * big_signal
small_weight_temp = small_weight + small_weight_adjust * small_signal

if big_weight_temp + small_weight_temp > 1:
	big_weight_temp = big_weight
	small_weight_temp = small_weight

adjust_li = [{'STOCKCODE':big_port,'WEIGHT':str(big_weight_temp)},\
				{'STOCKCODE':small_port,'WEIGHT':str(small_weight_temp)}]

res_ajust = adjust_port(auth,adjust_li)


print 'big_weight:',big_weight,'-->',big_weight_temp
print 'small_weight',small_weight , '-->', small_weight_temp

if res_ajust == '1':
	print 'adjust finished'
else:
	print 'something is wrong.'
'''







