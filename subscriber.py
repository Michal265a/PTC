import paho.mqtt.client as mqtt
import sys
import time
import matplotlib.pyplot as plt

"""
Program subscribera dla protokołu mqtt.
Do uruchuomienia skryptu należy podać co najmniej 1 argumenty będący subskrybowanymi topicami

Po otrzymaniu wszystkich danych program rysuje wykres przedstawiający otrzymane dane
"""

HOST = '127.0.0.1'
PORT = 1883
TIMEOUT = 60

TOPIC = "topic/"
topics = {}  # Słownik zawierający subsrybowane topici oraz dane które z nich dotarły
subs = 0  # Liczba subskrybowanych topiców


def on_connect(client, userdata, flags, rc):
    print("Connected with error code " + str(rc))
    for arg in sys.argv[1:]:
        global subs
        client.subscribe(TOPIC + str(arg))
        subs += 1
        topics[TOPIC + str(arg)] = []


def on_message(client, userdata, msg):
    global subs
    topic = msg.topic
    message = str(msg.payload.decode())
    if message == "END":
        client.unsubscribe(msg.topic)
        subs -= 1
    else:
        if topic in topics:
            topics[topic].append(int(message))


# Łączymy z protokołem oraz
client = mqtt.Client()
client.connect(HOST, PORT, TIMEOUT)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()
time.sleep(1)

#  Wykonujemy program dopóki mamy istniejące topici które subskrybujemy
while subs > 0:
    pass

client.loop_stop()
client.disconnect()
print("Disconnected")

#  Rysujemy wykres
plt.figure()
for key, value in topics.items():
    plt.plot(list(range(1, len(value) + 1)), value, 'o', label=(key.split("/")[1]))
plt.xlabel('nr pomiaru')
plt.ylabel('wartość')
plt.legend()
plt.show()
