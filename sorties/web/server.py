#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

import sys

from jinja2 import Template
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.static import File
from zmq import Context, PUSH, SUB, SUBSCRIBE

from settings import *  # YOLO


class Root(Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return Template(open('static/plan.html').read().decode('utf-8')).render(**globals()).encode('utf-8')

    def render_POST(self, request):
        self.socket = Context().socket(PUSH)
        self.socket.connect("tcp://%s:%i" % (MAIN_HOST.name, PORT_PUSH))
        agv, cmd = request.args['cmd[]']
        if cmd == 'stop':
            self.socket.send_json([int(agv), {'start': False}])
        elif cmd == 'start':
            self.socket.send_json([int(agv), {'start': True}])
        elif cmd == 'reverse-ok':
            self.socket.send_json([int(agv), {'reverse': True}])
        elif cmd == 'reverse-ko':
            self.socket.send_json([int(agv), {'reverse': False}])
        elif cmd == 'smoothe-ok':
            self.socket.send_json([int(agv), {'smoothe': True}])
        elif cmd == 'smoothe-ko':
            self.socket.send_json([int(agv), {'smoothe': False}])
        elif cmd == 'smoothe-speed-ok':
            self.socket.send_json([int(agv), {'smoothe_speed': True}])
        elif cmd == 'smoothe-speed-ko':
            self.socket.send_json([int(agv), {'smoothe_speed': False}])
        elif cmd == 'boost-ok':
            self.socket.send_json([int(agv), {'boost': True}])
        elif cmd == 'boost-ko':
            self.socket.send_json([int(agv), {'boost': False}])
        elif cmd == 'arriere-ok':
            self.socket.send_json([int(agv), {'arriere': True}])
        elif cmd == 'arriere-ko':
            self.socket.send_json([int(agv), {'arriere': False}])
        request.setResponseCode(200)
        return 'Ok'


class Table(Resource):
    isLeaf = True

    def render_GET(self, request):
        return Template(open('static/table.html').read().decode('utf-8')).render(**globals()).encode('utf-8')


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
        return NOT_DONE_YET

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
    table = Table()
    root.putChild('sub', subscribe)
    root.putChild('table', table)
    root.putChild('static', File('static'))
    site = Site(root)
    reactor.listenTCP(8000, site)
    log.startLogging(sys.stdout)
    LoopingCall(subscribe.update).start(0.1)
    reactor.run()
