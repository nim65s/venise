#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

from json import dumps, loads
import sys

from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log

from zmq import Context, REQ

from jinja2 import Template

from ..settings import ARBRES, R_ARBRES, MAX_X, MAX_Y, N_SONDES, PERIODE, STROKE_WIDTH, SOCKET_TRAJECTOIRES


class Root(resource.Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        return Template(open('index.html').read().decode('utf-8')).render(**globals()).encode('utf-8')


class Subscribe(resource.Resource):
    isLeaf = True

    def __init__(self):
        self.subscribers = set()

    def render_GET(self, request):
        request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
        request.setResponseCode(200)
        self.subscribers.add(request)
        d = request.notifyFinish()
        d.addBoth(self.remove_subscriber)
        log.msg("Adding subscriber...")
        request.write("")
        return server.NOT_DONE_YET

    def publish_to_all(self, data):
        for subscriber in self.subscribers:
            subscriber.write("data: %s\n\n" % data)

    def remove_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            log.msg("Removing subscriber..")
            self.subscribers.remove(subscriber)


class Publish(resource.Resource):
    isLeaf = True

    def __init__(self, subscriber):
        self.subscriber = subscriber
        self.arbres = ARBRES
        self.visiteurs = []
        self.murs = []
        self.sondes = [[0] * N_SONDES] * len(ARBRES)
        self.mmv = []
        self.max = []
        self.socket = Context().socket(REQ)
        self.socket.connect(SOCKET_TRAJECTOIRES)

    def render_POST(self, request):
        if 'sondes' in request.args:
            self.sondes = loads(request.args.get('sondes')[0])
        else:
            log.msg('%s' % request.args)
        request.setResponseCode(200)
        return 'Ok'

    def update_pos(self):
        self.socket.send_json(self.sondes)
        self.murs, self.arbres, self.mmv, self.max, self.visiteurs = self.socket.recv_json()
        self.subscriber.publish_to_all(dumps({
            'arbres': self.arbres,
            'sondes': self.sondes,
            'mmv': self.mmv,
            'max': self.max,
            'visiteurs': self.visiteurs,
            'murs': self.murs,
            }))


class Arbres(resource.Resource):
    isLeaf = True

    def __init__(self, pub):
        self.pub = pub

    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json; charset=utf-8')
        request.setResponseCode(200)
        return dumps(self.pub.arbres)


if __name__ == '__main__':
    root = Root()
    subscribe = Subscribe()
    publish = Publish(subscribe)
    arbres = Arbres(publish)
    root.putChild('sub', subscribe)
    root.putChild('pub', publish)
    root.putChild('arbres', arbres)
    site = server.Site(root)
    reactor.listenTCP(12000, site)
    log.startLogging(sys.stdout)
    LoopingCall(publish.update_pos).start(0.05)
    reactor.run()
