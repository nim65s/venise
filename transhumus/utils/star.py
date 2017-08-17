#!/usr/bin/env python

from itertools import product
from os.path import expanduser
from pickle import dump

from numpy import array, zeros

from .point_in_polygon import wn_pn_poly
from .scatter_grid import scatter_grid
from .settings import GRID_COEF, Hote
from .stay_in_poly import stay_in_poly

PICKLES = expanduser('~/.star_%i.pickle')

BORDS = {
        Hote.moro: [[-7, 6], [-7, 12], [-9, 12], [-13, 8], [-13, 6]],
        Hote.ame: [[8, 7], [8, 8], [11, 14], [13, 17], [14.5, 17.5], [20, 14], [27, 14], [32, 13],
            [24, 9], [25, 7], [25, 4], [20, 4], [15, 7], [12, 7], [9.5, 6.5], [9, 6.5]],
        Hote.yuki: [[8, 7], [8, 8], [11, 14], [13, 17], [14.5, 17.5], [20, 14], [27, 14], [32, 13],
            [24, 9], [25, 7], [25, 4], [20, 4], [15, 7], [12, 7], [9.5, 6.5], [9, 6.5]],
        }


def save_star(b, g=None):
    g_s = (b + 1).max(axis=0)
    if g is None:
        g = zeros(g_s)
        for i, j in product(*[range(int(x)) for x in g_s]):
            g[i, j] = abs(wn_pn_poly((i, j), b)) - 1

    for i, j in product(*[range(int(x)) for x in g_s]):
        g[i, j] = sum([stay_in_poly((i, j), dest, b, margin=0, strict=False) for dest in b]) if g[i, j] != -1 else -1

    return g


if __name__ == '__main__':
    for h in [2, 3]:
        b = abs(array(BORDS[h])) * GRID_COEF
        g = save_star(b)

        scatter_grid(g)

        with open(PICKLES % h, 'wb') as f:
            dump(g == g.max(), f)

    with open(PICKLES % 4, 'wb') as f:
        dump(g == g.max(), f)
