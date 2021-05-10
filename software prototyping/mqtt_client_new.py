import paho.mqtt.client as mqtt
import time
import json
import asyncio
import logging

accessPointEnabled = 1
ip = 1884
brokerip = "localhost"
brokerport = 1883
id = ip
DEBUGGING = 1
iptable =[]
client = 0

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
    logger.info("new message on this topic: "+msg.topic)

    if str(msg.topic) == "IPTABLE/ALIVE":
        logger.debug("Client with IP "+str(json.loads(msg.payload))+" is alive.")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected disconnection.")


def setup_client(id):
    global client
    client = mqtt.Client(client_id=str(id))
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    logger.info("client set up with id: "+str(id))
    client.enable_logger()

def connect(brokerip, brokerport : int):
    global client
    client.connect(brokerip, brokerport)


async def send_alive(ip):
    while True:
        global client
        client.publish("IPTABLE/ALIVE", json.dumps(ip))
        logger.debug("alive message send")
        await asyncio.sleep(10)



async def main():
    global client
    await asyncio.sleep(5)
    client.loop_forever()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    logger = logging.getLogger(__name__)
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)

    setup_client(id)
    client.connect(brokerip, brokerport)
    #main()
    loop.run_until_complete(asyncio.gather(send_alive(ip), main()))
