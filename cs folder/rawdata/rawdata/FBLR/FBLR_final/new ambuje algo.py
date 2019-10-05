
from keras.models import model_from_json
import json
import numpy as np
import paho.mqtt.client as mqtt
import time
#Location Of JSON file
json_file = open('fwdbwd1.json', 'r')
#json_file = open('pkmkb(70).json', 'r')

loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
# Write the file name of the weights
#loaded_model.load_weights("pkmkb(70)_weights.h5")
loaded_model.load_weights("fwdbwd1_weights.h5")
print("Loaded model from disk")

mqtt_username = "username"
mqtt_password = "qwertyuiop"
mqtt_topic1 = "runbot"
mqtt_topic = "wheelgear"
mqtt_broker_ip = "192.168.1.10"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):    
    x = str(msg.payload)[2:-1].split(",")
    #print("x ",x)
    
    #x=attention,meditation,delta,theta,lowAplha,highAlpha,lowBeta,highBeta,lowGamma,highGamma
    y=np.array(x,'float64')
   
    #print("yy",y)
    
    
    y=y.reshape(-1,10,1)
    #print("y ",y)
    prediction = loaded_model.predict(y)
    #print("********")
    #print(prediction)
    aa=prediction[0]
    k=aa.max()
    #print("k ", k)
    qq=list(aa)
    #print('qq ', qq)
    f=qq.index(k)
    #print('f ', f)
    if f==0:
        print("Forward")
        client.publish(mqtt_topic1,"F")
    elif f==1:
        print("Backward")
        client.publish(mqtt_topic1,"B")
    elif f==2:
        print("Left")
        client.publish(mqtt_topic1,"L")
    elif f==3:
        print("Right")
        client.publish(mqtt_topic1,"R")
        
    
    
    time.sleep(1)

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
