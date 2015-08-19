from itertools import product
from math import atan2, cos, pi, sin, sqrt

from .settings import DIST_MIN_AGV
from .stay_in_poly import inter


def masque(a, b, marge=DIST_MIN_AGV / 2):
    """ rectangle (vw, wx, xy, yv) de <marge> autour du segment [a b] """
    t = atan2(b[1] - a[1], b[0] - a[0])
    marge *= sqrt(2)
    v = a[0] + marge * cos(t + 3 * pi / 4), a[1] + marge * sin(t + 3 * pi / 4)
    w = a[0] + marge * cos(t - 3 * pi / 4), a[1] + marge * sin(t - 3 * pi / 4)
    x = b[0] + marge * cos(t + 1 * pi / 4), b[1] + marge * sin(t + 1 * pi / 4)
    y = b[0] + marge * cos(t - 1 * pi / 4), b[1] + marge * sin(t - 1 * pi / 4)
    return (v, w), (w, y), (y, x), (x, v)


def no_overlap(a1, d1, a2, d2, marge=DIST_MIN_AGV / 2):
    """ Deux rectangles de <marge> autour de [ai di] n’ont pas d’intersection """
    return all(not inter(a, b, ap, bp) for (a, b), (ap, bp) in product(masque(a1, d1, marge), masque(a2, d2, marge)))
