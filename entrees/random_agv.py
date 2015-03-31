import sys
from math import copysign, pi
from random import random

from .entree import Entree
from .settings import current_host, hosts


class EntreeRandomAGV(Entree):
    def __init__(self, nom='manuelle', host=current_host):
        super(EntreeRandomAGV, self).__init__(nom=nom, host=host)
        [v, w, t, vc, wc, tc] = [float(sys.argv[i + 1]) for i in range(6)] if len(sys.argv) == 7 else [0] * 6
        self.data = {'v': v, 'w': w, 't': t, 'vc': vc, 'wc': wc, 'tc': tc}
        self.cmpt = -1

    def send(self, value):
        self.push.send_json([self.host, value])

    def check_value(self, value):
        return value

    def process(self, v, w, t, vc, wc, tc, **kwargs):
        self.cmpt = (self.cmpt + 1) % 1000
        if self.cmpt == 0:
            vc = random() * 2 - 1
            while abs(vc) < 0.4:
                vc = random() * 2 - 1
        if self.cmpt == 333:
            wc = random() * 2 - 1
        if self.cmpt == 666:
            tc = random() * 2 * pi
        if abs(vc - v) > 0.003:
            v += copysign(0.003, vc - v)
        else:
            v = vc
        if abs(wc - w) > 0.001:
            w += copysign(0.001, wc - w)
        else:
            w = wc
        if abs(tc - t) > 0.001:
            t += copysign(0.001, tc - t)
        else:
            t = tc
        self.data = {'v': v, 'w': w, 't': t, 'vc': vc, 'wc': wc, 'tc': tc}
        print(self.data)
        return self.data

if __name__ == '__main__':
    if len(sys.argv) == 2:
        EntreeRandomAGV(host=hosts[sys.argv[1]]).loop()
    else:
        EntreeRandomAGV().loop()
