# -*- coding: utf-8 -*-
import blinker
from twisted.application.service import Service
from twisted.python import log

__author__ = 'viruzzz-kun'


class SimarglClient(Service):
    signal_name = None
    simargl = None

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        for name in dir(cls):
            item = getattr(obj, name)
            if hasattr(item, '_connect_to_signals'):
                for signal in item._connect_to_signals:
                    blinker.signal(signal).connect(item)
        blinker.signal('bouser.simargl:boot').connect(obj._fob)
        return obj

    def _fob(self, simargl):
        self.simargl = simargl
        log.msg(self.fq_name, system="Bootstrap:Simargl")
        if self.signal_name:
            blinker.signal(self.signal_name + ':boot').send(self)

    @property
    def module_name(self):
        module_name = self.__module__
        if module_name.startswith('bouser_simargl.'):
            module_name = module_name[15:]
        elif module_name.startswith('bouser_'):
            module_name = u'bouser.ext.%s' % module_name[7:]
        return module_name

    @property
    def fq_name(self):
        name = u'%s :: %s' % (self.module_name, self.name)
        if not self.signal_name:
            return name
        return "%s (%s)" % (name, self.signal_name)

    def __init__(self, config):
        self.config = config

    def send(self, message):
        """
        :type message: bouser.simargl.message.Message
        :param message:
        :return:
        """
        pass
