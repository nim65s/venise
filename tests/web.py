#!/usr/bin/env python3
from zmq import Context, SUB, SUBSCRIBE
from settings import PORT_PUB

context = Context()
socket = context.socket(SUB)
socket.connect("tcp://localhost:%i" % PORT_PUB)
socket.setsockopt_string(SUBSCRIBE, u'')  # TODO: les sorties devraient pouvoir override ça
print('get')
print(socket.recv_json())
print('ok')
