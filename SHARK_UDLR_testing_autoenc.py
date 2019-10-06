
from keras.models import model_from_json
import json
import numpy as np
import paho.mqtt.client as mqtt
import time
from keras.models import load_model
from keras_radam import RAdam
from sklearn.preprocessing import StandardScaler
import numpy


#Models
model_U = load_model("7AE_Umodel-1173-0.891304-0.869565_U.h5",custom_objects={'RAdam': RAdam})
model_D = load_model("4AE_Dmodel-4212-0.917808-0.944444_D.h5",custom_objects={'RAdam': RAdam})
model_L = load_model("5AE_Lmodel-1421-0.937500-0.806452_L.h5",custom_objects={'RAdam': RAdam})
model_R = load_model("6AE_Rmodel-241-0.610169-0.800000_R.h5",custom_objects={'RAdam': RAdam})
print('models loaded')


def comp(v):
    
    def up(v):
        #print("up")
        json_file= open('7AE_U_HK_U.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        #print("Loaded")
      
        a=v
        #a=numpy.asarray(a)
        #a=numpy.reshape(a, (-1, 10))
        
        scaler = StandardScaler().fit(a)
        b=scaler.transform(a)
        b=numpy.asarray(b)
        #print('b',b)
       
        c=[]
        for i in range(0,len(b)):
            #print("Len of b ",len(b))
            y=b[i]
          #  print("y",y)
            y=y.reshape(1,10)
            
            prediction = model_U.predict(y)
            aa=prediction[0]
           # print("pred",aa)
            mse = np.mean(np.power(y- aa, 2), axis=1)
            c.append(mse)
       
       # print("done")
        #print(c)
        return c
        
        
        
    def down(v):
        #print("down")
        json_file= open('4AE_D_HK_D.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        
        a=v
        #a=numpy.asarray(a)
       # a=numpy.reshape(a, (-1, 10))
        scaler = StandardScaler().fit(a)
        b=scaler.transform(a)
        b=numpy.asarray(b)
        
        c=[]
        for i in range(0,len(b)):
            y=b[i]
            y=y.reshape(1,10)
            prediction = model_D.predict(y)
            aa=prediction[0]
            mse = np.mean(np.power(y- aa, 2), axis=1)
            c.append(mse)
        #print(c)
        return c
        
    
    def right(v):
        #print("rt")
        json_file= open('6AE_R_HK_R.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
       
        a=v
        #a=numpy.asarray(a)
       # a=numpy.reshape(a, (-1, 10))
        scaler = StandardScaler().fit(a)
        b=scaler.transform(a)
        b=numpy.asarray(b)
        c=[]
        for i in range(0,len(b)):
            y=b[i]
            y=y.reshape(1,10)
            prediction = model_R.predict(y)
            aa=prediction[0]
            mse = np.mean(np.power(y- aa, 2), axis=1)
            c.append(mse)
        #print(c)
        return c



    def left(v):
        #print("lt")
        json_file= open('5AE_L_HK_L.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
       
        a=v
        #a=numpy.asarray(a)
       # a=numpy.reshape(a, (-1, 10))
        scaler = StandardScaler().fit(a)
        b=scaler.transform(a)
        b=numpy.asarray(b)
        c=[]
        for i in range(0,len(b)):
            y=b[i]
            y=y.reshape(1,10)
            prediction = model_L.predict(y)
            aa=prediction[0]
            mse = np.mean(np.power(y- aa, 2), axis=1)
            c.append(mse)
        #print(c)
        return c
   
    upward=up(v)
    rt=right(v)
    downward=down(v)
    lt=left(v)
   
    print("Upward",upward)
    print("downward",downward)
    print("left",lt)
    print("right",rt)
    l=[upward,downward,lt,rt]
    return l

##mqtt config
mqtt_username = "username"
mqtt_password = "qwertyuiop"
mqtt_topic = "sharknadoc"
mqtt_broker_ip = "192.168.43.217"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)

v = []

def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):    
    global v
    x = str(msg.payload)[2:-1].split(",")
  #  print("x ",x)
    
    #x->attention,meditation,delta,theta,lowAplha,highAlpha,lowBeta,highBeta,lowGamma,highGamma
    #print(v,len(v))

    if len(v) < 5:
        v.append(np.array(x,'float64'))
       # print('hi')

    else:  
        
       # print('v:',v)
        
        lst=comp(v)
        print('lst',lst)

        predlst = []
        for i in range(5):
            pl=[]
            for j in range(4):
                pl.append(lst[j][i])
            #print('pl',pl)
            m=min(pl)
            mi = pl.index(m)
            #print('m',m,'mi',mi)
            predlst.append(mi)
            
        print('predlst',predlst)
        n=max(set(predlst), key = predlst.count)
        
        if n==0:
            print("Up")
        elif n==1:
            print('Down')
        elif n==2:
            print("Left")
        elif n==3:
            print("Right")
        
        time.sleep(1)
        v = []

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
