# -*- coding: utf-8 -*-
from bouser.helpers.api_helpers import get_json
from bouser.helpers.plugin_helpers import BouserPlugin

__author__ = 'viruzzz-kun'


class Notifications(BouserPlugin):
    # noinspection PyUnresolvedReferences
    from .message import Message

    signal_name = 'bouser.simargl'

    def __init__(self, config):
        self.api_url = config.get('url', 'http://127.0.0.1:5002/').rstrip('/') + '/simargl-rpc/'

    def inject_message(self, message):
        """
        Здесь должен происходить некоторый роутинг
        :type message: bouser.simargl.message.Message
        :param message:
        :return:
        """
        get_json(self.api_url, json=message)


def make(config):
    return Notifications(config)
