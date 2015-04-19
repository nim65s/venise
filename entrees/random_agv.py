from argparse import ArgumentParser
from math import copysign, pi
from random import random

from .agv import entree_agv_parser, EntreeAGV


class EntreeAGVRandom(EntreeAGV):
    def __init__(self, vc, wc, tc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data[self.hote].update(vc=vc, wc=wc, tc=tc)
        self.cmpt = -1

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
        self.data[self.hote].update(vc=round(vc, 4), wc=round(wc, 4), tc=round(tc, 4), v=round(v, 4), w=round(w, 4), t=round(t, 4))

entree_agv_random_parser = ArgumentParser(parents=[entree_agv_parser], conflict_handler='resolve')
entree_agv_random_parser.add_argument('-vc', type=float, default=0, help="consigne initiale en vitesse linéaire")
entree_agv_random_parser.add_argument('-wc', type=float, default=0, help="consigne initiale en vitesse angulaire")
entree_agv_random_parser.add_argument('-tc', type=float, default=0, help="consigne initiale en direction")

if __name__ == '__main__':
    EntreeAGVRandom(**vars(entree_agv_random_parser.parse_args())).run()
