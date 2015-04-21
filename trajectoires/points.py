from math import atan2, copysign, hypot

from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoirePoints(Trajectoire):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = [(15, 9), (15, 13), (26, 13), (26, 9)]
        self.state = 0

    def process_speed(self, x, y, a, w, **kwargs):
        if x == y == a == 0:
            return {}
        xi, yi = self.points[self.state]
        if hypot(xi - x, yi - y) < 0.1:
            self.state = (self.state + 1) % len(self.points)
            print(self.state)
        if abs(a) > 0.003:
            w = max(min(round(w - copysign(0.01, a), 2), 0.1), -0.1)
        else:
            w = round(w + copysign(0.01, a), 2) if w != 0 else 0
        return {
                'v': 1,
                't': atan2(y - yi, x - xi),
                'w': w,
                }


if __name__ == '__main__':
    TrajectoirePoints(**vars(trajectoire_parser.parse_args())).run()
