from .trajectoire import Trajectoire, trajectoire_parser
from math import copysign, pi


class TrajectoireGranier(Trajectoire):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mini = [10, 10, 10]
        self.maxi = [-10, -10, -10]
        self.m = [0, 0, 0]

    def process_speed(self, granier, v, w, t, **kwargs):
        if not granier:
            return {}
        for i in range(3):
            self.mini[i] = min(granier[i], self.mini[i])
            self.maxi[i] = max(granier[i], self.maxi[i])
            self.m[i] = (granier[i] - self.mini[i]) / (self.maxi[i] - self.mini[i] if self.maxi[i] != self.mini[i] else 1)
        self.m[0] = 2 * self.m[0] - 1
        self.m[1] = 2 * self.m[1] - 1
        self.m[2] = 2 * self.m[2] * pi


        return {
                'v': v + copysign(0.01, self.m[0] - v) if abs(v - self.m[0]) > 0.01 else v,
                'w': w + copysign(0.01, self.m[1] - w) if abs(w - self.m[1]) > 0.01 else w,
                't': t + copysign(0.01, self.m[2] - t) if abs(t - self.m[2]) > 0.01 else t,
                'mini': self.mini,
                'maxi': self.maxi,
                'mmmm': self.m,
                }

if __name__ == '__main__':
    TrajectoireGranier(**vars(trajectoire_parser.parse_args())).loop()
