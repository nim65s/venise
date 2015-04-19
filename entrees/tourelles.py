from argparse import ArgumentParser
from math import pi

from .entree import Entree, entree_parser


class EntreeTourelles(Entree):
    def __init__(self, v1, v2, v3, t1, t2, t3, stop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data[self.hote].update(v1=v1, v2=v2, v3=v3, t1=t1 % (2 * pi), t2=t2 % (2 * pi), t3=t3 % (2 * pi), stop=stop)
        self.printe(self.data)

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
        self.data[self.hote].update(v1=v1, v2=v2, v3=v3, t1=t1 % (2 * pi), t2=t2 % (2 * pi), t3=t3 % (2 * pi), stop=stop)
        self.printe(self.data)

entree_tourelles_parser = ArgumentParser(parents=[entree_parser], conflict_handler='resolve')
entree_tourelles_parser.add_argument('-v1', type=float, default=0, help="tourelle 1: vitesse linéaire")
entree_tourelles_parser.add_argument('-v2', type=float, default=0, help="tourelle 2: vitesse linéaire")
entree_tourelles_parser.add_argument('-v3', type=float, default=0, help="tourelle 3: vitesse linéaire")
entree_tourelles_parser.add_argument('-t1', type=float, default=0, help="tourelle 1: orientation")
entree_tourelles_parser.add_argument('-t2', type=float, default=0, help="tourelle 2: orientation")
entree_tourelles_parser.add_argument('-t3', type=float, default=0, help="tourelle 3: orientation")
entree_tourelles_parser.add_argument('-s', '--stop', action='store_true', help="stoppe la puissance")

if __name__ == '__main__':
    EntreeTourelles(**vars(entree_tourelles_parser.parse_args())).run()
