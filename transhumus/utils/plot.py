#!/usr/bin/env python3

from pylab import *  # isort:skip

from datetime import datetime
from os.path import expanduser
from pathlib import Path
from pickle import dump, load

from dist_path import dist_path
from settings import _PATHS

PATHS = {i: _PATHS[i + 1][0] for i in [1, 2, 3]}
OLD_PATHS = {1: _PATHS[2][0], 2: _PATHS[4][0], 3: _PATHS[3][0]}


ubi = Path(expanduser('~/ubi'))

for day in ubi.iterdir():
    if not day.is_dir():
        continue
    date = datetime.strptime(day.name, '%Y-%m-%d')
    if date.weekday() == 0:
        continue
    paths = PATHS if date > datetime(2015, 7, 27) else OLD_PATHS
    X = {i: [] for i in [1, 2, 3]}
    Y = {i: [] for i in [1, 2, 3]}
    Z = {i: [] for i in [1, 2, 3]}
    U = {i: [] for i in [1, 2, 3]}
    V = {i: [] for i in [1, 2, 3]}
    D = {i: [] for i in [1, 2, 3]}
    E = {i: [] for i in [1, 2, 3]}
    for i in [1, 2, 3]:
        print(date.strftime('%m-%d'), i)
        _x = _y = 0
        if (day / ('%i.pickle' % i)).is_file():
            with (day / ('%i.pickle' % i)).open('rb') as f:
                [X[i], Y[i], Z[i], U[i], D[i], E[i]] = load(f)
        else:
            with (day / str(i)).open() as f:
                for line in f:
                    if ':[' not in line:
                        continue
                    d = datetime.fromtimestamp(int(line.split(' ')[2][:-1]))
                    if 10 <= d.hour <= 17 and d.day == date.day:
                        U[i].append(d)
                        x, y, z = eval(line.split('[')[2].split(']')[0])
                        X[i].append(x)
                        Y[i].append(y)
                        Z[i].append(y)
                        D[i].append(dist_path(paths[i], [x, y]))
                        E[i].append(hypot(x - _x, y - _y))
                        _x, _y = x, y
            with (day / ('%i.pickle' % i)).open('wb') as f:
                dump([X[i], Y[i], Z[i], U[i], D[i], E[i]], f)
        # plot(X[i], Y[i])

        # for j, d in enumerate(U[i]):
            # V[i].append(hypot(X[i][j] - X[i][j + 1], Y[i][j] - Y[i][j + 1]))
        ax = subplot(311)
        ax.set_title(date.strftime('%A %m/%d'))
        plot(X[i], Y[i])
        subplot(312)
        plot(U[i], D[i])
        subplot(313)
        plot(U[i], E[i])
    savefig('img/%s.png' % date.strftime('%m-%d'), dpi=300)
    clf()
    close()
