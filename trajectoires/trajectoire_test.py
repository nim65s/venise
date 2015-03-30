from numpy import mean, median, pi, var

from .settings import hosts
from .trajectoire import Trajectoire

ligne = {'v': 1, 'w': 0, 't': 0}
z = {'v': 0, 'w': 1, 't': 0}


class TrajectoireTest(Trajectoire):
    def process_speed(self, host, v, w, t, **kwargs):
        if host != hosts.yuki:
            return {}

        w = max(1, w + 0.1)
        return ligne
