#!/usr/bin/env python3

from zmq import SUB, SUBSCRIBE, Context


def get_data():
    s = Context().socket(SUB)
    s.connect('tcp://nausicaa:1338')
    s.setsockopt_string(SUBSCRIBE, '')
    return s.recv_json()
