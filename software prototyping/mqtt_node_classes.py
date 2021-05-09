""" Class node """

import logging
import asyncio
from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1
import paho.mqtt.client as mqtt
import json


class mqtt_node():
    accessPointEnabled = 0
    ip = 0
    config = 0
    broker = 0
    logger = 0
    accessPointIP = 0

    def __init__(self, accessPointEnabled, ip, accessPointIP = ip):

        self.accessPointEnabled = accessPointEnabled
        self.ip = ip
        self.accessPointIP = accessPointIP
        print("node started: accessPointEnabled: "+str(self.accessPointEnabled)+" ip: "+str(self.ip)+"accessPointIP: "+str(self.accessPointIP))
        self.logger = logging.getLogger(__name__)
        self.config = {
            'listeners': {
                'default': {
                    'type': 'tcp',
                    'bind': 'localhost:'+str(self.ip)
                    }
                },
                'sys_interval': 10,
                'topic-check': {
                    'enabled': False
                }
            }
        print(self.config)

        self.broker = Broker(self.config)
        #if __name__ == '__main__':
        formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
        logging.basicConfig(level=logging.INFO, format=formatter)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.startBroker())
        loop.run_until_complete(self.brokerGetMessage())
        loop.run_forever()


    def __str__(self):
        return f'NodeIP: '+str(self.ip)+'/naccessPointEnabled: '+str(self.accessPointEnabled)+'/naccessPointIP: '+str(self.accessPointIP)+'/n'

    async def startBroker(self):
        await self.broker.start()

    async def brokerGetMessage(self):
        C = MQTTClient()
        await C.connect('mqtt://localhost:'+str(self.accessPointIP)+'/')
        await C.subscribe([
            ("IPTABLE", QOS_1)
        ])
        self.logger.info('Subscribed!')
        try:
            for i in range(1,100):
                message = await C.deliver_message()
                packet = message.publish_packet
                print(packet.payload.data.decode('utf-8'))
        except ClientException as ce:
            self.logger.error("Client exception : %s" % ce)

        async def start_Client(self):
            client = mqtt.Client(client_id=str(self.ip))
