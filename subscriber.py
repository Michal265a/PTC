import paho.mqtt.client as mqtt
import sys
import time
import matplotlib.pyplot as plt
import mysql.connector
"""
Program subscribera dla protokołu mqtt.
Do uruchuomienia skryptu należy podać co najmniej 1 argumenty będący subskrybowanymi topicami. Dane są wysyłane do bazy danych mysql.
"""

HOST = '127.0.0.1'
PORT = 1883
TIMEOUT = 60

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ptc_mqtt"
)
mycursor = mydb.cursor()
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
            val = (topic.device_id, topic.channel_id, message.fulldate, message.message)
            sql = "INSERT INTO measurements (id_device, id_channel, datetime, measure) VALUES (%s, %s, %s, %s)"
            mycursor.execute(sql, val)
            mydb.commit()

client = mqtt.Client()
client.connect(HOST, PORT, TIMEOUT)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()
time.sleep(1)
while subs >0:
    pass
client.loop_stop()

