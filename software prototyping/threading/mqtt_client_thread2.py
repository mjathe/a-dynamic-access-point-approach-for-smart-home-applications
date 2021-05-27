import paho.mqtt.client as mqtt
import time
import json
import threading
import logging
#from hbmqtt_broker import *
import asyncio
from hbmqtt.broker import Broker
import os
accessPointEnabled = 1
ip = 1883
brokerip = "localhost"
brokerport = 1884
id = ip
DEBUGGING = 1
iptable = {}
client = 0
logger = 0
message_received = ""

config = {
            'listeners': {
                'default': {
                    'type': 'tcp',
                    'bind': 'localhost:'+str(ip)
                    }
                },
                'sys_interval': 10,
                'topic-check': {
                    'enabled': False
                }
            }
broker = Broker(config)

def on_connect(client, userdata, flags, rc):

    logger.info("Connection returned result: "+str(rc))
    topics = [
        ("IPTABLE"),
        ("SENSORDATA")
        ]
    client.subscribe("IPTABLE")
    logger.info("subscribed to topics: "+str(topics))
def on_message(client, userdata, msg):
    global message_received
    time.sleep(1)
    message_received=str(msg.payload.decode("utf-8"))
    handleMessage()

def on_disconnect(client, userdata, rc):
    global iptable
    global brokerport
    if rc != 0:
        logger.warning("Unexpected disconnection.")
    del iptable[str(brokerport)]
    y = 9999
    for x in iptable:
        if int(x) < y:
            y = int(x)
    brokerport = y
    logger.info("new brokerport"+str(brokerport))
    client.loop_stop()
    client.connect(brokerip, brokerport)
    client.loop_start()

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
            client.publish("IPTABLE", json.dumps(ip))
            logger.debug("alive message send")
            time.sleep(5)

def handleMessage():
    global message_received
    global logger
    global iptable
    logger.info("Nachricht von "+message_received+" erhalten.")

    iptable[message_received] = str(time.time())
    logger.info(iptable)

def thr():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(startBroker())
    loop.close()
def main():
    global client

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

async def startBroker():
        await broker.start()

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)

    #starting broker in a new thread:

    #localBroker = mqtt_broker(ip)
    #localBroker.start()
    #localBroker.join()

    #asyncio.get_event_loop().run_until_complete(startBroker())
    #asyncio.get_event_loop().run_forever()

    #localBroker = threading.Thread(target = thr)
    #localBroker.start()
    #localBroker.join()

    client = mqtt.Client(client_id=str(id))
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    logger.info("client set up with id: "+str(id))
    client.enable_logger()

    client.connect(brokerip, brokerport)
    client.loop_start() #starting mqtt client in a thread

    aliveThread = threading.Thread(target=send_alive(ip))
    aliveThread.start()
    aliveThread.join()
