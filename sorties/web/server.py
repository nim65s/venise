#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

import sys

from jinja2 import Template
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log
from twisted.web import server
from twisted.web.resource import Resource
from zmq import Context, SUB, SUBSCRIBE

from settings import *  # YOLO


class Root(Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return Template(open('table.html').read().decode('utf-8')).render(**globals()).encode('utf-8')


class Plan(Resource):
    isLeaf = True

    def render_GET(self, request):
        return Template(open('plan.html').read().decode('utf-8')).render(**globals()).encode('utf-8')


class Subscribe(Resource):
    isLeaf = True

    def __init__(self):
        self.subscribers = set()
        self.context = Context()
        self.socket = self.context.socket(SUB)
        self.socket.connect("tcp://%s:%i" % (MAIN_HOST.name, PORT_PUB))
        self.socket.setsockopt_string(SUBSCRIBE, u'')  # TODO: les sorties devraient pouvoir override ça

    def render_GET(self, request):
        request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
        request.setResponseCode(200)
        self.subscribers.add(request)
        d = request.notifyFinish()
        d.addBoth(self.remove_subscriber)
        log.msg("Adding subscriber...")
        request.write("")
        return server.NOT_DONE_YET

    def remove_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            log.msg("Removing subscriber..")
            self.subscribers.remove(subscriber)

    def publish_to_all(self, data):
        for subscriber in self.subscribers:
            subscriber.write("data: %s\n\n" % data)

    def update(self):
        self.publish_to_all(self.socket.recv())


if __name__ == '__main__':
    root = Root()
    subscribe = Subscribe()
    plan = Plan()
    root.putChild('sub', subscribe)
    root.putChild('plan', plan)
    site = server.Site(root)
    reactor.listenTCP(8000, site)
    log.startLogging(sys.stdout)
    LoopingCall(subscribe.update).start(0.1)
    reactor.run()
