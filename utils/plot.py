#!/usr/bin/env python3

from datetime import datetime

from pylab import *

from dist_path import dist_path
from settings import _PATHS

%matplotlib

X = {i: [] for i in [1, 2, 3]}
Y = {i: [] for i in [1, 2, 3]}

U = {i: [] for i in [1, 2, 3]}
V = {i: [] for i in [1, 2, 3]}

D = {i: [] for i in [1, 2, 3]}


for i in [1, 2, 3]:
    with open(str(i)) as f:
        for line in f:
            d = datetime.fromtimestamp(int(line.split(' ')[2][:-1]))
            if 10 <= d.hour <= 17:
                U[i].append(d)
                x, y, z = eval(line.split('[')[2].split(']')[0])
                X[i].append(x)
                Y[i].append(y)
                D[i].append(dist_path(_PATHS[i + 1][0], [x, y]))
    # plot(X[i], Y[i])

    #for j, d in enumerate(U[i]):
        #V[i].append(hypot(X[i][j] - X[i][j + 1], Y[i][j] - Y[i][j + 1]))
    plot(U[i], D[i])
