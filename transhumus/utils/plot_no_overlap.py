from itertools import chain

from pylab import axis, plot, scatter, show

from .get_data import get_data
from .no_overlap import masque
from .plotools import plot_bord
from .settings import BORDS, Host

data = get_data(0)
x, y, d, s = (data[str(Host.yuki.value)][var] for var in ['x', 'y', 'destination', 'stop'])
xo, yo, do, so = (data[str(Host.ame.value)][var] for var in ['x', 'y', 'destination', 'stop'])

plot(*plot_bord(BORDS[3]))
axis('equal')
scatter(x, y, color='blue')
scatter(*d, color='blue')
scatter(xo, yo, color='red')
scatter(*do, color='red')

plot(*list(chain(*[[(x1, x2), (y1, y2), 'b'] for (x1, y1), (x2, y2) in masque((x, y), d)])))
plot(*list(chain(*[[(x1, x2), (y1, y2), 'r'] for (x1, y1), (x2, y2) in masque((xo, yo), do)])))
show()
