#!/usr/bin/env python3

from zmq import NOBLOCK, SUB, SUBSCRIBE, Context


def get_data(block=NOBLOCK):
    s = Context().socket(SUB)
    s.connect('tcp://nausicaa:1338')
    s.setsockopt_string(SUBSCRIBE, '')
    return s.recv_json(block)
