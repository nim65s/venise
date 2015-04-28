from argparse import ArgumentParser
from datetime import datetime
from math import atan2, copysign, hypot

from ..settings import PATH_EXT, INTERIEUR, Hote, MAX_X, MAX_Y, MIN_X, MIN_Y, MAX_X_INT, MAX_Y_INT, MIN_X_INT, MIN_Y_INT
from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireBords(Trajectoire):
    def __init__(self, s1, s2, s3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = {2: s1, 3: s2, 4: s3}

    def process_speed(self, x, y, a, w, hote, **kwargs):
        if x == y == a == 0:
            return {'v': 0, 'w': 0}
        if hote == Hote.moro:
            return self.process_speed_moro(x, y, a, w, hote, **kwargs)
        if not (MIN_X < x < MAX_X) or not (MIN_Y < y < MAX_Y):
            print('OWAIT %s, %.3f %.3f' % (hote, x, y))
            #return {'v': 0, 'w': 0}
        xi, yi = PATH_EXT[self.state[hote]]
        if hypot(xi - x, yi - y) < 0.3:
            self.state[hote] = (self.state[hote] + 1) % len(PATH_EXT)
            print(datetime.now(), hote, self.state[hote])
        return {
                'v': 1,
                't': atan2(y - yi, x - xi) - a,
                'w': w,
                }

    def process_speed_moro(self, x, y, a, w, hote, **kwargs):
        if not (MIN_X_INT < x < MAX_X_INT) or not (MIN_Y_INT < y < MAX_Y_INT):
            print('OWAIT MORO, %.3f %.3f' % (x, y))
            return {'v': 0, 'w': 0}
        xi, yi = INTERIEUR[self.state[hote]]
        if hypot(xi - x, yi - y) < 0.5:
            self.state[hote] = (self.state[hote] + 1) % len(INTERIEUR)
            print(datetime.now(), hote, self.state[hote])
        return {
                'v': 1,
                't': atan2(y - yi, x - xi) - a,
                'w': w,
                }

trajectoire_bords_parser = ArgumentParser(parents=[trajectoire_parser], conflict_handler='resolve')
trajectoire_bords_parser.add_argument('--s1', type=int, default=0, choices=range(len(INTERIEUR)))
trajectoire_bords_parser.add_argument('--s2', type=int, default=0, choices=range(len(PATH_EXT)))
trajectoire_bords_parser.add_argument('--s3', type=int, default=0, choices=range(len(PATH_EXT)))

if __name__ == '__main__':
    TrajectoireBords(**vars(trajectoire_bords_parser.parse_args())).run()
