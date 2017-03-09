from itertools import product
from math import atan2, cos, pi, sin, sqrt

from .settings import DIST_MIN_AGV
from .stay_in_poly import inter


def mask(a, b, margin=DIST_MIN_AGV / 2):
    """ rectangle (vw, wx, xy, yv) of <margin> around segment [a b] """
    t = atan2(b[1] - a[1], b[0] - a[0])
    margin *= sqrt(2)
    v = a[0] + margin * cos(t + 3 * pi / 4), a[1] + margin * sin(t + 3 * pi / 4)
    w = a[0] + margin * cos(t - 3 * pi / 4), a[1] + margin * sin(t - 3 * pi / 4)
    x = b[0] + margin * cos(t + 1 * pi / 4), b[1] + margin * sin(t + 1 * pi / 4)
    y = b[0] + margin * cos(t - 1 * pi / 4), b[1] + margin * sin(t - 1 * pi / 4)
    return (v, w), (w, y), (y, x), (x, v)


def no_overlap(a1, d1, a2, d2, margin=DIST_MIN_AGV / 2):
    """ Two rectangles of <margin> around [ai di] do not intersect """
    return all(not inter(a, b, ap, bp) for (a, b), (ap, bp) in product(mask(a1, d1, margin), mask(a2, d2, margin)))
