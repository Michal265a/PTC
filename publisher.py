import paho.mqtt.client as mqtt
import time
import random
import sys
import math

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

# Czytanie listy argumentów
if str(sys.argv[0]) == "inf":
    n = math.inf
else:
    n = int(sys.argv[0])  # liczba danych które zostaną wysłane
min_n = int(sys.argv[1])  # minimalna wartość przesłanych danych
max_n = int(sys.argv[2])  # maksymalna wartość przesłanych danych
topics = []  # lista topiców

for topic in sys.argv[3:]:
    topics.append("toipic/" + topic)


# Połączenie z brokerem
host = "127.0.0.1"
client = mqtt.Client()
client.connect(host)

# Przesyłanie danych
finish = True
tmp = 1
while finish:
    for topic in topics:
        i = random.randint(min_n, max_n)
        client.publish(topic, i)
        print(i)
        time.sleep(2)
    tmp += 1
    if tmp == n:
        break

# sygnał pomocniczy informujacy o koncu przesylania danych
for topic in topics:
    client.publish("toipic/" + topic, "END")

client.disconnect()  # odłączenie z brokerem
