
from keras.models import model_from_json
import json
import numpy as np
import paho.mqtt.client as mqtt
import time

##Location Of JSON file

json_file = open('2_UDLR_HK.json', 'r')
#json_file = open('UDLR_HK.json', 'r')

loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)


##load weights into new model

loaded_model.load_weights("2_model-018-0.760234-0.764535_.h5")
#loaded_model.load_weights("model-028-0.766813-0.758721_.h5")

print("Loaded model from disk")


##mqtt config
mqtt_username = "username"
mqtt_password = "qwertyuiop"
mqtt_topic = "sharknado"
mqtt_broker_ip = "192.168.1.10"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)

def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):    
    x = str(msg.payload)[2:-1].split(",")
    #print("x ",x)
    
    #x->attention,meditation,delta,theta,lowAplha,highAlpha,lowBeta,highBeta,lowGamma,highGamma
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
        print("Up")
        client.publish(mqtt_topic1,"U")
    elif f==1:
        print("Down")
        client.publish(mqtt_topic1,"D")
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
