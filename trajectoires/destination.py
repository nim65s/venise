from math import atan2, hypot, pi

from .trajectoire import Trajectoire


class TrajectoireDestination(Trajectoire):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destination = {h: (0, 0) for h in self.hotes}
        self.wi = {h: 0 for h in self.hotes}

    def distance(self, hote, x, y):
        xi, yi = self.destination[hote]
        return hypot(xi - x, yi - y)

    def go_to_point(self, hote, x, y, a):
        xi, yi = self.destination[hote]
        if x == y == a == 0 or self.distance(hote, x, y) < 0.3 or xi == yi == 0:
            return {'v': 0, 'w': 0}
        return {
                'v': 1,
                't': (atan2(y - yi, x - xi) - a) % (2 * pi),
                'w': self.wi[hote],
                }
