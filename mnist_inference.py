#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 22:11:38 2017

@author: Gino
"""

import tensorflow as tf
#define arguments
INPUT_NODE  = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500

def get_weight_variable(shape,regularizer):
    weights = tf.get_variable(
        'weights',shape,
        initializer=tf.truncated_normal_initializer(stddev=0.1))
    if regularizer != None:
        tf.add_to_collection('losses', regularizer(weights))
    return weights
    
#define forward propagation
def inference(input_tensor,regularizer):
    #define layer1
    with tf.variable_scope('layer1',reuse=True):
        
        weights = get_weight_variable(
                    [INPUT_NODE,LAYER1_NODE],regularizer)
        biases = tf.Variable(
                    0.0,[LAYER1_NODE])
        layer1 = tf.nn.relu(tf.matmul(input_tensor,weights) + biases)
    
    #define layer2
    with tf.variable_scope('layer2',reuse=True):
        weights = get_weight_variable(
                    [LAYER1_NODE, OUTPUT_NODE], regularizer)
        biases = tf.get_variable(
                 'biases',[OUTPUT_NODE],
                    initializer=tf.constant_initializer(0.0))
        layer2 = tf.nn.relu(tf.matmul(layer1,weights) + biases)
    return layer2
    

        