import paho.mqtt.client as mqtt
import time
import subprocess
import config


p=subprocess.Popen(['echo'])


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config.mqtttopic)

def on_message(client, userdata, msg):
    global p
    if msg.payload.decode() == "strandtest":
        if not(subprocess.Popen.poll(p)):
            subprocess.Popen.terminate(p)
        print("Strandtest\n")
        p = subprocess.Popen(['python','/home/pi/rpi_ws281x/python/examples/strandtest.py'])
    if msg.payload.decode() == "stop":
        print("stop\n");
        if not(subprocess.Popen.poll(p)):
            subprocess.Popen.terminate(p)

    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.username_pw_set(config.mqttuser, config.mqttpass)
client.connect(config.mqttaddr,1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
