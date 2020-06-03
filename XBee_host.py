import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import time

mqttc = paho.Client()

data = np.arange(0, 1, 1 / 100)
# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x241\r\n".encode())
char = s.read(3)
print("Set MY 0x240.")
print(char.decode())

s.write("ATDL0x141\r\n".encode())
char = s.read(3)
print("Set DL0x140.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")
s.write("/How_Many_Times/run\r".encode())
time.sleep(10)

s.write("/How_Many_Times/run\r".encode())
for i in range (0, 100):
    line = s.readline()
    data[i] = float(line)

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

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


data = ' '.join(str(data).split())
mesg = data
mqttc.publish(topic, mesg)
print(mesg)
time.sleep(1)

s.close()