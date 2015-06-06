from argparse import ArgumentParser
from datetime import datetime
from math import atan2, hypot, pi, sin

from ..settings import Hote
from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireDestination(Trajectoire):
    def __init__(self, v1, v2, v3, w1, w2, w3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wi = {2: w1, 3: w2, 4: w3}
        self.vi = {2: v1, 3: v2, 4: v3}

    def distance(self, destination, x, y):
        xi, yi = destination
        return hypot(xi - x, yi - y)

    def go_to_point(self, hote, destination, x, y, a, **kwargs):
        xi, yi = destination
        if x == y == a == 0 or self.distance(destination, x, y) < 0.3 or xi == yi == 0:
            return {'vg': 0, 'wg': 0}
        return {
                'vg': self.get_v(**self.data[hote]),
                'wg': self.get_w(**self.data[hote]),
                'tg': round((atan2(y - yi, x - xi) - a) % (2 * pi), 5),
                }

    def get_v(self, hote, **kwargs):
        # return round(cos(m + (pi / 2 if hote == Hote.moro else 0)) / 4 + 0.75, 5),
        return self.vi[hote]

    def get_w(self, hote, **kwargs):
        m = datetime.now().minute + datetime.now().second / 60
        # 'wg': self.wi[hote]
        if hote == Hote.moro:
            return round(sin(m / 6) / 2, 5)
        if hote == Hote.ame:
            return round(sin(m / 6 + 2 * pi / 3) / 2, 5)
        if hote == Hote.yuki:
            return round(sin(m / 6 + 4 * pi / 3) / 2, 5)


trajectoire_destination_parser = ArgumentParser(parents=[trajectoire_parser], conflict_handler='resolve')
trajectoire_destination_parser.add_argument('--w1', type=float, default=0)
trajectoire_destination_parser.add_argument('--w2', type=float, default=0)
trajectoire_destination_parser.add_argument('--w3', type=float, default=0)
trajectoire_destination_parser.add_argument('--v1', type=float, default=1)
trajectoire_destination_parser.add_argument('--v2', type=float, default=1)
trajectoire_destination_parser.add_argument('--v3', type=float, default=1)
