import paho.mqtt.client as mqtt
import sys
import numpy as np
import time
import matplotlib.pyplot as plt
import itertools

HOST = '127.0.0.1'
PORT = 1883
TIMEOUT = 60

TOPIC = "topic/"
topics = {}
data = []
subs = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with error code " + str(rc))
    for arg in sys.argv[1:]:
        global data
        global subs
        client.subscribe(TOPIC + str(arg))
        subs += 1
        data.append([])
        topics[TOPIC + str(arg)] = []


def on_message(client, userdata, msg):
    global data
    global subs
    topic = msg.topic
    message = str(msg.payload.decode())
    if message == "END":
        client.unsubscribe(msg.topic)
        subs -= 1
    else:
        if topic in topics:
            topics[topic].append(int(message))


client = mqtt.Client()
client.connect(HOST, PORT, TIMEOUT)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()
time.sleep(1)

while subs > 0:
    pass
client.loop_stop()
client.disconnect()
print("Disconnected")


# data zawiera wszystkie dane pomiarowe
plt.figure()
for key, value in topics.items():
    X = list(range(1, len(value)+1))
    Y = value
    plt.plot(X, Y, 'o', label=(key.split("/")[1]))
plt.xlabel('nr pomiaru')
plt.ylabel('wartość')
plt.legend()
plt.show()
