import paho.mqtt.client as mqtt
import subprocess
import time
from dbtable import *

server = True
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IPTABLE")
    client.subscribe("login")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    if str(msg.topic) == "login":
        print("neuer client: "+msg.topic+" "+(json.loads(msg.payload)))

        if server == True:
            tLoginData = json.loads(msg.payload)
            iptable.insert(tLoginData[0],tLoginData[1],tLoginData[2])
            client.publish("IPTABLE", json.dumps(iptable), qos=0, retain=False)
    if str(msg.topic) == "IPTABLE":
        print("update iptable: "+json.loads(msg.payload))
        iptable = json.loads(msg.payload)

brokerport = str(1882)
#broker = subprocess.Popen(r"C:\Users\Norbert\Desktop\mosquitto\mosquitto -p "+brokerport, shell=False)
#print("Broker auf port "+brokerport+" gestartet.")
iptable = DbTable('nodes',['ip','broker','cloud'])


print("IPTABLE erstellt")
client = mqtt.Client(client_id="1882")
print("Client ID gesetzt.")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1882, 60)
print("Client mit broker verbunden")
time.sleep(1)
print("eine Sekunde gewartet")
client.publish("login", json.dumps[brokerport, server,0], qos=0, retain=False)
print("Client ID an Broker gesendet")

client.loop_forever()
