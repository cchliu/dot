# Reference
# https://github.com/osrg/ryu/blob/master/ryu/controller/handler.py
#

import inspect
import logging

LOG = logging.getLogger('dot.controller.handler')

class _Caller(object):
    """
    Describe how to handle an event class.
    """
    def __init__(self, ev_source):
        """
        :param ev_source: The module which generates the event.
        ev_cls.__module__ for set_ev_cls
        """
        self.ev_source = ev_source

def _listify(may_list):
    if may_list is None:
        may_list = []
    if not isinstance(may_list, list):
        may_list = [may_list]
    return may_list

def set_ev_cls(ev_cls):
    """
    A decorator for DDoS detection application to declare an event handler.

    Decorated method will become an event handler.
    :param ev_cls: An event class whose instances this application wants to receive.
    """
    def _set_ev_cls(handler):
        if 'callers' not in dir(handler):
            hanlder.callers = {}
        for e in _listify(ev_cls):
            handler.callers[e] = _Caller(e.__module__)
        return handler
    return _set_ev_cls

def _has_caller(method):
    return hasattr(method, 'callers')

def register_instance(i):
    for _k, m in inspect.getmembers(i, inspect.ismethod):
        LOG.debug('instance %s k %s m %s', i, _k, m)
        if _has_caller(m):
            for ev_cls, c in m.callers.items():
                print ev_cls, c
                i.register_handler(ev_cls, m)
