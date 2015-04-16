from argparse import ArgumentParser
from math import pi

from .entree import Entree, entree_parser


class EntreeAGV(Entree):
    def __init__(self, v, w, t, stop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data.update(v=v, w=w, t=t % (2 * pi), stop=stop)
        print(self.data)

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
        self.data.update(v=v, w=w, t=t % (2 * pi), stop=stop)
        print(self.data)
        return self.data

entree_agv_parser = ArgumentParser(parents=[entree_parser], conflict_handler='resolve')
entree_agv_parser.add_argument('-v', type=float, default=0, help="vitesse linéaire")
entree_agv_parser.add_argument('-w', type=float, default=0, help="vitesse angulaire")
entree_agv_parser.add_argument('-t', type=float, default=0, help="direction")
entree_agv_parser.add_argument('-s', '--stop', action='store_true', help="stoppe la puissance")

if __name__ == '__main__':
    EntreeAGV(**vars(entree_agv_parser.parse_args())).run()
