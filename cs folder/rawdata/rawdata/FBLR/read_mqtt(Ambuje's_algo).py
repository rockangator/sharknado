
from keras.models import model_from_json
import json
import numpy as np
import paho.mqtt.client as mqtt
import time
#Location Of JSON file
json_file = open('pkmkb.json', 'r')

loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
# Write the file name of the weights
loaded_model.load_weights("pkmkb_weights.h5")
print("Loaded model from disk")

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
    print("x ",x)
    
    #x=attention,meditation,delta,theta,lowAplha,highAlpha,lowBeta,highBeta,lowGamma,highGamma
    y=np.array(x,'float64')

    
    
    y=y.reshape(1,10)
    print("y ",y[0])
    prediction = loaded_model.predict(y)
    print("hi")
    print("pred ",prediction)
    if prediction[0][0] >0.7:
        print("Forword")
        client.publish(mqtt_topic1,"F")        
    elif prediction[0][0] <0.48:
        print("Backword")
        client.publish(mqtt_topic1,"B")
    time.sleep(1)

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
