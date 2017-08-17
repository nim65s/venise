#!/usr/bin/env python3
from numpy import *

from point_in_polygon import wn_pn_poly
from settings import *

grid = {h: zeros((abs(array(BORDS[h])) * GRID_COEF + 1).max(axis=0)) for h in [2, 3, 4]}


def nprint(g):
    for l in g.T:
        for i in l:
            print('O' if i == -1 else 'X' if i == -2 else '█' if i else ' ', end='')
        print()


for h in [2, 3, 4]:
    g = grid[h]
    b = abs(array(BORDS[h])) * GRID_COEF

    for i, row in enumerate(g):
        for j, cell in enumerate(row):
            g[i, j] = abs(wn_pn_poly((i, j), b))

    g -= 1
    nprint(g)
