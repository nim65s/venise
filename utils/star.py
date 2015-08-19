#!/usr/bin/env python

from itertools import product
from os.path import expanduser
from pickle import dump, load

from numpy import array, zeros

from .point_in_polygon import wn_pn_poly
from .scatter_grid import scatter_grid
from .settings import BORDS, GRID_COEF
from .stay_in_poly import stay_in_poly

PICKLES = expanduser('~/.star_%i.pickle')


def save_star(b, g=None):
    g_s = (b + 1).max(axis=0)
    if g is None:
        g = zeros(g_s)
        for i, j in product(*[range(int(x)) for x in g_s]):
            g[i, j] = abs(wn_pn_poly((i, j), b)) - 1

    for i, j in product(*[range(int(x)) for x in g_s]):
        g[i, j] = sum([stay_in_poly((i, j), dest, b, marge=0, strict=False) for dest in b]) if g[i, j] != -1 else -1

    return g


if __name__ == '__main__':
    for h in [2, 3]:
        b = abs(array(BORDS[h])) * GRID_COEF
        g = save_star(b)

        with open(PICKLES % h, 'wb') as f:
            dump(g, f)

        scatter_grid(g)
    with open(PICKLES % 4, 'wb') as f:
        dump(g, f)
