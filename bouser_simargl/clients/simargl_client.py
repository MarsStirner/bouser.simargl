# -*- coding: utf-8 -*-
from twisted.internet.protocol import ReconnectingClientFactory

from ..simargl_inter_protocol import SimarglFactory
from bouser.helpers.plugin_helpers import Dependency
from bouser_simargl.client import SimarglClient

__author__ = 'viruzzz-kun'


class SimarglClientFactory(SimarglFactory, ReconnectingClientFactory):
    maxDelay = 120
    # The proportion is divine,
    # You'll find your way to phi, to phi, to phi!
    # The ratio defined,
    # You can't deny it's phi!
    factor = 1.6180339887498948


class Client(SimarglClient):
    simargl = Dependency('bouser.simargl')

    def __init__(self, config):
        SimarglClient.__init__(self, config)
        self.host, self.port = config.get('host', 'localhost'), int(config.get('port', 9666))
        self.factory = SimarglClientFactory(self)

    def startService(self):
        SimarglClient.startService(self)
        from twisted.internet import reactor

        reactor.connectTCP(self.host, int(self.port), self.factory)

    def send(self, message):
        print('Simargl Client tries to send a message')
        self.factory.send(message)
