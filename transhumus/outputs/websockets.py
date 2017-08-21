#!/usr/bin/env python

import asyncio
from json import dumps

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

from ..settings import PERIOD
from ..vmq import Subscriber, vmq_parser


class MyServerProtocol(WebSocketServerProtocol):
    connections = []

    def onConnect(self, request):
        self.connections.append(self)
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        self.sendMessage(payload, isBinary)
        self.broadcast_message('plop')

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.connections.remove(self)

    def broadcast_message(self, data):
        data = dumps(data).encode('utf-8')
        for server in self.connections:
            server.sendMessage(data, False)


@asyncio.coroutine
def update():
    subscriber = Subscriber(**vars(vmq_parser.parse_args()))
    while True:
        subscriber.sub()
        for server in MyServerProtocol.connections:
            server.sendMessage(dumps(subscriber.data).encode('utf-8'))
        yield from asyncio.sleep(PERIOD)


if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory("ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    task = asyncio.Task(update())
    server = loop.run_until_complete(asyncio.gather(coro, task))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
