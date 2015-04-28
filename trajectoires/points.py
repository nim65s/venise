from math import hypot, atan2
from .trajectoire import Trajectoire

class TrajectoirePoints(Trajectoire):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = {h: (0, 0) for h in self.hotes}
        self.wi = {h: 0 for h in self.hotes}

    def dist_point(self, hote, x, y):
        xi, yi = self.points[hote]
        return hypot(xi - x, yi - y)

    def go_to_point(self, hote, x, y, a):
        xi, yi = self.points[hote]
        if x == y == a == 0 or self.dist_point(hote, x, y) < 0.3 or xi == yi == 0:
            return {'v': 0, 'w': 0}
        return {
                'v': 1,
                't': atan2(y - yi, x - xi) - a,
                'w': self.wi[hote],
                }
