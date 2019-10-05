# 0-maybe
# 1-no
# 2-yes

from keras.models import model_from_json
import json
import numpy as np
import paho.mqtt.client as mqtt
import time
import pyttsx3


# Location Of JSON file
json_file = open('yesnomaybe_relu_model_72.json', 'r')

loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
# Write the file name of the weights
loaded_model.load_weights("yesnomaybe_relu_model_weights_72.h5")
print("Loaded model from disk")

mqtt_username = "username"
mqtt_password = "qwertyuiop"
mqtt_topic1 = "runbot"
mqtt_topic = "wheelgear"
mqtt_broker_ip = "192.168.43.131"

engine = pyttsx3.init()
engine.say("Yes!")
engine.setProperty('rate',100)
engine.setProperty('volume', 0.9)

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):    
    x = str(msg.payload)[2:-1].split(",")
    print("x ",x)
    
    #x=attention,meditation,delta,theta,low
    Aplha,highAlpha,lowBeta,highBeta,lowGamma,highGamma
    y=np.array(x,'float64')
    
    
    y=y.reshape(1,10,1)
    print("y ",y)
    prediction = loaded_model.predict(y)
    print("pred ",prediction[0],"-----",prediction[0][0])
    aa=prediction[0]
    k=aa.max()
    #print("k ", k)
    qq=list(aa)
    #print('qq ', qq)
    pos=qq.index(k)
    #print('f ', f)
    # pos = prediction[0].index(max(prediction[0]))
    # print(pos)
    if (pos == 0):
        print("Maybe!")
        engine.say("Maybe!")
        engine.runAndWait()
    elif(pos == 1):
        print("No!")
        engine.say("No!")
        engine.runAndWait()
    else:
        print("Yes!")
        engine.say("Yes!")
        engine.runAndWait()

    time.sleep(0.2)

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
