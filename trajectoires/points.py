from datetime import datetime
from math import atan2, copysign, hypot

from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoirePoints(Trajectoire):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = [(11, 9), (11, 13), (26, 9), (26, 13)]
        self.state = [0, 0, 0, 0, 0]

    def process_speed(self, x, y, a, w, hote, **kwargs):
        if x == y == a == 0:
            return {'v': 0, 'w': 0}
        if hote == 4:
            return {'v': 0, 'w': 0}
        if not (10 < x < 27) or not (8 < y < 14):
            print('OWAIT, %.3f %.3f' % (x, y))
            return {'v': 0, 'w': 0}
        xi, yi = self.points[self.state[hote]]
        if hypot(xi - x, yi - y) < 0.1:
            self.state[hote] = (self.state[hote] + 1) % len(self.points)
            print(datetime.now(), hote, self.state[hote])
        return {
                'v': 1,
                't': atan2(y - yi, x - xi) - a,
                'w': w,
                }


if __name__ == '__main__':
    TrajectoirePoints(**vars(trajectoire_parser.parse_args())).run()
