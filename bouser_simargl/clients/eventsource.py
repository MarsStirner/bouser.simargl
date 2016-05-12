# -*- coding: utf-8 -*-
from twisted.internet import defer
from twisted.python import failure, log
from twisted.python.failure import Failure
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET

from bouser.helpers.eventsource import make_event
from bouser_simargl.client import SimarglClient
from bouser.helpers.plugin_helpers import Dependency

__author__ = 'viruzzz-kun'


class Client(SimarglClient, Resource):
    isLeaf = 1
    cas = Dependency('bouser.castiel')
    web = Dependency('bouser.web')

    def __init__(self, config):
        SimarglClient.__init__(self, config)
        Resource.__init__(self)
        self.requests = set()

    def send(self, message):
        """
        :type message: simargl.message.Message
        :param message:
        :return:
        """
        if message.control:
            return
        event = make_event(message)
        for request in self.requests:
            if not (message.recipient and request.user != message.recipient):
                request.write(event)

    @web.on
    def web_boot(self, web):
        web.root_resource.putChild('simargl-es', self)

    @defer.inlineCallbacks
    def render(self, request):
        """
        :type request: bouser.web.request.BouserRequest
        :param request:
        :return:
        """
        self.web.crossdomain(request, True)

        def onFinish(result):
            log.msg("Connection from %s closed" % request.getClientIP(), system="Event Source")
            self.requests.remove(request)
            if not isinstance(result, Failure):
                return result

        user_id = yield self.cas.request_get_user_id(request)
        if not user_id:
            request.setResponseCode(401, 'Authentication Failure')
            defer.returnValue('')
        else:
            request.user = user_id
            request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
            request.write(': connection established\n\n')
            self.requests.add(request)
            request.notifyFinish().addBoth(onFinish)
            log.msg("Connection from %s established" % request.getClientIP(), system="Event Source")

        defer.returnValue(NOT_DONE_YET)
