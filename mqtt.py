import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import time

log = np.arange(0, 1, 1 / 100) # log data; create Fs samples
t = np.arange(0, 10, 0.1) # time vector; create Fs samples between 0 and 10.0 sec.

mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    data = str(msg.payload)
    data = data.split()
    log[0] = 0
    for i in range(1, 100):
        log[i] = float(data[i])
    # plot
    print("fuck")
    fig, ax = plt.subplots()
    ax.plot(t, log)
    ax.set_ylabel('Velocity')
    ax.set_xlabel('Time')
    plt.show()

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")
# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

# while(1):
#     mesg = "Hello, world!"
#     mqttc.publish(topic, mesg)
#     print(mesg)
#     time.sleep(1)
mqttc.loop_forever()