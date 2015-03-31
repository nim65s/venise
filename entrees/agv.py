import sys
from math import pi

from .entree import Entree


class EntreeAGV(Entree):
    def __init__(self, nom='manuelle AGV'):
        super(EntreeAGV, self).__init__(nom=nom)
        [v, w, t] = [float(sys.argv[i + 1]) for i in range(3)] if len(sys.argv) == 4 else [0] * 3
        self.data = {'v': v, 'w': w, 't': t, 'stop': False}

    def send(self, value):
        self.push.send_json([self.host, value])

    def check_value(self, value):
        return value

    def process(self, v, w, t, stop, **kwargs):
        r = input('→ ')
        if 'é' in r: v += 0.2
        if 'p' in r: w += 0.1
        if 'o' in r: t += 0.03
        if 'y' in r: v -= 0.2
        if 'x' in r: w -= 0.1
        if '.' in r: t -= 0.03
        if 'u' in r: v = 0
        if 'i' in r: w = 0
        if 'e' in r: t = 0
        if 'c' in r: stop = False
        if ',' in r: stop = True
        self.data = {'v': v, 'w': w, 't': t % (2 * pi), 'stop': stop}
        print(self.data)
        return self.data

if __name__ == '__main__':
    EntreeAGV().loop()
