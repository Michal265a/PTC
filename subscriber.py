import paho.mqtt.client as mqtt
import sys
import numpy as np
import time
import matplotlib.pyplot as plt

localhost = '127.0.0.1'
port = 1883
timeout = 60
topic = "topic/"
data = []
subs = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with error code " + str(rc))
    for i in range(int(sys.argv[1])):
        global data
        global subs
        client.subscribe(topic + str(i))
        subs += 1
        data.append([])


def on_message(client, userdata, msg):
    global data
    global subs
    topic = msg.topic.split('/')
    nr_topic = int(topic[2])
    message = msg.payload.decode()
    if message == "END":
        client.unsubscribe(msg.topic)
        subs -= 1
    else:
        data[nr_topic].append(int(message))


client = mqtt.Client()
client.connect(localhost, port, timeout)

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
i = 0
plt.figure()
for tab in data:
    i += 1
    n = len(tab)
    X = np.arange(n)
    Y = np.array(tab)
    plt.plot(X, Y, '.-', label=("data" + str(i)))
plt.xlabel('nr pomiaru')
plt.ylabel('wartość')
plt.legend()
plt.show()
