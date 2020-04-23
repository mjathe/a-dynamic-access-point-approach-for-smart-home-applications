import paho.mqtt.client as mqtt
import subprocess
server = False
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IPTABLE")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if server == True:
        iptable[msg.payload] =msg.payload
        print(iptable)
brokerport = str(1884)
broker = subprocess.Popen("D:\Sciebo\STUDIUM\Bachelorarbeit\mosquitto\mosquitto -p "+brokerport, shell=False)
print("Broker auf port "+brokerport+" gestartet.")
iptable ={}

client = mqtt.Client(client_id="1884")
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1882, 60)

client.publish("IPTABLE", brokerport, qos=0, retain=False)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
