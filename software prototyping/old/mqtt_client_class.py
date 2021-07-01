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

    def __init__(self, accessPointEnabled, ip, accessPointIP):
        self.accessPointEnabled = accessPointEnabled
        self.ip = ip
        self.accessPointIP = accessPointIP
        formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG, format=formatter)
        self.logger.info('IPTABLE erstellt')
        client = mqtt.Client(client_id=str(self.ip))
        self.logger.info("Client ID gesetzt.")
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", self.accessPointIP, 60)
        self.logger.info("Client mit broker verbunden")
        time.sleep(1)
        self.logger.debug("eine Sekunde gewartet")
        client.publish("login", json.dumps(cliendData), qos=0, retain=False)
        self.logger.info("Client Data an Broker gesendet")

        client.loop_forever()


    def printDict(d):
        print(json.dumps(d, indent = 4))
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        self.logger.debug("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("IPTABLE",2)
        client.subscribe("login",2)
        client.subscribe("IPTABLE/alive", 2)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        global iptable
        self.logger.info("Topic: "+msg.topic)
        if str(msg.topic) == "login":
            self.logger.info("neuer client: "+msg.topic)
            printDict(json.loads(msg.payload))

            if accessPointEnabled == 1:

                iptable.append(json.loads(msg.payload))
                client.publish("IPTABLE", json.dumps(iptable), qos=0, retain=False)
        if str(msg.topic) == "IPTABLE":
            self.logger.info("update iptable: "+str(json.loads(msg.payload)))
            iptable = json.loads(msg.payload)
