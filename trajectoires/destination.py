from argparse import ArgumentParser
from math import atan2, hypot, pi, sin, cos
from datetime import datetime

from ..settings import Hote
from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireDestination(Trajectoire):
    def __init__(self, v1, v2, v3, w1, w2, w3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destination = {h: (0, 0) for h in self.hotes}
        self.wi = {2: w1, 3: w2, 4: w3}
        self.vi = {2: v1, 3: v2, 4: v3}

    def distance(self, hote, x, y):
        xi, yi = self.destination[hote]
        return hypot(xi - x, yi - y)

    def go_to_point(self, hote, x, y, a):
        xi, yi = self.destination[hote]
        if x == y == a == 0 or self.distance(hote, x, y) < 0.3 or xi == yi == 0:
            return {'vg': 0, 'wg': 0}
        m = datetime.now().minute + datetime.now().second / 60
        return {
                #'vg': self.vi[hote],
                'vg': round(cos(4 * m + (pi / 2 if hote == Hote.moro else 0)) / 4 + 0.75, 5),
                'tg': round((atan2(y - yi, x - xi) - a) % (2 * pi), 5),
                #'wg': self.wi[hote],
                'wg': round(sin(m / 4 + (pi / 2 if hote == Hote.moro else 0)) / 3, 5),
                }


trajectoire_destination_parser = ArgumentParser(parents=[trajectoire_parser], conflict_handler='resolve')
trajectoire_destination_parser.add_argument('--w1', type=float, default=0)
trajectoire_destination_parser.add_argument('--w2', type=float, default=0)
trajectoire_destination_parser.add_argument('--w3', type=float, default=0)
trajectoire_destination_parser.add_argument('--v1', type=float, default=1)
trajectoire_destination_parser.add_argument('--v2', type=float, default=1)
trajectoire_destination_parser.add_argument('--v3', type=float, default=1)
