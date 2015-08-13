from itertools import product
from pickle import dump
from random import randrange

from numpy import array, where, zeros

from ..settings import BORDS, GRID_COEF, Hote
from ..utils.point_in_polygon import wn_pn_poly
from ..utils.stay_in_poly import stay_in_poly
from .destination import TrajectoireDestination, trajectoire_destination_parser


class TrajectoirePartout(TrajectoireDestination):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = {h: zeros((abs(array(BORDS[h])) * GRID_COEF + 1).max(axis=0)) for h in self.hotes}
        self.grid_size = {}
        self.grid = {}
        for h in self.hotes:
            self.data[h]['smoothe'] = False
            self.grid_size[h] = (abs(array(BORDS[h])) * GRID_COEF + 1).max(axis=0)
            g = zeros(self.grid_size[h])
            b = abs(array(BORDS[h])) * GRID_COEF
            for i, j in product(*[range(int(x)) for x in self.grid_size[h]]):
                g[i, j] = abs(wn_pn_poly((i, j), b)) - 1
            self.grid[h] = g
            self.change_destination(**self.data[h])

    def set_grid(self, hote, x, y, granier, **kwargs):
        if self.grid[hote][x * GRID_COEF, y * GRID_COEF] >= 0:
            self.grid[hote][x * GRID_COEF, y * GRID_COEF] = array(granier).mean()
            with open('/tmp/grid_%i.pickle' % hote, 'wb') as f:
                dump(self.grid[hote], f)

    def process_speed(self, hote, destination, x, y, dest_next, dest_prev, **kwargs):
        self.set_grid(**self.data[hote])
        if self.distance(destination, x, y) < 1 or dest_prev or dest_next:
            self.change_destination(**self.data[hote])
        return self.go_to_point(**self.data[hote])

    def change_destination(self, hote, x, y, state, dest_next, dest_prev, inside, **kwargs):
        xd = yd = -1
        if not dest_next and not dest_prev:
            state += 1
            state %= 3
        failcount = 0
        while xd == yd == -1:
            if state == 0:
                while True:
                    xd, yd = (randrange(z) for z in self.grid_size[hote])
                    if self.grid[hote][xd, yd] >= 0:
                        break
            else:
                maxima = where(self.grid[hote] == (self.grid[hote].max() if state == 1 else abs(self.grid[hote]).min()))
                i = randrange(len(maxima[0]))
                xd, yd = (int(z[i]) for z in maxima)
            xd, yd = xd / GRID_COEF * (-1 if hote == Hote.moro else 1), yd / GRID_COEF
            if inside and not stay_in_poly((x, y), (xd, yd), BORDS[hote]):
                failcount += 1
                if failcount > 5:
                    state += 1
                    state %= 3
                    failcount = 0
                xd = yd = -1
        self.data[hote].update(state=state, destination=(xd, yd), dest_next=False, dest_prev=False)

trajectoire_destination_parser.set_defaults(vw=1)
