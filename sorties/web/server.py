#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

import sys
from os.path import expanduser

from jinja2 import Template
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET, Site
from twisted.web.static import File
from zmq import PUSH, SUB, SUBSCRIBE, Context

from settings import *  # YOLO


class Root(Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return Template(open('templates/plan.html').read().decode('utf-8')).render(expert=False, **globals()).encode('utf-8')

    def render_POST(self, request):
        self.socket = Context().socket(PUSH)
        self.socket.connect("tcp://%s:%i" % (MAIN_HOST.name, PORT_PUSH))
        agv, cmd = request.args['cmd[]']
        if cmd == 'stop-ok':
            self.socket.send_json([int(agv), {'stop': True}])
        elif cmd == 'stop-ko':
            self.socket.send_json([int(agv), {'stop': False}])
        elif cmd == 'reverse-ok':
            self.socket.send_json([int(agv), {'reverse': True}])
        elif cmd == 'reverse-ko':
            self.socket.send_json([int(agv), {'reverse': False}])
        elif cmd == 'rotation-ok':
            self.socket.send_json([int(agv), {'rotation': True}])
        elif cmd == 'rotation-ko':
            self.socket.send_json([int(agv), {'rotation': False}])
        elif cmd == 'smoothe-ok':
            self.socket.send_json([int(agv), {'smoothe': True}])
        elif cmd == 'smoothe-ko':
            self.socket.send_json([int(agv), {'smoothe': False}])
        elif cmd == 'smoothe_speed-ok':
            self.socket.send_json([int(agv), {'smoothe_speed': True}])
        elif cmd == 'smoothe_speed-ko':
            self.socket.send_json([int(agv), {'smoothe_speed': False}])
        elif cmd == 'boost-ok':
            self.socket.send_json([int(agv), {'boost': True}])
        elif cmd == 'boost-ko':
            self.socket.send_json([int(agv), {'boost': False}])
        elif cmd == 'arriere-ok':
            self.socket.send_json([int(agv), {'arriere': True}])
        elif cmd == 'arriere-ko':
            self.socket.send_json([int(agv), {'arriere': False}])
        elif cmd == 'sens-ok':
            self.socket.send_json([int(agv), {'sens': True}])
        elif cmd == 'sens-ko':
            self.socket.send_json([int(agv), {'sens': False}])
        elif cmd == 'dest+':
            self.socket.send_json([int(agv), {'dest_next': True}])
        elif cmd == 'dest-':
            self.socket.send_json([int(agv), {'dest_prev': True}])
        elif cmd == 'path+':
            self.socket.send_json([int(agv), {'path_next': True}])
        elif cmd == 'path-':
            self.socket.send_json([int(agv), {'path_prev': True}])
        else:
            print(cmd)
        request.setResponseCode(200)
        return 'Ok'


class Expert(Resource):
    isLeaf = True

    def render_GET(self, request):
        return Template(open('templates/plan.html').read().decode('utf-8')).render(expert=True, **globals()).encode('utf-8')


class Table(Resource):
    isLeaf = True

    def render_GET(self, request):
        return Template(open('templates/table.html').read().decode('utf-8')).render(**globals()).encode('utf-8')


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
    root.putChild('sub', subscribe)
    root.putChild('table', Table())
    root.putChild('expert', Expert())
    root.putChild('static', File('static'))
    root.putChild('logs', File(expanduser('~/logs'), defaultType='text/plain'))
    site = Site(root)
    reactor.listenTCP(8000, site)
    log.startLogging(sys.stdout)
    LoopingCall(subscribe.update).start(0.1)
    reactor.run()
