# -*- coding: utf-8 -*-
import json

import blinker
from twisted.internet import defer
from twisted.web.resource import Resource

from bouser.utils import as_json
from bouser_simargl.client import SimarglClient
from bouser_simargl.message import Message
from bouser.helpers.plugin_helpers import Dependency
from bouser.helpers.msgpack_helpers import load

__author__ = 'viruzzz-kun'


class Client(SimarglClient, Resource):
    isLeaf = 1
    simargl_client = None
    web = Dependency('bouser.web')
    cas = Dependency('bouser.castiel')

    @web.on
    def on_boot(self, web):
        web.root_resource.putChild('simargl-rpc', self)

    def render(self, request):
        """
        :type request: bouser.web.request.BouserRequest
        :param request:
        :return:
        """
        self.web.crossdomain(request, allow_credentials=True)
        main, sub = request.get_content_type()
        if not main:
            main, sub = 'application', 'json'
        content = request.content.getvalue()
        if sub in ('msgpack', 'application/x-msgpack'):
            data = load(content)
        elif sub == 'json':
            data = json.loads(content, 'utf-8')
        else:
            request.setResponseCode(400, 'Unknown Content Type')
            defer.returnValue('')

        message = Message.from_json(data)

        from twisted.internet import reactor
        reactor.callLater(0, self.simargl.message_received(self, message))

        request.setHeader('content-type', 'application/json; charset=utf-8')
        return as_json({
            'success': True
        })
