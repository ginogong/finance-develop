#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 20:18:55 2017

@author: Gino
"""
from __future__ import division
import tensorflow as tf 
import pandas as pd 

#dataset 相关参数
INPUT_NODE = 784   # 输入层节点数
OUTPUT_NODE = 10   #输出层节点数

#配置神经网络参数
LAYER1_NODE = 500   #隐藏层节点
BATCH_SIZE = 100    #一个训练中的数据个数，数字越小越接近于随机梯度下降，反之接近梯度下降
LEARNING_RATE_BASE = 0.8  #基础的学习率
LEARNING_RATE_DECAY = 0.99  #学习率的衰减率
REGULARIZTION_RATE = 0.0001 #正则化项的损失函数的系数
TRAINING_STEPS = 30000  #训练轮数
MOVING_AVERAGE_DECAY = 0.99 #滑动平均衰减率

#定义一个辅助函数 给点神经网络的输入和所有参数，计算神经网络前向传播的结果
def inference(input_tensor, avg_class, weights1,biases1,weights2,biases2):
    #当诶与提供滑动平均类时，直接使用参数当前的取值
    if avg_class == None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor,weights1) + biases1 )
        return tf.matmul(layer1,weights2) + biases2
    else:
        #首先使用avg_class.average函数计算出变量的滑动平均值
        layer1 = tf.nn.relu(tf.matmul(input_tensor,avg_class.average(weights1)) + 
                            avg_class.average(biases1))
        return tf.matmul(layer1,avg_class.average(weights2) +
                         avg_class.average(biases2))
        
#训练模型的过程
def train(data):
    x  = tf.placeholder(tf.float32, [None,INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None,OUTPUT_NODE], name='y-input')
    weights1 = tf.Variable(
                           tf.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1))
    biases1 = tf.Variable(tf.constant(0.1,shape=[LAYER1_NODE]))
    weights2 = tf.Variable(
                           tf.truncated_normal([LAYER1_NODE,OUTPUT_NODE],stddev=0.1))
    biases2 = tf.Variable(tf.constant(0.1,shape=[OUTPUT_NODE]))
    #计算当前参数下神经网络前向传播的结果。这里给出的滑动平均的类为None
    #函数不会使用参数的滑动平均值
    y = inference(x, None,weights1,biases1,weights2,biases2)
    #定义存储训练轮数的变量。这个变量是不需要滑动平均
    global_step = tf.Variable(0, trainable=False)
    
    #给定滑动平均衰减率和训练轮数的变量，初始化滑动平均类
    variable_averages = tf.train.ExponentialMovingAverage(
                        MOVING_AVERAGE_DECAY,global_step)
    #在所有代表神经网络参数的变量上使用滑动平均
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    #计算使用滑动平均之后的前向传播的结果
    average_y = inference(x,variable_averages,weights1,biases1,weights2,biases2)
    #计算交叉熵作为刻画预测值和真实值之间差距的损失函数
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                        y, tf.argmax(y_,1))
    #计算当前batch中交叉熵的平均值
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    #计算L2正则化函数
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZTION_RATE)
    #计算模型的正则化损失
    regularization = regularizer(weights1) + regularizer(weights2)
    loss = cross_entropy_mean + regularization
    #设置指数衰减的学习率
    learning_rate = tf.train.exponential_decay(
                    LEARNING_RATE_BASE, global_step,
                    train_num/BATCH_SIZE,#过完所有训练数据需要的迭代次数
                    LEARNING_RATE_DECAY)
    train_step = tf.train.GradientDescentOptimizer(learning_rate)\
                .minimize(loss,global_step=global_step)
    #训练一遍数据 需要通过反向传播来更新神经网络的参数，也需要更新参数的滑动平均值
    train_op = tf.group(train_step,variables_averages_op)
    correct_prediction = tf.equal(tf.argmax(average_y,1),tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    
    #初始会话开始训练过程
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        #准备验证数据
        validate_feed = {x:data,y_:label}
        #准备测试数据
        test_feed = {x:data_test,y_:label_test}
        #迭代训练神经网络
        for i in range(TRAINING_STEPS):
            #每1000轮输出一次验证数据集上的测试结果
            if i % 1000 == 0:
                validate_acc = sess.run(accuracy, feed_dict=validate_feed)
                print 'After %d training steps, validation accuracy  is %g' % (i,validate_acc)
            xs,ys = next_data 
            sess.run(train_op,feed_dict={x:xs, y:ys})
        test_acc = sess.run(accuracy, feed_dict=test_feed)
        print 'After %d training steps, test accuracy  is %g' % (TRAINING_STEPS,test_acc)
        
def main(argv=None):
    data=...
    train(data)

if __name__ == '__main__':
    tf.app.run()
    
    
    
        
        
        
        
        
        