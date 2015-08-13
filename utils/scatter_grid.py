#!/usr/bin/env python3

from argparse import ArgumentParser
from pickle import load

import matplotlib.pyplot as plt

x = []
y = []
s = []
c = []

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('n', type=int, nargs='?', choices=[2, 3, 4], default=3)
    host = parser.parse_args().n

    with open('/tmp/grid_%i.pickle' % host, 'rb') as f:
        t = load(f)

    mini = abs(t).min()
    maxi = t.max()

    for i, line in enumerate(t):
        for j, k in enumerate(line):
            x.append(i)
            y.append(j)
            s.append(100 if k != 0 else 0)
            c.append((k - mini) / (maxi - mini) if k > 0 else 0)

    plt.scatter(x, y, s=s, c=c, marker='s', edgecolor='none')
    plt.axis('equal')
    plt.show()
