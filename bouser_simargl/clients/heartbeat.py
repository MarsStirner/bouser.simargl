# -*- coding: utf-8 -*-
import time

import blinker
from bouser_simargl.client import SimarglClient
from bouser_simargl.message import Message
from bouser.utils import as_json
from twisted.internet.task import LoopingCall
from twisted.python.log import callWithContext

__author__ = 'viruzzz-kun'


class Client(SimarglClient):
    def startService(self):
        SimarglClient.startService(self)
        LoopingCall(self.loop).start(10)

    def loop(self):
        message = Message()
        message.control = True
        message.topic = 'heartbeat'
        message.data = {'ts': time.time()}
        self.simargl.message_received(self, message)

