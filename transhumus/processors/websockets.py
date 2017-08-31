import asyncio
from json import dumps, loads

from autobahn.asyncio.websocket import WebSocketServerFactory, WebSocketServerProtocol

from ..settings import AGV_RADIUS, BORDS_SVG, HEIGHT, OCTOGONE, PERIOD, PORT_WS, PX_PER_M, SPEED_MEAN_MAX, WIDTH
from .processor import Processor, processor_parser


def svg_poly(points):
    return ' '.join([','.join(str(n) for n in p) for p in points]),


CONSTS = {
    'px_per_m': PX_PER_M, 'height': HEIGHT, 'width': WIDTH, 'agv_radius': AGV_RADIUS, 'speed_mean_max': SPEED_MEAN_MAX,
    'octogone': svg_poly(OCTOGONE), 'bords': svg_poly(BORDS_SVG[3]),
}


class MyServerProtocol(WebSocketServerProtocol):
    connections = []
    processor = Processor(**vars(processor_parser.parse_args()))

    def onConnect(self, request):
        self.connections.append(self)

    def onOpen(self):
        self.sendMessage(dumps({'consts': CONSTS}).encode())

    def onClose(self, wasClean, code, reason):
        self.connections.remove(self)

    def onMessage(self, payload, isBinary):
        self.processor.send(loads(payload.decode()))

    @classmethod
    @asyncio.coroutine
    def send_all(cls):
        while True:
            cls.processor.sub()
            for connection in cls.connections:
                connection.sendMessage(dumps({'agv': cls.processor.data[cls.processor.host]}).encode())
            yield from asyncio.sleep(PERIOD)


if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://0.0.0.0:%i" % PORT_WS)
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', PORT_WS)
    send_all = asyncio.Task(factory.protocol.send_all())

    server = loop.run_until_complete(asyncio.gather(coro, send_all))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
