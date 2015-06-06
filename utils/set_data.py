#!/usr/bin/env python3
from zmq import Context, PUSH


def set_data(h, var, val):
    c = Context()
    s = c.socket(PUSH)
    s.connect('tcp://cerf:1337')
    s.send_json([h, {var: val}])


def moro(var, val):
    set_data(2, var, val)


def ame(var, val):
    set_data(3, var, val)


def yuki(var, val):
    set_data(4, var, val)


if __name__ == '__main__':
    set_data(2, 'x', -7)
    set_data(2, 'y', 12)
    set_data(3, 'x', 8)
    set_data(3, 'y', 8)
    set_data(4, 'x', 24)
    set_data(4, 'y', 9)
    set_data(2, 'v', 1)
    set_data(3, 'v', 0.8)
    set_data(4, 'v', 0.5)
    set_data(2, 'vg', 1)
    set_data(3, 'vg', 0.8)
    set_data(4, 'vg', 0.5)
    set_data(2, 'w', -0.6)
    set_data(3, 'w', 0.3)
    set_data(4, 'w', -0.1)
