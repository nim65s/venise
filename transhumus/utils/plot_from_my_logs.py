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


ubi = Path(expanduser('/tmp/ubi'))

for day in ubi.glob('ubisense-1.log.*'):
    date_str = day.name[-10:]
    date = datetime.strptime(date_str, '%Y-%m-%d')
    if date.weekday() == 0:
        continue
    if not (ubi / date_str).is_dir():
        (ubi / date_str).mkdir()
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
        pickle_file = (ubi / ('%s-%i.pickle' % (date_str, i)))
        _x = _y = 0
        if pickle_file.is_file():
            with pickle_file.open('rb') as f:
                [X[i], Y[i], Z[i], U[i], D[i], E[i]] = load(f)
        else:
            with (ubi / ('ubisense-%i.log.%s' % (i, date_str))).open() as f:
                for line in f:
                    d = datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S')
                    if 10 <= d.hour <= 17:
                        U[i].append(d)
                        x, y, z = map(float, line.strip().split()[-3:])
                        X[i].append(x)
                        Y[i].append(y)
                        Z[i].append(y)
                        D[i].append(dist_path(paths[i], [x, y]))
                        E[i].append(hypot(x - _x, y - _y))
                        _x, _y = x, y
            with pickle_file.open('wb') as f:
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
    savefig('img_from_my_logs/%s.png' % date.strftime('%m-%d'), dpi=300)
    clf()
    close()
