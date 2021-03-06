# -*- coding: utf-8 -*-

from twisted.application.internet import StreamServerEndpointService
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import ServerFactory

from ..simargl_inter_protocol import SimarglFactory
from bouser.helpers.plugin_helpers import Dependency
from bouser_simargl.client import SimarglClient

__author__ = 'viruzzz-kun'


class SimarglServerFactory(SimarglFactory, ServerFactory):
    pass


class Client(SimarglClient, StreamServerEndpointService):
    simargl = Dependency('bouser.simargl')

    def __init__(self, config):
        SimarglClient.__init__(self, config)

        from twisted.internet import reactor

        self.factory = SimarglServerFactory(self)

        StreamServerEndpointService.__init__(
            self,
            TCP4ServerEndpoint(reactor, int(config.get('port', 9666)), interface=config.get('host')),
            self.factory
        )

    def send(self, message):
        print('Simargl Server tries to send a message')
        self.factory.send(message)
