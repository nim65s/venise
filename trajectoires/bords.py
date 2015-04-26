from argparse import ArgumentParser
from datetime import datetime
from math import atan2, copysign, hypot

from ..settings import ANGLES, MAX_X, MAX_Y, MIN_X, MIN_Y
from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireBords(Trajectoire):
    def __init__(self, s1, s2, s3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = {2: s1, 3: s2, 4: s3}

    def process_speed(self, x, y, a, w, hote, **kwargs):
        if x == y == a == 0:
            return {'v': 0, 'w': 0}
        if not (MIN_X < x < MAX_X) or not (MIN_Y < y < MAX_Y):
            print('OWAIT, %.3f %.3f' % (x, y))
            return {'v': 0, 'w': 0}
        xi, yi = ANGLES[self.state[hote]]
        if hypot(xi - x, yi - y) < 0.2:
            self.state[hote] = (self.state[hote] + 1) % len(ANGLES)
            print(datetime.now(), hote, self.state[hote])
        return {
                'v': 1,
                't': atan2(y - yi, x - xi) - a,
                'w': w,
                }

trajectoire_bords_parser = ArgumentParser(parents=[trajectoire_parser], conflict_handler='resolve')
trajectoire_bords_parser.add_argument('--s1', type=int, default=0, choices=range(len(ANGLES)))
trajectoire_bords_parser.add_argument('--s2', type=int, default=0, choices=range(len(ANGLES)))
trajectoire_bords_parser.add_argument('--s3', type=int, default=0, choices=range(len(ANGLES)))

if __name__ == '__main__':
    TrajectoireBords(**vars(trajectoire_bords_parser.parse_args())).run()
