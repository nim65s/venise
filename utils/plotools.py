from pylab import *  # isort:skip


def plot_bord(bord):
    data = [[bord[i], bord[(i + 1) % len(bord)]] for i in range(len(bord))]
    path = []
    for d in data:
        path.append((d[0][0], d[1][0]))
        path.append((d[0][1], d[1][1]))
        path.append('b')
    return path
