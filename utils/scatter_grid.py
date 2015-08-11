#!/usr/bin/env python3

from pickle import load

import matplotlib.pyplot as plt

x = []
y = []
s = []
c = []

with open('/tmp/grid_3.pickle', 'rb') as f:
    t = load(f)

for i, line in enumerate(t):
    for j, k in enumerate(line):
        x.append(i)
        y.append(j)
        s.append(50 if k > 0 else 0)
        c.append(k if k > 0 else 0)

plt.scatter(x, y, s=s, c=c, marker='s')
plt.show()
