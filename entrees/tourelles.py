import sys
from math import pi

from .entree import Entree
from .settings import current_host


class EntreeTourelles(Entree):
    def __init__(self, nom='manuelle', host=current_host, period=0.1):
        super(EntreeTourelles, self).__init__(nom=nom, host=host, period=period)
        [v1, v2, v3, t1, t2, t3] = [float(sys.argv[i + 1]) for i in range(6)] if len(sys.argv) == 7 else [0] * 6
        self.data = {'v1': v1, 'v2': v2, 'v3': v3, 't1': t1, 't2': t2, 't3': t3, 'stop': False}

    def send(self, value):
        self.push.send_json([self.host, value])

    def check_value(self, value):
        return value

    def process(self, v1, v2, v3, t1, t2, t3, stop, **kwargs):
        r = input('> ')
        if 'é' in r: v1 += 5
        if 'p' in r: v2 += 5
        if 'o' in r: v3 += 5
        if 'v' in r: t1 += 0.1
        if 'd' in r: t2 += 0.1
        if 'l' in r: t3 += 0.1
        if 'y' in r: v1 -= 5
        if 'x' in r: v2 -= 5
        if '.' in r: v3 -= 5
        if 'q' in r: t1 -= 0.1
        if 'g' in r: t2 -= 0.1
        if 'h' in r: t3 -= 0.1
        if 'u' in r: v1 = 0
        if 'i' in r: v2 = 0
        if 'e' in r: v3 = 0
        if 't' in r: t1 = 0
        if 's' in r: t2 = 0
        if 'r' in r: t3 = 0
        if 'c' in r: stop = False
        if ',' in r: stop = True
        self.data = {'v1': v1, 'v2': v2, 'v3': v3, 't1': t1 % (2 * pi), 't2': t2 % (2 * pi), 't3': t3 % (2 * pi), 'stop': stop}
        print(self.data)
        return self.data

if __name__ == '__main__':
    EntreeTourelles().loop()
