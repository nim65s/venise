#!/usr/bin/env python

import asyncio
from json import dumps

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

from ..settings import PERIOD, PX_PAR_M, OCTOGONE, BORDS_SVG, HEIGHT, WIDTH, AGV_RADIUS
from ..vmq import Subscriber, vmq_parser

CONSTS = {
    'px_par_m': PX_PAR_M, 'height': HEIGHT, 'width': WIDTH, 'agv_radius': AGV_RADIUS,
    'octogone': ' '.join([','.join(str(n) for n in p) for p in OCTOGONE]),
    'bords': ' '.join([','.join(str(n) for n in p) for p in BORDS_SVG[3]]),
}

class MyServerProtocol(WebSocketServerProtocol):
    connections = []

    def onConnect(self, request):
        self.connections.append(self)

    def onClose(self, wasClean, code, reason):
        self.connections.remove(self)

    # def onMessage(self, payload, isBinary):
        # if isBinary:
            # print("Binary message received: {0} bytes".format(len(payload)))
        # else:
            # print("Text message received: {0}".format(payload.decode('utf8')))


@asyncio.coroutine
def agv():
    subscriber = Subscriber(**vars(vmq_parser.parse_args()))
    while True:
        subscriber.sub()
        for server in MyServerProtocol.connections:
            server.sendMessage(dumps({'agv': subscriber.data[3]}).encode('utf-8'))
        yield from asyncio.sleep(.5)


@asyncio.coroutine
def consts():
    while True:
        for server in MyServerProtocol.connections:
            server.sendMessage(dumps({'consts': CONSTS}).encode('utf-8'))
        yield from asyncio.sleep(.5)


if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory("ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    task_agv = asyncio.Task(agv())
    task_consts = asyncio.Task(consts())
    server = loop.run_until_complete(asyncio.gather(coro, task_agv, task_consts))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
