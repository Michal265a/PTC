import paho.mqtt.client as mqtt
import time
import random
import sys
import math
import datetime

"""
Program publishera dal protokołu mqtt.
Do uruchuomienia skryptu należy podać co najmniej 4 argumenty.
1 - liczbe danych ktore publisher musi przesłac do poszczególnych topiców
2 - minimalna wartość przesyłanych danych
3 - maksymalna wartość przesyłanych danych
4 - nazwa topicu

Dla ułatawienia testów współpracy publisher z subsrciberem dodaliśmy również na koniec sygnał informujący o 
zakończeniu przesyłania danych. Jeżeli chcemy by dane się przysyłały w sposób ciągły wystarczy dopóki ręcznie nie 
przerwiemy działania, wystarczy w pierwszym topicu wpisać wartość inf.

"""

def make_messege(messege):
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    hour = now.strftime("%H:%M")
    separator = "#"
    return separator.join([str(date), str(hour), str(messege)])


if len(sys.argv) < 5:
    raise Exception("Not enough arguments")
# Czytanie listy argumentów
if str(sys.argv[1]) == "inf":
    n = math.inf
else:
    n = int(sys.argv[1])  # liczba danych które zostaną wysłane
min_n = int(sys.argv[2])  # minimalna wartość przesłanych danych
max_n = int(sys.argv[3])  # maksymalna wartość przesłanych danych
topics = []  # lista topiców


for topic in sys.argv[4:]:
    topics.append("topic/" + str(topic))


# Połączenie z brokerem
HOST = '127.0.0.1'
PORT = 1883
TIMEOUT = 60
client = mqtt.Client()
print("Connecting..")
client.connect(HOST, PORT, TIMEOUT)
print("Connected")

# Przesyłanie danych
tmp = 0
print("Sending data...")
while True:
    for topic in topics:
        i = random.randint(min_n, max_n)
        client.publish(topic, make_messege(i))
        time.sleep(0.3)

    tmp += 1
    if tmp == n:
        break

# sygnał pomocniczy informujacy o koncu przesylania danych\
print("Data sent")
for topic in topics:
    client.publish(topic, make_messege("END"))
    time.sleep(0.3)

client.disconnect()  # odłączenie z brokerem
print("Disconnected")
