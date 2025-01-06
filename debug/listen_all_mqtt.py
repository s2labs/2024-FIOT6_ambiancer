from paho.mqtt import client as mqtt_client
import sys
import time

broker="10.42.0.17"
broker="192.168.2.53"
port=1883
client_id = "clientPi3_debug"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("fiot/iot/time")
        client.subscribe("fiot/iot/time-upd")
        client.subscribe("fiot/iot/mood")
        client.subscribe("fiot/iot/show")
        client.subscribe("*")
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    print("[{}]: Message:{}\n".format(message.topic, str(message.payload)))

clientPi = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)  # create client object
clientPi.on_connect= on_connect
clientPi.on_message= on_message
clientPi.connect(broker, port)  # establish connection
clientPi.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nexiting\n")
    clientPi.disconnect()
    clientPi.loop_stop()
    print("bye\n")