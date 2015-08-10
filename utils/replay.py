#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import date, datetime, timedelta
from os.path import expanduser
from pathlib import Path
from pickle import load
from sys import exit
from time import sleep

import pygame as pg
from numpy import array, exp, pi

from settings import _PATHS, HEIGHT, LEFT_WIDTH, PORT_PUB, PX_PAR_M, RAYON_AGV, WIDTH

PATHS = {i: _PATHS[i + 1][0] for i in [1, 2, 3]}
OLD_PATHS = {1: _PATHS[2][0], 2: _PATHS[4][0], 3: _PATHS[3][0]}
SPEED = 100

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED =   (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE =  (  0,   0, 255)


OCTOTREE = RAYON_AGV * array([exp(2j * pi * i / 8) for i in range(8)])

def coord(carray):
    carray = (complex(LEFT_WIDTH, HEIGHT) - carray) * PX_PAR_M
    return array([carray.real, carray.imag]).T.tolist()

ubi = Path(expanduser('~/ubi'))

parser = ArgumentParser(description='Replay stuffs')
parser.add_argument('day', type=int, nargs='?', default=4, choices=range(1, 32))
parser.add_argument('month', type=int, nargs='?', default=8, choices=range(1, 13))

day = date(2015, **vars(parser.parse_args()))

if not (ubi / day.strftime('%Y-%m-%d')).is_dir():
    print('date pas valide', day)
    exit(1)

paths = PATHS if day > date(2015, 7, 27) else OLD_PATHS

X = {i: [] for i in [1, 2, 3]}
Y = {i: [] for i in [1, 2, 3]}
Z = {i: [] for i in [1, 2, 3]}
U = {i: [] for i in [1, 2, 3]}
D = {i: [] for i in [1, 2, 3]}
E = {i: [] for i in [1, 2, 3]}
X_ = {i: [] for i in [1, 2, 3]}
Y_ = {i: [] for i in [1, 2, 3]}
Z_ = {i: [] for i in [1, 2, 3]}
U_ = {i: [] for i in [1, 2, 3]}
D_ = {i: [] for i in [1, 2, 3]}
E_ = {i: [] for i in [1, 2, 3]}

pg.init()
screen = pg.display.set_mode([WIDTH * PX_PAR_M, HEIGHT * PX_PAR_M])
pg.display.set_caption("float")
screen.fill(WHITE)


try:
    for i in [1, 2, 3]:
        print(day.strftime('%m-%d'), i)
        _x = _y = 0
        if (ubi / day.strftime('%Y-%m-%d') / ('%i.pickle' % i)).is_file():
            with (ubi / day.strftime('%Y-%m-%d') / ('%i.pickle' % i)).open('rb') as f:
                [X[i], Y[i], Z[i], U[i], D[i], E[i]] = load(f)
        else:
            print('euh, je trouve pas le pickle', day / ('%i.pickle' % i))
            exit(2)
        _d = U[i][0]
        for j, d in enumerate(U[i]):
            if (d - _d) >= timedelta(seconds=5):
                U_[i].append(d)
                X_[i].append(X[i][j])
                Y_[i].append(Y[i][j])
                Z_[i].append(Z[i][j])
                _d = d
        print('fin du filtrage:', len(U[i]), len(U_[i]))
        for j, d in enumerate(U_[i]):
            screen.fill(WHITE)
            pg.draw.aalines(screen, BLUE, True, coord(OCTOTREE + complex(X_[i][j], Y_[i][j])), 1)
            pg.display.flip()
            sleep(0.03)
        break
finally:
    pg.quit()
