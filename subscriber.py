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

class Message():
    def __init__(self, full_message):
        full_message = full_message.split(sep="#")
        self.message = full_message[2]
        self.hour = full_message[1]
        self.date = full_message[0]

    @property
    def fulldate(self):
        return self.date + " " + self.hour

    def print(self):
        print(f"messege: {self.message}, datetime: {self.fulldate}")


class Topic():
    def __init__(self, full_topic):
        full_topic = full_topic.split(sep="/")
        self.name = full_topic[0]
        self.device_id = full_topic[1]
        self.channel_id = full_topic[2]

    @property
    def full_topic(self):
        return "/".join([str(self.name), str(self.device_id), str(self.channel_id)])


def on_connect(client, userdata, flags, rc):
    print("Connected with error code " + str(rc))
    for arg in sys.argv[1:]:
        global subs
        topic = Topic(arg)
        client.subscribe(topic.full_topic)
        subs += 1
        topics[topic.full_topic] = []


def on_message(client, userdata, msg):
    global subs
    topic = Topic(msg.topic)
    message = Message(str(msg.payload.decode()))
    if str(message.message) == "END" and topic.full_topic in topics.keys():
        client.unsubscribe(topic.full_topic)
        subs -= 1
    else:
        if topic.full_topic in topics.keys():
            topics[topic.full_topic].append(int(message.message))


# Łączymy z protokołem oraz
client = mqtt.Client()
client.connect(HOST, PORT, TIMEOUT)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()
time.sleep(1)

#  Wykonujemy wykresy w czasie rzeczywistym
# while subs > 0:
#     for key, value in topics.items():
#         plt.plot(list(range(1, len(value) + 1)), value, '-o', label=key)
#     plt.xlabel('nr pomiaru')
#     plt.ylabel('wartość')
#     plt.legend()
#     plt.draw()
#     plt.pause(0.3)
#     plt.cla()
#
# client.loop_stop()
# client.disconnect()
# print("Disconnected")
#
# for key, value in topics.items():
#     print(key)
#     plt.plot(list(range(1, len(value) + 1)), value, '-o', label=key)
# plt.show()

