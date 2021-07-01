import paho.mqtt.client as mqtt
import subprocess
import time
import json
iptable = []

server = False
def printDict(d):
    print(json.dumps(d, indent = 4))
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IPTABLE",2)
    client.subscribe("login",2)
    client.subscribe("IPTABLE/alive", 2)
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global iptable
    print("Topic: "+msg.topic)
    if str(msg.topic) == "IPTABLE/alive":

    if str(msg.topic) == "login":
        print("neuer client: "+msg.topic)
        printDict(json.loads(msg.payload))

        if server == True:

            iptable.append(json.loads(msg.payload))
            client.publish("IPTABLE", json.dumps(iptable), qos=0, retain=False)
    if str(msg.topic) == "IPTABLE":
        print("update iptable: "+str(json.loads(msg.payload)))
        iptable = json.loads(msg.payload)

brokerport = str(1884)
#broker = subprocess.Popen(r"C:\Users\Norbert\Desktop\mosquitto\mosquitto -p "+brokerport, shell=False)
#print("Broker auf port "+brokerport+" gestartet.")
cliendData = {
    "ip": brokerport,
    "broker": server,
    "cloud": 0
}


print("IPTABLE erstellt")
client = mqtt.Client(client_id="1884")
print("Client ID gesetzt.")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
print("Client mit broker verbunden")
time.sleep(1)
print("eine Sekunde gewartet")
client.publish("login", json.dumps(cliendData), qos=0, retain=False)
print("Client Data an Broker gesendet")

client.loop_forever()
