import paho.mqtt.client as mqtt
import subprocess
import time
import json
import logging
class mqtt_client():
    iptable = []
    accessPointEnabled = 0
    accessPointIP = 0
    ip = 0
    logger = 0

    def __init__(self, accessPointEnabled, ip, accessPointIP, logger):
        self.accessPointEnabled = accessPointEnabled
        self.ip = ip
        self.accessPointIP = accessPointIP
        self.logger = logger
        self.logger.info('IPTABLE erstellt')
        client = mqtt.Client(client_id=str(self.ip))
        print("Client ID gesetzt.")
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", self.accessPointIP, 60)
        print("Client mit broker verbunden")
        time.sleep(1)
        print("eine Sekunde gewartet")
        client.publish("login", json.dumps(cliendData), qos=0, retain=False)
        print("Client Data an Broker gesendet")

        client.loop_forever()


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
        if str(msg.topic) == "login":
            print("neuer client: "+msg.topic)
            printDict(json.loads(msg.payload))

            if accessPointEnabled == 1:

                iptable.append(json.loads(msg.payload))
                client.publish("IPTABLE", json.dumps(iptable), qos=0, retain=False)
        if str(msg.topic) == "IPTABLE":
            print("update iptable: "+str(json.loads(msg.payload)))
            iptable = json.loads(msg.payload)
