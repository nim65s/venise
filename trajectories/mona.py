from datetime import datetime, timedelta
from itertools import product
from math import atan2, pi
from os.path import expanduser, isfile
from pickle import dump, load
from random import randrange

from numpy import array, where, zeros

from ..settings import BOUNDARIES, GRID_COEF, Host
from ..utils.dist_angles import dist_angle
from ..utils.dist_path import dist_path
from ..utils.no_overlap import no_overlap
from ..utils.point_in_polygon import wn_pn_poly
from ..utils.stay_in_poly import stay_in_poly
from .destination import DestinationTrajectory

PICKLES = expanduser('~/.grid_%i.pickle')


class MonaTrajectory(DestinationTrajectory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = {}
        self.grid = {}
        for h in self.hosts:
            self.data[h]['smoothe'] = False
            self.grid_size[h] = [int(i) for i in (abs(array(BOUNDARIES[h])) * GRID_COEF + 1).max(axis=0)]
            if isfile(PICKLES % h):
                with open(PICKLES % h, 'rb') as f:
                    self.grid[h] = array(load(f))
            else:
                g = zeros(self.grid_size[h])
                b = abs(array(BOUNDARIES[h])) * GRID_COEF
                for i, j in product(*[range(int(x)) for x in self.grid_size[h]]):
                    g[i, j] = abs(wn_pn_poly((i, j), b)) - 1
                self.grid[h] = g
            self.change_destination(**self.data[h])

    def set_grid(self, host, x, y, granier, inside, **kwargs):
        xi, yi = int(round(abs(x) * GRID_COEF)), int(round(abs(y) * GRID_COEF))
        if inside and self.grid[host][xi, yi] >= 0:
            self.grid[host][xi, yi] = array(granier).mean()
            with open(PICKLES % host, 'wb') as f:
                dump(self.grid[host], f)

    def process_speed(self, host, destination, x, y, dest_next, dest_prev, deadlock, **kwargs):
        self.set_grid(**self.data[host])
        if deadlock:
            return self.deadlock(host, deadlock)
        elif self.distance(destination, x, y) < 1 or dest_prev or dest_next:
            self.change_destination(**self.data[host])
        return self.go_to_point(**self.data[host])

    def find_dest_other(self, host):
        """ Trouve une destination où on est jamais allé, sinon random """
        xl, yl = where(self.grid[host] == 0)
        if len(xl):
            i = randrange(len(xl))
            xd, yd = xl[i], yl[i]
        else:
            while True:
                xd, yd = (randrange(z) for z in self.grid_size[host])
                if self.grid[host][xd, yd] >= 0:
                    break
        return xd, yd

    def find_dest_extr(self, host, state):
        """ Retourne à une destination où on avait atteint un extremum """
        maxima = where(self.grid[host] == (self.grid[host].max() if state == 1 else abs(self.grid[host]).min()))
        i = randrange(len(maxima[0]))
        return (int(z[i]) for z in maxima)

    def change_destination(self, host, x, y, state, dest_next, dest_prev, inside, **kwargs):
        xd = yd = -1
        if not dest_next and not dest_prev:
            state += 1
            state %= 3
        failcount = 0
        df = 0
        while xd == yd == -1:
            xd, yd = self.find_dest_other(host) if state == 0 else self.find_dest_extr(host, state)
            xd, yd = xd / GRID_COEF * (-1 if host == host.moro else 1), yd / GRID_COEF
            if inside and self.unsafe_way(x, y, xd, yd, host):
                failcount += 1
                if failcount > 5:
                    state += 1
                    state %= 3
                    failcount = 0
                    df += 1
                    if df > 3:
                        self.data[host].update(**self.deadlock(host, deadlock=datetime.now().timestamp()))
                        return
                xd = yd = -1
        self.data[host].update(state=state, destination=(xd, yd), dest_next=False, dest_prev=False)
        self.invert_direction(**self.data[host])

    def unsafe_way(self, x, y, xd, yd, host):
        marge = 0 if dist_path(BOUNDARIES[host], (x, y)) < 1 else 0.5
        return not stay_in_poly((x, y), (xd, yd), BOUNDARIES[host], marge=marge) or self.collision(host, x, y, xd, yd)

    def invert_direction(self, host, t, x, y, a, w, destination, inverse_rot, **kwargs):
        """ inverse la direction et la rotation si la nouvelle destination est à plus de 2π/3 """
        xd, yd = destination
        tg = round((atan2(y - yd, x - xd) - a) % (2 * pi), 5)
        if abs(dist_angle(t, tg)) > 2 * pi / 3:
            t = (t + pi) % (2 * pi)
            inverse_rot = not inverse_rot
            self.data[host].update(t=t, inverse_rot=inverse_rot, w=-w)

    def deadlock(self, host, deadlock, **kwargs):
        """ stope les moteurs 5s """
        fini = datetime.now() - datetime.fromtimestamp(deadlock) > timedelta(seconds=5)
        return {'stop': False, 'deadlock': False} if fini else {'stop': True, 'deadlock': deadlock}

    def collision(self, host, x, y, xd, yd):
        if host == Host.moro:
            return False
        xo, yo, do, so = (self.data[Host.ame if host == Host.yuki else Host.yuki][var] for var in ['x', 'y', 'destination', 'stop'])
        return not no_overlap((x, y), (xd, yd), (xo, yo), (xo, yo) if so else do)

    def get_v(self, gm, **kwargs):
        return gm[0]

    def get_w(self, gm, inverse_rot, **kwargs):
        return gm[1]
