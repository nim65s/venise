from datetime import datetime, timedelta
from itertools import product
from math import atan2, pi, tau
from os.path import expanduser, isfile
from random import randrange

from numpy import array, where, zeros

from ..settings import BOUNDARIES, GRID_COEF
from ..utils.dist_angles import dist_angle
from ..utils.dist_path import dist_path
from ..utils.point_in_polygon import wn_pn_poly
from ..utils.stay_in_poly import stay_in_poly
from .destination import DestinationTrajectory, trajectory_destination_parser


class MonaTrajectory(DestinationTrajectory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = {}
        self.grid = {}
        for h in self.hosts:
            self.grid_size[h] = [int(i) for i in (abs(array(BOUNDARIES[h])) * GRID_COEF + 1).max(axis=0)]
            g = zeros(self.grid_size[h])
            b = abs(array(BOUNDARIES[h])) * GRID_COEF
            for i, j in product(*[range(int(x)) for x in self.grid_size[h]]):
                g[i, j] = abs(wn_pn_poly((i, j), b)) - 1
            self.grid[h] = g
            self.change_destination(**self.data[h])

    def get_v(self, gm, **kwargs):
        return gm[0]

    def get_w(self, gm, **kwargs):
        return gm[1]

    def set_grid(self, host, x, y, gm, inside, **kwargs):
        xi, yi = int(round(x * GRID_COEF)), int(round(y * GRID_COEF))
        if inside and self.grid[host][xi, yi] >= 0:
            self.grid[host][xi, yi] = gm[2]

    def process_speed(self, host, destination, x, y, dest_next, dest_prev, **kwargs):
        self.set_grid(**self.data[host])
        if self.distance(destination, x, y) < 1 or dest_prev or dest_next:
            self.change_destination(**self.data[host])
        return self.go_to_point(**self.data[host])

    def find_dest_extr(self, host, state):
        """ Goes to a destination where the granier probe's signal was extreme """
        maxima = where(self.grid[host] == (self.grid[host].max() if state == 1 else self.grid[host]).min())
        i = randrange(len(maxima[0]))
        return (int(z[i]) for z in maxima)

    def find_dest_other(self, host):
        """ Find a destination where we never have been, or a random one """
        xl, yl = where(self.grid[host] == 0)
        if len(xl):
            i = randrange(len(xl))
            return xl[i], yl[i]
        while True:
            xd, yd = (randrange(z) for z in self.grid_size[host])
            if self.grid[host][xd, yd] >= 0:
                return xd, yd

    def change_destination(self, host, x, y, state, dest_next, dest_prev, inside, **kwargs):
        if not dest_next and not dest_prev:
            state = (state + 1) % 3
        failcount = 0
        while True:
            xd, yd = self.find_dest_other(host) if state == 0 else self.find_dest_extr(host, state)
            xd, yd = xd / GRID_COEF, yd / GRID_COEF
            if inside and not self.safe_way(x, y, xd, yd, host):
                failcount += 1
                if failcount > 5:
                    state = (state + 1) % 3
                    failcount = 0
            else:
                break
        self.data[host].update(state=state, destination=(xd, yd), dest_next=False, dest_prev=False)

    def safe_way(self, x, y, xd, yd, host):
        margin = 0 if dist_path(BOUNDARIES[host], (x, y)) < 1 else 0.5
        return stay_in_poly((x, y), (xd, yd), BOUNDARIES[host], margin=margin)


if __name__ == '__main__':
    MonaTrajectory(**vars(trajectory_destination_parser.parse_args())).run()
