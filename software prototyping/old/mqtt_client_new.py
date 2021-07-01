import paho.mqtt.client as mqtt
import time
import json
import threading
import logging

accessPointEnabled = 1
ip = 1884
brokerip = "localhost"
brokerport = 1883
id = ip
DEBUGGING = 1
iptable =[]
client = 0
logger = 0
message_received = ""
def on_connect(client, userdata, flags, rc):

    logger.info("Connection returned result: "+str(rc))
    topics = [
        ("IPTABLE"),
        ("LOGIN"),
        ("IPTABLE/ALIVE"),
        ("SENSORDATA")
        ]
    client.subscribe("IPTABLE/ALIVE")
    logger.info("subscribed to topics: "+str(topics))
def on_message(client, userdata, msg):
    global message_received
    time.sleep(1)
    message_received=str(msg.payload.decode("utf-8"))
    printMessage()
def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected disconnection.")


def setup_client(id):
    global client

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    logger.info("client set up with id: "+str(id))
    client.enable_logger()

def connect(brokerip, brokerport : int):
    global client
    client.connect(brokerip, brokerport)


def send_alive(ip):
        global client
        while True:
            client.publish("IPTABLE/ALIVE", json.dumps(ip))
            logger.debug("alive message send")
            time.sleep(2)
def printMessage():
    global message_received
    global logger
    logger.info("message received")

def main():
    global client

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    client = mqtt.Client(client_id=str(id))
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    logger.info("client set up with id: "+str(id))
    client.enable_logger()
    client.connect(brokerip, brokerport)
    client.loop_start()
    aliveThread = threading.Thread(target=send_alive(ip))
    aliveThread.start()
    aliveThread.join()
