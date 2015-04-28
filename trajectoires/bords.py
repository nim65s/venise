from argparse import ArgumentParser
from datetime import datetime
from math import atan2, copysign, hypot

from ..settings import PATHS
from .trajectoire import trajectoire_parser
from .points import TrajectoirePoints


class TrajectoireBords(TrajectoirePoints):
    def __init__(self, s1, s2, s3, w1, w2, w3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = {2: s1, 3: s2, 4: s3}
        self.wi = {2: w1, 3: w2, 4: w3}

    def process_speed(self, x, y, a, w, hote, **kwargs):
        if self.dist_point(hote, x, y) < 0.5:
            print(datetime.now(), hote, self.state[hote])
            self.state[hote] = (self.state[hote] + 1) % len(PATHS[hote])
            self.points[hote] = PATHS[hote][self.state[hote]]
        return self.go_to_point(hote, x, y, a)


trajectoire_bords_parser = ArgumentParser(parents=[trajectoire_parser], conflict_handler='resolve')
trajectoire_bords_parser.add_argument('--s1', type=int, default=0, choices=range(len(PATHS[2])))
trajectoire_bords_parser.add_argument('--s2', type=int, default=0, choices=range(len(PATHS[3])))
trajectoire_bords_parser.add_argument('--s3', type=int, default=0, choices=range(len(PATHS[4])))
trajectoire_bords_parser.add_argument('--w1', type=float, default=0)
trajectoire_bords_parser.add_argument('--w2', type=float, default=0)
trajectoire_bords_parser.add_argument('--w3', type=float, default=0)

if __name__ == '__main__':
    TrajectoireBords(**vars(trajectoire_bords_parser.parse_args())).run()
