#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 20:08:44 2017

@author: Gino
"""


import pandas as pd
import numpy as np
import tensorflow as tf
from numpy.random import RandomState
'''
# first NN
batch_size = 8
w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
x  = tf.placeholder(tf.float32, shape=(None,2), name='x-input')
y_ = tf.placeholder(tf.float32, shape=(None,1), name='y-input')
a = tf.matmul(x,w1)
y = tf.matmul(a,w2)
cross_entropy = - tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y,1e-10,1.0)))
train_step =tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size,2)
Y = [[int(x1+x2 < 1)] for (x1,x2) in X]
with tf.Session() as sess:
    init_op = tf.initialize_all_variables()
    sess.run(init_op)
    print sess.run(w1)
    print sess.run(w2)
    step = 5000
    for i in range(step):
        start = ( i * batch_size) % dataset_size
        end = min(start+batch_size, dataset_size)
        sess.run(train_step, feed_dict={x:X[start:end],y_:Y[start:end]})
        if i % 1000 ==0:
            total_cross_entropy = sess.run(cross_entropy,feed_dict={x:X,y_:Y})
            print 'After %d  training steps,cross entropy on all data is %g' % (i,total_cross_entropy)
    print sess.run(w1)
    print sess.run(w2)

#second NN
batch_size = 8
x  = tf.placeholder(tf.float32,shape=(None,2),name='x-input')
y_ = tf.placeholder(tf.float32,shape=(None,1),name='y-input')

w1 = tf.Variable(tf.random_normal([2,1],stddev=1,seed=1))
y  = tf.matmul(x,w1)
loss_less = 10
loss_more = 1
loss = tf.reduce_sum(tf.select(tf.greater(y,y_),
                               (y - y_) * loss_more,
                               ( y_ - y) * loss_less))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size,2)
Y = [[x1 + x2 + rdm.rand() / 10 - 0.05] for (x1,x2) in X]

with tf.Session() as sess:
    init_op = tf.initialize_all_variables()
    sess.run(init_op)
    STEPS = 5000
    for i in range(STEPS):
        start = (i * batch_size) % dataset_size
        end = min(start+batch_size, dataset_size)
        sess.run(train_step, feed_dict={x:X[start:end],y_:Y[start:end]})
    print sess.run(w1)

#stochastic gradient descent
batch_size = n
x  = tf.placeholder(tf.float32,shape=(batch_size,2),name='x-input')
y_ = tf.placeholder(tf.float32,shape=(batch_size,1),name='y-input')
loss = '...'
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)
with tf.Session() as sess:
    for i in range(steps):
        current_X = ''
        current_y = ''
        sess.run(train_step,feed_dict={x:current_X,y_:current_Y})



def get_weight(shape,lam):
    var = tf.Variable(tf.random_normal(shape),dtype=tf.float32)
    tf.add_to_collection('losses',tf.contrib.layers.l2_regularizer(lam)(var))
    return var
    
    
x  = tf.placeholder(tf.float32,shape=(None,2))
y_ = tf.placeholder(tf.float32,shape=(None,1))
batch_size = 8
layer_dimension = [2,10,10,10,1]
n_layers = len(layer_dimension)
cur_layer = x
in_dimension = layer_dimension[0]
for i in range(1,n_layers):
    out_dimension = layer_dimension[i]
    weight = get_weight([in_dimension,out_dimension], 0.001)
    bias = tf.Variable(tf.constant(0.1,shape=[out_dimension]))
    cur_layer = tf.nn.relu(tf.matmul(cur_layer,weight) + bias)
    in_dimension = layer_dimension[i]
mse_loss = tf.reduce_mean(tf.square(y_ - cur_layer))
tf.add_to_collection('losses',mse_loss)
loss = tf.add_n(tf.get_collection('losses'))

v1 = tf.Variable(0,dtype=tf.float32)
step = tf.Variable(0,trainable=False)
ema = tf.train.ExponentialMovingAverage(0.99, step)
maintain_averages_op = ema.apply([v1])
with tf.Session() as sess:
    init_op = tf.initialize_all_variables()
    sess.run(init_op)
    print sess.run([v1, ema.average(v1)])
    
    sess.run(tf.assign(v1,5))
    sess.run(maintain_averages_op)
    print sess.run([v1,ema.average(v1)])
    
    sess.run(tf.assign(step, 1000))
    sess.run(tf.assign(v1,10))
    sess.run(maintain_averages_op)
    
'''
from tensorflow.examples.tutorials.mnist import input_data
#mnist = input_data.read_data_sets('/Users/Gino/workspace/to/MNIST_data/',one_hot=True)
'''
print mnist.train.num_examples
print mnist.validation.num_examples
print mnist.test.num_examples
print mnist.train.images[0]
print mnist.train.labels[0]

batch_size = 100
xs,ys = mnist.train.next_batch(batch_size)
print ys.shape
'''
'''

INPUT_NODE = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500
BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY= 0.99

def inference(input_tensor, avg_class, weights1, biases1,weights2,biases2):
    if avg_class == None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor,weights1) + biases1)
        return tf.matmul(layer1, weights2) + biases2

    else:
        layer1 = tf.nn.relu(
                            tf.matmul(input_tensor, avg_class.average(weights1))+
                            avg_class.average(biases1))
        return tf.matmul(layer1, avg_class.average(weights2) +
                         avg_class.average(biases2))


def train(mnist):
    x  = tf.placeholder(tf.float32,[None, INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32,[None, OUTPUT_NODE], name='y-input')
    weights1 = tf.Variable(
                           tf.truncated_normal([INPUT_NODE, LAYER1_NODE],stddev=0.1))
    biases1 = tf.Variable(tf.constant(0.1,shape=[LAYER1_NODE]))
    weights2 = tf.Variable(
                           tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
    biases2 = tf.Variable(tf.constant(0.1,shape=[OUTPUT_NODE]))
    y = inference(x, None,weights1, biases1,weights2, biases2)
    global_step = tf.Variable(0, trainable=False)
    variable_averages = tf.train.ExponentialMovingAverage(
                        MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    
    average_y = inference(x, variable_averages,weights1,biases1,weights2,biases2)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                            y, tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    regularization = regularizer(weights1) + regularizer(weights2)
    loss = cross_entropy_mean + regularization
    learning_rate = tf.train.exponential_decay(
                    LEARNING_RATE_BASE,
                    global_step,
                    mnist.train.num_examples/BATCH_SIZE,
                    LEARNING_RATE_DECAY)
    train_step = tf.train.GradientDescentOptimizer(learning_rate)\
                .minimize(loss,global_step=global_step)
    train_op = tf.group(train_step,variables_averages_op)
    correct_prediction = tf.equal(tf.argmax(average_y, 1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        validate_feed = {x:mnist.validation.images,y_:mnist.validation.labels}
        test_feed = {x:mnist.test.images,y_:mnist.test.labels}
        for i in range(TRAINING_STEPS):
            if i % 1000 == 0:
                validate_acc = sess.run(accuracy, feed_dict=validate_feed)
                print 'After %d training step(s),validate accuracy \
                         using average model is %g' %(i,validate_acc)
            xs,ys = mnist.train.next_batch(BATCH_SIZE)
            sess.run(train_op, feed_dict={x:xs,y_:ys})
        test_acc = sess.run(accuracy, feed_dict=test_feed)
        print 'After %d traing step(s), test accuracy using average \
            model is %g' % (TRAINING_STEPS, test_acc)

def main(argv=None):
    mnist = input_data.read_data_sets('/Users/Gino/workspace/to/MNIST_data/',one_hot=True)
    train(mnist)

if __name__ == '__main__':
    tf.app.run()

'''
    



























































