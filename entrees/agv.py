import sys

from .entree import Entree
from .settings import current_host


class EntreeAGV(Entree):
    def __init__(self, nom='manuelle', host=current_host, period=0.1):
        super(EntreeAGV, self).__init__(nom=nom, host=host, period=period)
        [v1, v2, v3, t1, t2, t3] = [float(sys.argv[i + 1]) for i in range(6)] if len(sys.argv) == 7 else [0] * 6
        self.data = {'v1': v1, 'v2': v2, 'v3': v3, 't1': t1, 't2': t2, 't3': t3, 'stop': False}

    def send(self, value):
        self.push.send_json([self.host, value])

    def check_value(self, value):
        return value

    def process(self, v, w, t, stop, **kwargs):
        r = input('> ')
        if 'é' in r: v += 5
        if 'p' in r: w += 0.01
        if 'o' in r: t += 0.1
        if 'y' in r: v -= 5
        if 'x' in r: w -= 0.01
        if '.' in r: t -= 0.1
        if 'u' in r: v = 0
        if 'i' in r: w = 0
        if 'e' in r: t = 0
        if 'c' in r: stop = False
        if ',' in r: stop = True
        self.data = {'v': v, 'w': w, 't': t, 'stop': stop}
        print(self.data)
        return self.data

if __name__ == '__main__':
    EntreeAGV().loop()
