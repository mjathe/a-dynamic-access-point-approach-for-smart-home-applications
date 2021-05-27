""" Class node """

import logging
import asyncio
from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1
from threading import Thread
import os


class mqtt_broker(Thread):

    ip = 0
    def __init__(self, ip):

        Thread.__init__(self)
        self.ip = ip

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
        self.broker = Broker(self.config)
    async def startBroker(self):
        await self.broker.start()
    def run(self):

        formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
        logging.basicConfig(level=logging.INFO, format=formatter)


        loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        loop.run_until_complete(self.startBroker())
        loop.run_forever()
