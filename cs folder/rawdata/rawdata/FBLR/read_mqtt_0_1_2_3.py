# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:49:07 2019

@author: ambuj
"""

from keras.models import model_from_json
import json
import numpy as np
import paho.mqtt.client as mqtt
import pickle
import pandas as pd
import numpy
import time

mqtt_username = "username"
mqtt_password = "qwertyuiop"
mqtt_topic1 = "runbot"
mqtt_topic = "wheelgear"
mqtt_broker_ip = "192.168.43.131"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):    
    x = str(msg.payload)[2:-1].split(",")
    print("x",x)
    #x=attention,meditation,delta,theta,lowAplha,highAlpha,lowBeta,highBeta,lowGamma,highGamma
    def sig(xx):
    
        if xx>51 and x<-51:
            return 1
        else:
            return 1/(1+numpy.exp(-xx))

    def evaluatestack(stack):
        elem = stack.pop(0)
    
        if (elem == '-'):
            return evaluatestack(stack) - evaluatestack(stack)
        elif (elem == '+'):
            return evaluatestack(stack) + evaluatestack(stack)
        elif (elem == '/'):
            try:
                return evaluatestack(stack) / evaluatestack(stack)
            except:
                print("anindya")
                return 0
        elif (elem == '*'):
            return evaluatestack(stack) * evaluatestack(stack)
        elif(elem=='P'):
             return sig(evaluatestack(stack)+evaluatestack(stack))
        elif(elem=="W"):
            return evaluatestack(stack)*evaluatestack(stack)
        else:
            # print(type(elem))
            return int(elem)
        
    infile = open('0_1_2_3_classifier.pkl','rb')
    new_dict = pickle.load(infile)
    infile.close()
    b=list(map(int,x))
    #print("b ",b)
    #classifier=new_dict[2]
    '''print(classifier)
    for i in range(20):
        
        if isinstance(classifier[i], int):
            classifier[i]=b[classifier[i]]
    print(classifier)
    a=(evaluatestack(classifier))
    print("a: ",a)
                
    if(a > 0.9):
        print('3')
    elif(a > 0.5 and a< 0.8):
        print('2')
    elif(a > 0.8 and a < 0.9):
        print('1')
    else:
        print('0')'''
    for c in b:
        if(c > 5000):
            print('3')
            client.publish(mqtt_topic1,"R")
        elif(c > 0 and c< 1000):
            print('2')
            client.publish(mqtt_topic1,"L")
        elif(c > 1000 and c < 2000):
            print('1')
            client.publish(mqtt_topic1,"B")
        else:
            print('0')
            client.publish(mqtt_topic1,"F")
        time.sleep(2)

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
