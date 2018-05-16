#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 21:18:28 2017

@author: Gino
"""
from __future__ import division
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn import cross_validation
from sklearn import datasets
from sklearn import metrics

'''
#定义一个LSTM结构。在tensorflow中通过简单的命令就可以实现一个完整LSTM结构
#LSTM中使用的变量也会在该函数中自动被声明

lstm = tf.rnn_cell.BasicLSTMCell(lstm_hidden_size)
#将LSTM中的状态初始化为全0数组。与其他神经网络相似，在优化循环神经网络时，每次也会
#使用一个BATCH的训练样本。以下代码中，batch_size给出了一个batch的大小
#BasicLSTMCell类提供了zero_state函数来生成全0的初始状态
state = lstm.zero_state(batch_size,tf_float32)
#定义损失函数
loss =0.
#用num step 来表示避免梯度消散而允许最大的序列长度
'''
learn = tf.contrib.learn
#自定义模型，对于给定的输入数据(features)以及对应的正确答案(target) 返回在这些输入上
#的预测值，损失函数以及训练步骤
def my_model(features,target):
    #将预测的目标转换为one-hot的编码形式，因为共有3个类别，所以向量长度为3
    #经过转化后第一个类别表示（1，0，0） 第二个类别表示（0，1，0） 第三个类别表示（0，0，1）
    target = tf.one_hot(target,3,1,0)
    #定义模型以及给定数据上的损失函数。 TFLEARN 通过 logistic_regression封装了一个单层全连接
    #神经网络
    logits, loss = learn.models.logistic_regression(feature, target)
    #创建模型的优化器，并得到优化步骤
    train_op = tf.contrib.layers.optimize_loss(
                loss,                                     #损失函数
                tf.contrib.framework.get_global_step(),   #获取训练步数并在训练时更新
                optimizer='Adagrad',                      #定义优化器
                learning_rate=0.1)                        #定义学习率

    return tf.arg_max(logits,1) ,loss , train_op

#对自定义的模型进行封装
classifier = learn.Estimator(model_fn=my_model)
#使用封装好的模型和训练数据执行100轮迭代
classifier.fit(x_train , y_train, steps=100)
#使用训练好的模型进行结果预测
y_predicted = classifier.predict(x,test)
#计算模型的精确度
score = metrics.accuracy_score(y_test,y_predicted)





   