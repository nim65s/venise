from datetime import datetime, timedelta
from itertools import product
from math import atan2, pi
from os.path import expanduser, isfile
from pickle import dump, load
from random import randrange

from numpy import array, where, zeros

from ..settings import BORDS, GRID_COEF, Hote
from ..utils.dist_angles import dist_angle
from ..utils.no_overlap import no_overlap
from ..utils.point_in_polygon import wn_pn_poly
from ..utils.stay_in_poly import stay_in_poly
from .destination import TrajectoireDestination

PICKLES = expanduser('~/.grid_%i.pickle')


class TrajectoirePartout(TrajectoireDestination):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = {}
        self.grid = {}
        for h in self.hotes:
            self.data[h]['smoothe'] = False
            self.grid_size[h] = (abs(array(BORDS[h])) * GRID_COEF + 1).max(axis=0)
            if isfile(PICKLES % h):
                with open(PICKLES % h, 'rb') as f:
                    self.grid[h] = array(load(f))
            else:
                g = zeros(self.grid_size[h])
                b = abs(array(BORDS[h])) * GRID_COEF
                for i, j in product(*[range(int(x)) for x in self.grid_size[h]]):
                    g[i, j] = abs(wn_pn_poly((i, j), b)) - 1
                self.grid[h] = g
            self.change_destination(**self.data[h])

    def set_grid(self, hote, x, y, granier, inside, **kwargs):
        if inside and self.grid[hote][abs(x) * GRID_COEF, abs(y) * GRID_COEF] >= 0:
            self.grid[hote][abs(x) * GRID_COEF, abs(y) * GRID_COEF] = array(granier).mean()
            with open(PICKLES % hote, 'wb') as f:
                dump(self.grid[hote], f)

    def process_speed(self, hote, destination, x, y, dest_next, dest_prev, deadlock, **kwargs):
        self.set_grid(**self.data[hote])
        if deadlock:
            return self.deadlock(hote, deadlock)
        elif self.distance(destination, x, y) < 1 or dest_prev or dest_next:
            self.change_destination(**self.data[hote])
        return self.go_to_point(**self.data[hote])

    def find_dest_other(self, hote):
        """ Trouve une destination où on est jamais allé, sinon random """
        xl, yl = where(self.grid[hote] == 0)
        if len(xl):
            i = randrange(len(xl))
            xd, yd = xl[i], yl[i]
        else:
            while True:
                xd, yd = (randrange(z) for z in self.grid_size[hote])
                if self.grid[hote][xd, yd] >= 0:
                    break
        return xd, yd

    def find_dest_extr(self, hote, state):
        """ Retourne à une destination où on avait atteint un extremum """
        maxima = where(self.grid[hote] == (self.grid[hote].max() if state == 1 else abs(self.grid[hote]).min()))
        i = randrange(len(maxima[0]))
        return (int(z[i]) for z in maxima)

    def change_destination(self, hote, x, y, state, dest_next, dest_prev, inside, **kwargs):
        xd = yd = -1
        if not dest_next and not dest_prev:
            state += 1
            state %= 3
        failcount = 0
        df = 0
        while xd == yd == -1:
            xd, yd = self.find_dest_other(hote) if state == 0 else self.find_dest_extr(hote, state)
            xd, yd = xd / GRID_COEF * (-1 if hote == Hote.moro else 1), yd / GRID_COEF
            if inside and (not stay_in_poly((x, y), (xd, yd), BORDS[hote]) or self.collision(hote, x, y, xd, yd)):
                failcount += 1
                if failcount > 5:
                    state += 1
                    state %= 3
                    failcount = 0
                    df += 1
                    if df > 3:
                        self.data[hote].update(**self.deadlock(hote, deadlock=datetime.now().timestamp()))
                        return
                xd = yd = -1
        self.data[hote].update(state=state, destination=(xd, yd), dest_next=False, dest_prev=False)
        self.invert_direction(**self.data[hote])

    def invert_direction(self, hote, t, x, y, a, destination, **kwargs):
        """ inverse la direction si la nouvelle destination est à plus de 2π/3 """
        xd, yd = destination
        tg = round((atan2(y - yd, x - xd) - a) % (2 * pi), 5)
        if abs(dist_angle(t, tg)) > 2 * pi / 3:
            t = (t + pi) % (2 * pi)
            self.data[hote].update(t=t)

    def deadlock(self, hote, deadlock, **kwargs):
        """ stope les moteurs 5s """
        fini = datetime.now() - datetime.fromtimestamp(deadlock) > timedelta(seconds=5)
        return {'stop': False, 'deadlock': False} if fini else {'stop': True, 'deadlock': deadlock}

    def collision(self, hote, x, y, xd, yd):
        if hote == Hote.moro:
            return False
        xo, yo, do, so = (self.data[Hote.ame if hote == Hote.yuki else Hote.yuki][var] for var in ['x', 'y', 'destination', 'stop'])
        return not no_overlap((x, y), (xd, yd), (xo, yo), (xo, yo) if so else do)

    def get_v(self, gm, **kwargs):
        return gm[0]

    def get_w(self, gm, **kwargs):
        return gm[1] * 2 - 1
