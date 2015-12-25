# -*- coding: utf-8 -*-
import ConfigParser
import uuid

from twisted.python import log
from twisted.application.service import MultiService

from bouser.helpers.plugin_helpers import BouserPlugin, Dependency

__author__ = 'viruzzz-kun'


class Simargl(MultiService, BouserPlugin):
    # noinspection PyUnresolvedReferences
    from .message import Message

    signal_name = 'bouser.simargl'
    root = Dependency('bouser')
    name = 'Simargl.Service'

    def __init__(self, config):
        MultiService.__init__(self)
        self.uuid = uuid.uuid4()
        self.clients = {}
        with open(config['config'], 'rt') as fp:
            parsed_config = ConfigParser.ConfigParser()
            parsed_config.readfp(fp)

        for name in parsed_config.sections():
            mod_name = parsed_config.get(name, 'module')
            module = __import__(mod_name, globals(), locals(), fromlist=['Client'])
            client = getattr(module, 'Client')(dict(parsed_config.items(name)))
            client.setName(name)
            client.setServiceParent(self)
            self.clients[name] = client

    def message_received(self, client, message):
        """
        Зднсь должен происходить некоторый роутинг
        :type client: bouser.simargl.client.SimarglClient
        :type message: bouser.simargl.message.Message
        :param client:
        :param message:
        :return:
        """
        if client is not None:
            name = client.name
            if client is not self.clients.get(name):
                log.msg('Name mismatch', system="Simargl")
                return
        if self.uuid.hex in message.hops:
            # log.msg('Short circuit detected', system="Simargl")
            return
        message.hops.append(self.uuid.hex)
        for recipient in self.clients.itervalues():
            log.callWithContext({'subsystem': 'Simargl:Client:%s' % recipient.fq_name}, recipient.send, message)

    def inject_message(self, message):
        return self.message_received(None, message)