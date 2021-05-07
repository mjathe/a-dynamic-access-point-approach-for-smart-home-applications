import logging
import asyncio
from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1
import paho.mqtt.client as mqtt
import json
logger = logging.getLogger(__name__)
ip = "1883"
config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': 'localhost:1883'    # 0.0.0.0:1883
        }
    },
    'sys_interval': 10,
    'topic-check': {
        'enabled': False
    }
}

broker = Broker(config)

@asyncio.coroutine
def startBroker():
    yield from broker.start()

@asyncio.coroutine
def brokerGetMessage():
    C = MQTTClient()
    yield from C.connect('mqtt://localhost:1883/')
    yield from C.subscribe([
        ("IPTABLE", QOS_1)
    ])
    logger.info('Subscribed!')
    try:
        for i in range(1,100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print(packet.payload.data.decode('utf-8'))
    except ClientException as ce:
        logger.error("Client exception : %s" % ce)
@asyncio.coroutine
async def client():
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

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        global iptable
        print("Topic: "+msg.topic)
        if str(msg.topic) == "login":
            print("neuer client: "+msg.topic)
            printDict(json.loads(msg.payload))

            if server == True:

                iptable.append(json.loads(msg.payload))
                client.publish("IPTABLE", json.dumps(iptable), qos=0, retain=False)
        if str(msg.topic) == "IPTABLE":
            print("update iptable: "+str(json.loads(msg.payload)))
            iptable = json.loads(msg.payload)

    brokerport = str(1883)
    #broker = subprocess.Popen(r"C:\Users\Norbert\Desktop\mosquitto\mosquitto -p "+brokerport, shell=False)
    #print("Broker auf port "+brokerport+" gestartet.")
    cliendData = {
        "ip": brokerport,
        "broker": server,
        "cloud": 0
    }


    print("IPTABLE erstellt")
    client = mqtt.Client(client_id="1883")
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


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(startBroker())
    asyncio.get_event_loop().run_until_complete(brokerGetMessage())
    asyncio.get_event_loop().run_until_complete(client())
    asyncio.get_event_loop().run_forever()
